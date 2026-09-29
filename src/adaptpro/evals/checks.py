from dataclasses import dataclass, field

from adaptpro.contract import (
    GROUNDING_MARKERS,
    REQUIRED_FAILURE_MODES,
    REQUIRED_FINDING_IDS,
    REQUIRED_SOURCE_IDS,
)
from adaptpro.corpus.models import AskTheGraphCorpus, GoldSet
from adaptpro.schema.enums import (
    AlignmentStatus,
    Altitude,
    BoardItemStatus,
    ClaimProvenance,
    ConstraintStatus,
    Persona,
    PromiseGapStatus,
)
from adaptpro.schema.models import CanonicalEpic


@dataclass(frozen=True)
class CheckResult:
    id: str
    passed: bool
    message: str


@dataclass
class EvalReport:
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.checks)

    @property
    def failed_check_ids(self) -> list[str]:
        return [check.id for check in self.checks if not check.passed]

    def add(self, check_id: str, passed: bool, message: str) -> None:
        self.checks.append(CheckResult(id=check_id, passed=passed, message=message))


def _open_contradictions(epic: CanonicalEpic) -> list:
    return [item for item in epic.contradictions if item.status == BoardItemStatus.OPEN]


def _accepted_without_owner(epic: CanonicalEpic) -> list:
    return [
        item
        for item in epic.contradictions
        if item.status == BoardItemStatus.ACCEPTED_RISK and not item.owner
    ]


def check_goldset_integrity(goldset: GoldSet) -> CheckResult:
    ids = goldset.ids()
    missing = REQUIRED_FINDING_IDS - ids
    extra = ids - REQUIRED_FINDING_IDS
    missing_modes = REQUIRED_FAILURE_MODES - goldset.modes()
    passed = not missing and not extra and not missing_modes
    parts: list[str] = []
    if missing:
        parts.append(f"missing ids: {sorted(missing)}")
    if extra:
        parts.append(f"unexpected ids: {sorted(extra)}")
    if missing_modes:
        parts.append(f"missing failure modes: {sorted(m.value for m in missing_modes)}")
    if goldset.epic_id != "ask-the-graph":
        passed = False
        parts.append(f"epic_id={goldset.epic_id}")
    return CheckResult(
        id="goldset_integrity",
        passed=passed,
        message="; ".join(parts) if parts else "gold-set matches the planted contract",
    )


def check_corpus_evidence(goldset: GoldSet, corpus: AskTheGraphCorpus) -> CheckResult:
    by_id = corpus.by_id()
    missing_sources = REQUIRED_SOURCE_IDS - set(by_id)
    problems: list[str] = []
    if missing_sources:
        problems.append(f"corpus missing sources: {sorted(missing_sources)}")
    for finding in goldset.findings:
        for anchor in finding.evidence:
            source = by_id.get(anchor.source_id)
            if source is None:
                problems.append(f"{finding.id}: unknown source {anchor.source_id}")
                continue
            if anchor.must_contain not in source.text:
                problems.append(
                    f"{finding.id}: {anchor.source_id} does not contain {anchor.must_contain!r}"
                )
    return CheckResult(
        id="corpus_evidence",
        passed=not problems,
        message="; ".join(problems) if problems else "every gold finding is anchored in the corpus",
    )


def check_goldset_coverage(epic: CanonicalEpic, goldset: GoldSet) -> CheckResult:
    present = {item.id for item in epic.contradictions}
    missing = goldset.ids() - present
    return CheckResult(
        id="goldset_coverage",
        passed=not missing,
        message=(
            f"epic is missing planted findings: {sorted(missing)}"
            if missing
            else "all planted findings appear on the contradiction board"
        ),
    )


def check_no_false_green(epic: CanonicalEpic) -> CheckResult:
    open_items = _open_contradictions(epic)
    unowned = _accepted_without_owner(epic)
    illegal = epic.declared_status == AlignmentStatus.ALIGNED and (open_items or unowned)
    detail = []
    if open_items:
        detail.append(f"open: {sorted(item.id for item in open_items)}")
    if unowned:
        detail.append(f"accepted_risk without owner: {sorted(item.id for item in unowned)}")
    return CheckResult(
        id="no_false_green",
        passed=not illegal,
        message=(
            f"declared ALIGNED while the board is not clear ({'; '.join(detail)})"
            if illegal
            else "declared status does not hide an open board"
        ),
    )


