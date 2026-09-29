from adaptpro.contract import (
    EPIC_ID,
    EPIC_INTENT,
    EPIC_TITLE,
    FINDING_AS_WRITE_FROM_CHAT,
    FINDING_FF_MVP,
    FINDING_FF_REALTIME,
    FINDING_FF_SOURCE_OF_TRUTH,
    FINDING_FF_UNDERSTANDS_PLANT,
    FINDING_OC_CLUSTER_LOCAL,
    FINDING_OC_NO_INVENTED_IDS,
    FINDING_OC_P95_CITATIONS,
    FINDING_SL_DOWNWARD_GROUNDING,
    FINDING_SL_UPWARD_FILE_COVERAGE,
    FINDING_UP_ASK_ANYTHING,
    SOURCE_ADR_GROUNDING,
    SOURCE_ADR_TOOLS,
    SOURCE_CXO_SLIDE,
    SOURCE_GTM,
    SOURCE_INTERN_NOTE,
    SOURCE_PRD,
    SOURCE_SLACK,
    SOURCE_TICKETS,
)
from adaptpro.corpus.loader import load_goldset, load_manifest
from adaptpro.schema.enums import (
    AlignmentStatus,
    Altitude,
    BoardItemStatus,
    ClaimProvenance,
    ConstraintStatus,
    FalseFriendStatus,
    Persona,
    PromiseGapStatus,
)
from adaptpro.schema.models import (
    AltitudeView,
    BusinessProjection,
    CanonicalEpic,
    Claim,
    Constraint,
    Contradiction,
    FalseFriend,
    ProductProjection,
    PromiseGap,
    SignOff,
    SourceRef,
    TechProjection,
)


def _source_refs() -> list[SourceRef]:
    manifest = load_manifest()
    return [
        SourceRef(
            id=item.id,
            title=item.title,
            kind=item.kind,
            filename=item.filename,
            persona_owner=item.persona_owner,
        )
        for item in manifest.sources
    ]


def _contradictions_from_gold(*, status: BoardItemStatus, owner: str | None = None) -> list[Contradiction]:
    gold = load_goldset()
    return [
        Contradiction(
            id=finding.id,
            failure_mode=finding.failure_mode,
            title=finding.title,
            summary=finding.summary,
            source_ids=[anchor.source_id for anchor in finding.evidence],
            status=status,
            owner=owner,
            waiver_reason="Accepted for v1 with a named owner" if status == BoardItemStatus.ACCEPTED_RISK else None,
        )
        for finding in gold.findings
    ]


def _false_friends(*, status: FalseFriendStatus) -> list[FalseFriend]:
    chosen = status == FalseFriendStatus.DEFINED
    return [
        FalseFriend(
            id=FINDING_FF_REALTIME,
            phrase="real-time",
            business_meaning="Fresh enough for a live customer conversation",
            product_meaning="The UI feels instant",
            tech_meaning="Streaming ingest plus sub-second queries",
            chosen_meaning="Query data already in CDF; UI p95 < 8s. No new streaming ingest in v1." if chosen else None,
            status=status,
        ),
        FalseFriend(
            id=FINDING_FF_UNDERSTANDS_PLANT,
            phrase="understands the plant",
            business_meaning="Fluent, trustworthy answers in a customer room",
            product_meaning="A copilot with three templates and empty states",
            tech_meaning="Retrieval that cannot hallucinate IDs, plus access and views",
            chosen_meaning="Grounded answers with citations; refuse invented externalIds." if chosen else None,
            status=status,
        ),
        FalseFriend(
            id=FINDING_FF_MVP,
            phrase="MVP",
            business_meaning="Something we can show in a sales cycle next month",
            product_meaning="Three starter templates, English, read-only",
            tech_meaning="Narrow tool surface with an SLO and eval harness",
            chosen_meaning="Three English read-only templates, citations required, no writes." if chosen else None,
            status=status,
        ),
        FalseFriend(
            id=FINDING_FF_SOURCE_OF_TRUTH,
            phrase="source of truth",
            business_meaning="It is in Cognite",
            product_meaning="The user never leaves Fusion",
            tech_meaning="A specific view in a specific space — not RAW",
            chosen_meaning="Answers are grounded in a named CDF view; not RAW; not last week's export." if chosen else None,
            status=status,
        ),
    ]


