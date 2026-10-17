-- SAP PM notifications -> VeridionDowntimeActivity.
--
-- Decisions encoded here (and the gaps they leave):
--  * SAP gives local date and time with no zone. The plant is on Europe/London, so times are converted to UTC.
--  * qmart M3 = planned work, M1/M2 = malfunction/breakdown. Planned work does not count as availability loss.
--  * An open notification (no end date) keeps endTime = null. Downstream OEE ignores it.
--  * The same real-world stop can arrive as two notifications (operator + maintenance). Both are
--    loaded as separate activities; nothing here merges them. oee.py merges overlapping windows.
--  * Two historical activities keep hand-assigned externalIds via raw.activity_xid_map.
select
  coalesce(m.external_id, concat('activity_sap_', n.qmnum))                                   as externalId,
  n.qmtxt                                                                                     as name,
  n.qmnum                                                                                     as sourceId,
  node_reference('sp_veridion_demo', 'src_sap_pm_cv')                                         as source,
  to_utc_timestamp(to_timestamp(concat(n.ausvn, n.auztv), 'yyyyMMddHHmmss'), 'Europe/London') as startTime,
  case when n.ausbs = '' then null
       else to_utc_timestamp(to_timestamp(concat(n.ausbs, n.auztb), 'yyyyMMddHHmmss'), 'Europe/London')
  end                                                                                         as endTime,
  case when n.qmart = 'M3'
       then to_utc_timestamp(to_timestamp(concat(n.ausvn, n.auztv), 'yyyyMMddHHmmss'), 'Europe/London')
  end                                                                                         as scheduledStartTime,
  array_distinct(array(
    node_reference('sp_veridion_demo', f.asset_external_id),
    node_reference('sp_veridion_demo', f.line_asset_external_id)))                             as assets,
  case when n.qmart = 'M3' and n.ursache like 'PM%' then 'planned-maintenance'
       when n.qmart = 'M3'                          then 'changeover'
       when n.ursache like 'PT%'                    then 'process-trip'
       else 'equipment-failure' end                                                           as downtimeCategory,
  case when n.qmart = 'M3' then 'planned' else 'unplanned' end                                as lossClass,
  n.qmart <> 'M3'                                                                             as countsAsAvailabilityLoss,
  n.qmnum                                                                                     as sapNotificationId,
  n.ursache                                                                                   as causeCode,
  n.ernam_role                                                                                as reportedByRole
from `db_veridion_sap_raw`.`pm_notifications` n
left join `db_veridion_sap_raw`.`activity_xid_map` m on n.qmnum = m.qmnum
-- R-301's functional location exists twice (current asset and the decommissioned legacy DCS asset);
-- joining without the status filter would fan out every R-301 notification.
left join `db_veridion_sap_raw`.`pm_functional_locations` f on n.tplnr = f.tplnr and f.status = 'ACTIVE'
