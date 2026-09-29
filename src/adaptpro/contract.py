"""Stable IDs for the Ask the graph planted contract.

Deleting any of these from the gold-set must fail Slice 1 tests.
"""

from adaptpro.schema.enums import FailureMode

EPIC_ID = "ask-the-graph"
EPIC_TITLE = "Ask the graph"
EPIC_INTENT = (
    "Let a user ask a natural-language question over a customer's Cognite Data Fusion "
    "project and get an answer grounded in assets, time series, and files — with "
    "citations — without inventing tag names or asset IDs."
)

FINDING_FF_REALTIME = "FF-realtime"
FINDING_FF_UNDERSTANDS_PLANT = "FF-understands-plant"
FINDING_FF_MVP = "FF-mvp"
FINDING_FF_SOURCE_OF_TRUTH = "FF-source-of-truth"
FINDING_UP_ASK_ANYTHING = "UP-ask-anything"
FINDING_OC_CLUSTER_LOCAL = "OC-cluster-local"
FINDING_OC_NO_INVENTED_IDS = "OC-no-invented-ids"
FINDING_OC_P95_CITATIONS = "OC-p95-and-citations"
FINDING_AS_WRITE_FROM_CHAT = "AS-write-from-chat"
FINDING_SL_DOWNWARD_GROUNDING = "SL-downward-grounding"
FINDING_SL_UPWARD_FILE_COVERAGE = "SL-upward-file-coverage"

REQUIRED_FINDING_IDS: frozenset[str] = frozenset(
    {
        FINDING_FF_REALTIME,
        FINDING_FF_UNDERSTANDS_PLANT,
        FINDING_FF_MVP,
        FINDING_FF_SOURCE_OF_TRUTH,
        FINDING_UP_ASK_ANYTHING,
        FINDING_OC_CLUSTER_LOCAL,
        FINDING_OC_NO_INVENTED_IDS,
        FINDING_OC_P95_CITATIONS,
        FINDING_AS_WRITE_FROM_CHAT,
        FINDING_SL_DOWNWARD_GROUNDING,
        FINDING_SL_UPWARD_FILE_COVERAGE,
    }
)

REQUIRED_FAILURE_MODES: frozenset[FailureMode] = frozenset(FailureMode)

SOURCE_CXO_SLIDE = "cxo-slide"
SOURCE_GTM = "gtm-one-pager"
SOURCE_PRD = "prd-v1"
SOURCE_ADR_GROUNDING = "adr-014-grounding"
SOURCE_ADR_TOOLS = "adr-015-tools"
SOURCE_TICKETS = "tickets"
SOURCE_INTERN_NOTE = "intern-file-coverage"
SOURCE_SLACK = "slack-architect"

REQUIRED_SOURCE_IDS: frozenset[str] = frozenset(
    {
        SOURCE_CXO_SLIDE,
        SOURCE_GTM,
        SOURCE_PRD,
        SOURCE_ADR_GROUNDING,
        SOURCE_ADR_TOOLS,
        SOURCE_TICKETS,
        SOURCE_INTERN_NOTE,
        SOURCE_SLACK,
    }
)

GROUNDING_MARKERS = (
    "I don't know",
    "citation",
    "externalId",
)