def _promise_gap(*, status: PromiseGapStatus, owner: str | None = None) -> PromiseGap:
    return PromiseGap(
        id=FINDING_UP_ASK_ANYTHING,
        promised_text="Ask anything about your operations",
        scoped_text="Three starter question templates, English, read-only",
        buildable_text="Tool-calling over Instances API + file RAG; no write tools; cluster-local",
        promised_source_id=SOURCE_GTM,
        scoped_source_id=SOURCE_PRD,
        buildable_source_id=SOURCE_ADR_TOOLS,
        owner=owner,
        status=status,
    )


def _constraints(*, status: ConstraintStatus, promoted: bool) -> list[Constraint]:
    return [
        Constraint(
            id=FINDING_OC_CLUSTER_LOCAL,
            text="Answers must not leave the customer's CDF cluster / region",
            tech_source_id=SOURCE_ADR_GROUNDING,
            appears_in_product=promoted,
            appears_in_business=promoted,
            owner="Priya Mehta (Architect)" if promoted else None,
            status=status,
        ),
        Constraint(
            id=FINDING_OC_NO_INVENTED_IDS,
            text="Inventing an externalId is worse than saying I don't know",
            tech_source_id=SOURCE_ADR_GROUNDING,
            appears_in_product=promoted,
            appears_in_business=promoted,
            owner="Priya Mehta (Architect)" if promoted else None,
            status=status,
        ),
        Constraint(
            id=FINDING_OC_P95_CITATIONS,
            text="p95 latency and citation coverage are launch blockers, not polish",
            tech_source_id=SOURCE_SLACK,
            appears_in_product=promoted,
            appears_in_business=promoted,
            owner="Priya Mehta (Architect)" if promoted else None,
            status=status,
        ),
    ]


def _claims(*, sourced: bool) -> list[Claim]:
    provenance = ClaimProvenance.SOURCED if sourced else ClaimProvenance.UNSOURCED
    specs = [
        ("CL-intent", "AI that understands the plant", SOURCE_CXO_SLIDE, Persona.BUSINESS),
        ("CL-ask-anything", "Ask anything about your operations", SOURCE_GTM, Persona.BUSINESS),
        ("CL-work-order", "Create a work order from the answer", SOURCE_GTM, Persona.BUSINESS),
        ("CL-read-only", "v1 is read-only; three English templates; citations required", SOURCE_PRD, Persona.PRODUCT),
        ("CL-no-invent", "Inventing an externalId is worse than saying I don't know", SOURCE_ADR_GROUNDING, Persona.TECH),
        ("CL-no-writes", "No write tools registered", SOURCE_ADR_TOOLS, Persona.TECH),
        ("CL-textbox", "Add a text box on Search", SOURCE_TICKETS, Persona.PRODUCT),
        ("CL-file-gaps", "About 40% of demo tenants have no file links to assets", SOURCE_INTERN_NOTE, Persona.TECH),
    ]
    claims: list[Claim] = []
    for claim_id, text, source_id, persona in specs:
        claims.append(
            Claim(
                id=claim_id,
                text=text,
                provenance=provenance,
                source_ids=[source_id] if sourced else [],
                asserted_by=persona,
            )
        )
    return claims


def _intern_view(*, aligned: bool) -> AltitudeView:
    return AltitudeView(
        altitude=Altitude.INTERN,
        summary=(
            "Ticket ATG-12 is not 'add a text box'. It exists because the CXO sentence "
            "'AI that understands the plant' requires grounded retrieval, citations, and "
            "ID honesty. Also: ~40% of demo tenants have no file links to assets."
            if aligned
            else "ATG-12: add a text box on Search. The CXO sentence is not on the ticket."
        ),
        linked_claim_ids=["CL-intent", "CL-no-invent", "CL-file-gaps"] if aligned else ["CL-textbox"],
        linked_contradiction_ids=[FINDING_SL_DOWNWARD_GROUNDING, FINDING_SL_UPWARD_FILE_COVERAGE],
    )


