from adaptpro.contract import REQUIRED_FAILURE_MODES, REQUIRED_FINDING_IDS, REQUIRED_SOURCE_IDS
from adaptpro.corpus.loader import load_corpus, load_goldset
from adaptpro.evals.checks import check_goldset_integrity, evaluate, evaluate_corpus, evaluate_epic
from adaptpro.fixtures.ask_the_graph import blocked_complete, false_green, legally_aligned
from adaptpro.schema.enums import AlignmentStatus, BoardItemStatus, FailureMode
from adaptpro.schema.models import CanonicalEpic


def test_goldset_matches_planted_contract() -> None:
    gold = load_goldset()
    assert gold.ids() == REQUIRED_FINDING_IDS
    assert gold.modes() == REQUIRED_FAILURE_MODES
    assert gold.epic_id == "ask-the-graph"
    assert check_goldset_integrity(gold).passed


def test_goldset_integrity_fails_if_a_finding_is_removed() -> None:
    gold = load_goldset()
    gold.findings = gold.findings[1:]
    result = check_goldset_integrity(gold)
    assert not result.passed
    assert "missing ids" in result.message


def test_corpus_contains_every_gold_anchor() -> None:
    report = evaluate_corpus(load_goldset(), load_corpus())
    assert report.passed, report.failed_check_ids
    assert load_corpus().by_id().keys() == REQUIRED_SOURCE_IDS


def test_false_green_cannot_declare_aligned() -> None:
    epic = false_green()
    assert epic.declared_status == AlignmentStatus.ALIGNED
    assert _open_board(epic)
    report = evaluate_epic(epic, load_goldset())
    assert not report.passed
    assert "no_false_green" in report.failed_check_ids


def test_deleting_a_planted_finding_fails_coverage() -> None:
    epic = blocked_complete()
    dropped = "AS-write-from-chat"
    epic.contradictions = [item for item in epic.contradictions if item.id != dropped]
    report = evaluate_epic(epic, load_goldset())
    assert not report.passed
    assert "goldset_coverage" in report.failed_check_ids
    assert dropped in next(
        check.message for check in report.checks if check.id == "goldset_coverage"
    )


def test_blocked_complete_is_honest_and_passes() -> None:
    epic = blocked_complete()
    assert epic.declared_status == AlignmentStatus.BLOCKED
    assert {item.id for item in epic.contradictions} == REQUIRED_FINDING_IDS
    assert all(item.status == BoardItemStatus.OPEN for item in epic.contradictions)
    report = evaluate(load_goldset(), load_corpus(), epic)
    assert report.passed, [(c.id, c.message) for c in report.checks if not c.passed]


def test_legally_aligned_can_pass() -> None:
    epic = legally_aligned()
    assert epic.declared_status == AlignmentStatus.ALIGNED
    assert not _open_board(epic)
    report = evaluate(load_goldset(), load_corpus(), epic)
    assert report.passed, [(c.id, c.message) for c in report.checks if not c.passed]


def test_aligned_with_open_board_fails_even_if_goldset_is_complete() -> None:
    epic = blocked_complete()
    mutated = CanonicalEpic(
        **{
            **epic.model_dump(),
            "declared_status": AlignmentStatus.ALIGNED,
            "version": "v-illegal",
            "sign_offs": legally_aligned().sign_offs,
            "will_not_promise": ["Ask anything about your operations"],
        }
    )
    mutated.sign_offs = [
        item.model_copy(update={"epic_version": "v-illegal"}) for item in mutated.sign_offs
    ]
    report = evaluate_epic(mutated, load_goldset())
    assert not report.passed
    assert "no_false_green" in report.failed_check_ids


def test_each_failure_mode_is_planted_in_corpus() -> None:
    gold = load_goldset()
    by_mode = {mode: [] for mode in FailureMode}
    for finding in gold.findings:
        by_mode[finding.failure_mode].append(finding.id)
    for mode, ids in by_mode.items():
        assert ids, f"no planted finding for {mode}"


def _open_board(epic: CanonicalEpic) -> bool:
    return any(item.status == BoardItemStatus.OPEN for item in epic.contradictions)