def check_claim_traceability(epic: CanonicalEpic) -> CheckResult:
    problems: list[str] = []
    source_ids = {source.id for source in epic.sources}
    for claim in epic.claims:
        if claim.provenance == ClaimProvenance.SOURCED:
            if not claim.source_ids:
                problems.append(f"{claim.id}: sourced but has no source_ids")
            elif not set(claim.source_ids) <= source_ids:
                problems.append(f"{claim.id}: unknown sources {sorted(set(claim.source_ids) - source_ids)}")
        elif claim.provenance == ClaimProvenance.UNSOURCED and claim.source_ids:
            problems.append(f"{claim.id}: unsourced but lists source_ids")
    return CheckResult(
        id="claim_traceability",
        passed=not problems,
        message="; ".join(problems) if problems else "claims are sourced or explicitly UNSOURCED",
    )


def check_promise_accounting(epic: CanonicalEpic) -> CheckResult:
    open_gaps = [gap for gap in epic.promise_gaps if gap.status == PromiseGapStatus.OPEN]
    unowned = [
        gap
        for gap in epic.promise_gaps
        if gap.status == PromiseGapStatus.ACCEPTED_RISK and not gap.owner
    ]
    illegal = epic.declared_status == AlignmentStatus.ALIGNED and (open_gaps or unowned)
    return CheckResult(
        id="promise_accounting",
        passed=not illegal,
        message=(
            "ALIGNED while promised vs scoped vs buildable is still open"
            if illegal
            else "promise gaps are not hidden behind ALIGNED"
        ),
    )


def check_constraint_promotion(epic: CanonicalEpic) -> CheckResult:
    orphans = [item for item in epic.constraints if item.status == ConstraintStatus.ORPHANED]
    fake_promoted = [
        item
        for item in epic.constraints
        if item.status == ConstraintStatus.PROMOTED
        and not (item.appears_in_product and item.appears_in_business)
    ]
    illegal_aligned = epic.declared_status == AlignmentStatus.ALIGNED and orphans
    passed = not illegal_aligned and not fake_promoted
    parts: list[str] = []
    if illegal_aligned:
        parts.append(f"ALIGNED with orphaned constraints: {sorted(item.id for item in orphans)}")
    if fake_promoted:
        parts.append(
            f"marked promoted but missing Product/Business views: {sorted(item.id for item in fake_promoted)}"
        )
    return CheckResult(
        id="constraint_promotion",
        passed=passed,
        message="; ".join(parts) if parts else "constraints are not silently left in Tech-only",
    )


def check_cross_persona_consistency(epic: CanonicalEpic) -> CheckResult:
    """If ALIGNED, Business must not still sell what Product/Tech cut."""

    if epic.declared_status != AlignmentStatus.ALIGNED:
        return CheckResult(
            id="cross_persona_consistency",
            passed=True,
            message="disagreement is allowed while not ALIGNED",
        )
    sold = " ".join(epic.business.customer_facing_claims).lower()
    cut = " ".join(epic.product.out_of_scope + epic.will_not_promise).lower()
    collisions: list[str] = []
    for token in ("work order", "ask anything", "create a work order"):
        if token in sold and token in cut:
            collisions.append(token)
    write_sold = "work order" in sold or "write" in sold
    write_forbidden = any("no write" in item.lower() or "read-only" in item.lower() for item in epic.tech.interfaces + epic.product.out_of_scope)
    if write_sold and write_forbidden:
        collisions.append("write-from-chat")
    return CheckResult(
        id="cross_persona_consistency",
        passed=not collisions,
        message=(
            f"ALIGNED but personas still assert opposites: {collisions}"
            if collisions
            else "ALIGNED projections do not assert opposite facts"
        ),
    )