def _cxo_view(*, aligned: bool) -> AltitudeView:
    return AltitudeView(
        altitude=Altitude.CXO,
        summary=(
            "Fund a grounded, read-only v1. We will not promise 'ask anything' or write-from-chat. "
            "Intern finding SL-upward-file-coverage: file links are missing on ~40% of demo tenants — "
            "that is a demo-risk, not polish."
            if aligned
            else "AI that understands the plant. Happy path only. Do not slow the sales cycle."
        ),
        linked_claim_ids=["CL-intent", "CL-read-only"] if aligned else ["CL-intent"],
        linked_contradiction_ids=[FINDING_SL_UPWARD_FILE_COVERAGE] if aligned else [],
        will_promise=["Grounded Q&A on three templates, with citations"] if aligned else ["AI that understands the plant"],
        will_not_promise=(
            [
                "Ask anything about your operations",
                "Create a work order from the answer",
            ]
            if aligned
            else []
        ),
    )


def blocked_complete() -> CanonicalEpic:
    """Honest pre-kickoff state: every planted finding is on the board, status BLOCKED."""

    return CanonicalEpic(
        id=EPIC_ID,
        title=EPIC_TITLE,
        version="v0-blocked",
        intent=EPIC_INTENT,
        declared_status=AlignmentStatus.BLOCKED,
        sources=_source_refs(),
        claims=_claims(sourced=True),
        false_friends=_false_friends(status=FalseFriendStatus.UNDEFINED),
        promise_gaps=[_promise_gap(status=PromiseGapStatus.OPEN)],
        constraints=_constraints(status=ConstraintStatus.ORPHANED, promoted=False),
        contradictions=_contradictions_from_gold(status=BoardItemStatus.OPEN),
        business=BusinessProjection(
            narrative="GTM is already saying ask-anything and write-from-chat.",
            customer_facing_claims=[
                "Ask anything about your operations",
                "Create a work order from the answer",
            ],
            will_not_say=[],
            risks=["Sales cycle demo will over-promise v1"],
            claim_ids=["CL-ask-anything", "CL-work-order"],
        ),
        product=ProductProjection(
            narrative="PRD is three templates, English, read-only, citations required.",
            in_scope=["Three starter templates", "English", "Read-only", "Citations required"],
            out_of_scope=["Write actions", "Work orders", "Languages other than English"],
            acceptance=["If data exists: answer + citation", "If data does not exist: say so"],
            claim_ids=["CL-read-only"],
        ),
        tech=TechProjection(
            narrative="Instances API + file RAG; cluster-local; no write tools.",
            interfaces=["Instances API tool-calling", "File RAG", "No write tools registered"],
            failure_modes=["Invented externalId", "Cross-region model call", "Uncited answer"],
            eval_gates=[
                "I don't know is better than an invented externalId",
                "Every answer has a citation or an explicit miss",
                "p95 < 8s",
            ],
            claim_ids=["CL-no-invent", "CL-no-writes"],
        ),
        intern_view=_intern_view(aligned=False),
        cxo_view=_cxo_view(aligned=False),
        will_not_promise=[],
    )


def false_green() -> CanonicalEpic:
    """Illegal ALIGNED: signatures and a green status while the fight is still on the board."""

    contradictions = _contradictions_from_gold(status=BoardItemStatus.OPEN)
    contradictions = [item for item in contradictions if item.id != FINDING_SL_UPWARD_FILE_COVERAGE]
    return CanonicalEpic(
        id=EPIC_ID,
        title=EPIC_TITLE,
        version="v0-false-green",
        intent=EPIC_INTENT,
        declared_status=AlignmentStatus.ALIGNED,
        sources=_source_refs(),
        claims=_claims(sourced=False),
        false_friends=_false_friends(status=FalseFriendStatus.UNDEFINED),
        promise_gaps=[_promise_gap(status=PromiseGapStatus.OPEN)],
        constraints=_constraints(status=ConstraintStatus.ORPHANED, promoted=False),
        contradictions=contradictions,
        business=BusinessProjection(
            narrative="Looks aligned. Keep the GTM sentences.",
            customer_facing_claims=[
                "Ask anything about your operations",
                "Create a work order from the answer",
            ],
            will_not_say=[],
            risks=[],
            claim_ids=[],
        ),
        product=ProductProjection(
            narrative="MVP is fine.",
            in_scope=["A text box on Search"],
            out_of_scope=["Write actions", "Create a work order from the answer"],
            acceptance=["User can type a question"],
            claim_ids=[],
        ),
        tech=TechProjection(
            narrative="We will figure it out in the sprint.",
            interfaces=["A chat box"],
            failure_modes=[],
            eval_gates=[],
            claim_ids=[],
        ),
        intern_view=_intern_view(aligned=False),
        cxo_view=_cxo_view(aligned=False),
        sign_offs=[
            SignOff(persona=Persona.BUSINESS, signer="Alex Chen (GTM)", epic_version="v0-false-green"),
            SignOff(persona=Persona.PRODUCT, signer="Jordan Blake (PM)", epic_version="v0-false-green"),
            SignOff(persona=Persona.TECH, signer="Priya Mehta (Architect)", epic_version="v0-false-green"),
        ],
        will_not_promise=[],
    )


def legally_aligned() -> CanonicalEpic:
    """Legal ALIGNED after humans priced the gaps. Evals must be able to pass."""

    return CanonicalEpic(
        id=EPIC_ID,
        title=EPIC_TITLE,
        version="v1-signed",
        intent=EPIC_INTENT,
        declared_status=AlignmentStatus.ALIGNED,
        sources=_source_refs(),
        claims=_claims(sourced=True),
        false_friends=_false_friends(status=FalseFriendStatus.DEFINED),
        promise_gaps=[_promise_gap(status=PromiseGapStatus.ACCEPTED_RISK, owner="Alex Chen (GTM)")],
        constraints=_constraints(status=ConstraintStatus.PROMOTED, promoted=True),
        contradictions=_contradictions_from_gold(
            status=BoardItemStatus.ACCEPTED_RISK,
            owner="Jordan Blake (PM)",
        ),
        business=BusinessProjection(
            narrative="v1 is a grounded copilot, not an open-ended plant oracle.",
            customer_facing_claims=["Grounded Q&A on three templates, with citations"],
            will_not_say=[
                "Ask anything about your operations",
                "Create a work order from the answer",
            ],
            risks=["Demo tenants missing file links (~40%)"],
            claim_ids=["CL-read-only"],
        ),
        product=ProductProjection(
            narrative="Three English read-only templates; citations required; no writes.",
            in_scope=["Three starter templates", "English", "Read-only", "Citations required"],
            out_of_scope=["Write actions", "Create a work order from the answer", "Ask anything"],
            acceptance=[
                "If data exists: answer + citation",
                "If data does not exist: say I don't know",
                "Invented externalId is a Sev-1",
            ],
            claim_ids=["CL-read-only", "CL-no-invent"],
        ),
        tech=TechProjection(
            narrative="Cluster-local tool-calling; no write tools; evals on IDs and citations.",
            interfaces=["Instances API tool-calling", "File RAG", "No write tools registered"],
            failure_modes=["Invented externalId", "Cross-region model call", "Uncited answer"],
            eval_gates=[
                "I don't know is better than an invented externalId",
                "Every answer has a citation or an explicit miss",
                "p95 < 8s",
            ],
            claim_ids=["CL-no-invent", "CL-no-writes", "CL-file-gaps"],
        ),
        intern_view=_intern_view(aligned=True),
        cxo_view=_cxo_view(aligned=True),
        sign_offs=[
            SignOff(persona=Persona.BUSINESS, signer="Alex Chen (GTM)", epic_version="v1-signed"),
            SignOff(persona=Persona.PRODUCT, signer="Jordan Blake (PM)", epic_version="v1-signed"),
            SignOff(persona=Persona.TECH, signer="Priya Mehta (Architect)", epic_version="v1-signed"),
        ],
        will_not_promise=[
            "Ask anything about your operations",
            "Create a work order from the answer",
        ],
    )