def check_grounding_gates(epic: CanonicalEpic) -> CheckResult:
    blob = " ".join(epic.tech.eval_gates + epic.product.acceptance).lower()
    missing = [marker for marker in GROUNDING_MARKERS if marker.lower() not in blob]
    # ALIGNED requires the gates; BLOCKED/DRAFT may still list them as open Tech work.
    if epic.declared_status != AlignmentStatus.ALIGNED:
        return CheckResult(
            id="grounding_gates",
            passed=True,
            message="grounding gates are enforced at ALIGNED",
        )
    return CheckResult(
        id="grounding_gates",
        passed=not missing,
        message=(
            f"ALIGNED without testable grounding gates: {missing}"
            if missing
            else "I don't know, citations, and externalId honesty are testable"
        ),
    )


def check_altitude_fidelity(epic: CanonicalEpic) -> CheckResult:
    problems: list[str] = []
    if epic.intern_view.altitude != Altitude.INTERN:
        problems.append("intern_view.altitude must be intern")
    if epic.cxo_view.altitude != Altitude.CXO:
        problems.append("cxo_view.altitude must be cxo")
    if epic.declared_status == AlignmentStatus.ALIGNED:
        if not epic.intern_view.linked_claim_ids:
            problems.append("intern view has no path up to claims")
        if not epic.cxo_view.will_not_promise and not epic.will_not_promise:
            problems.append("CXO view has no will-not-promise")
        # Blocking intern finding must still be visible at CXO altitude
        if "SL-upward-file-coverage" in {item.id for item in epic.contradictions}:
            cxo_blob = (epic.cxo_view.summary + " " + " ".join(epic.cxo_view.linked_contradiction_ids)).lower()
            if "sl-upward-file-coverage" not in cxo_blob and "file" not in epic.cxo_view.summary.lower():
                problems.append("intern file-coverage finding is not visible in the CXO view")
    return CheckResult(
        id="altitude_fidelity",
        passed=not problems,
        message="; ".join(problems) if problems else "intern and CXO views stay on the same object",
    )


def check_sign_offs(epic: CanonicalEpic) -> CheckResult:
    if epic.declared_status != AlignmentStatus.ALIGNED:
        return CheckResult(
            id="sign_offs",
            passed=True,
            message="sign-offs are required only to declare ALIGNED",
        )
    signed = {item.persona for item in epic.sign_offs if item.epic_version == epic.version}
    missing = set(Persona) - signed
    empty_promise = not epic.will_not_promise
    passed = not missing and not empty_promise
    parts: list[str] = []
    if missing:
        parts.append(f"missing sign-offs: {sorted(p.value for p in missing)}")
    if empty_promise:
        parts.append("ALIGNED brief has no will_not_promise")
    return CheckResult(
        id="sign_offs",
        passed=passed,
        message="; ".join(parts) if parts else "Business, Product, and Tech signed this version",
    )


def evaluate_corpus(goldset: GoldSet, corpus: AskTheGraphCorpus) -> EvalReport:
    report = EvalReport()
    report.checks.append(check_goldset_integrity(goldset))
    report.checks.append(check_corpus_evidence(goldset, corpus))
    return report


def evaluate_epic(epic: CanonicalEpic, goldset: GoldSet) -> EvalReport:
    report = EvalReport()
    report.checks.append(check_goldset_coverage(epic, goldset))
    report.checks.append(check_no_false_green(epic))
    report.checks.append(check_claim_traceability(epic))
    report.checks.append(check_promise_accounting(epic))
    report.checks.append(check_constraint_promotion(epic))
    report.checks.append(check_cross_persona_consistency(epic))
    report.checks.append(check_grounding_gates(epic))
    report.checks.append(check_altitude_fidelity(epic))
    report.checks.append(check_sign_offs(epic))
    return report


def evaluate(
    goldset: GoldSet,
    corpus: AskTheGraphCorpus,
    epic: CanonicalEpic | None = None,
) -> EvalReport:
    report = evaluate_corpus(goldset, corpus)
    if epic is not None:
        report.checks.extend(evaluate_epic(epic, goldset).checks)
    return report
