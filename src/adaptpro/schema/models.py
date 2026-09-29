from pydantic import BaseModel, ConfigDict, Field

from adaptpro.schema.enums import (
    AlignmentStatus,
    Altitude,
    BoardItemStatus,
    ClaimProvenance,
    ConstraintStatus,
    FailureMode,
    FalseFriendStatus,
    Persona,
    PromiseGapStatus,
    SourceKind,
)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SourceRef(StrictModel):
    id: str
    title: str
    kind: SourceKind
    filename: str
    persona_owner: Persona


class Claim(StrictModel):
    id: str
    text: str
    provenance: ClaimProvenance
    source_ids: list[str] = Field(default_factory=list)
    asserted_by: Persona | None = None


class FalseFriend(StrictModel):
    id: str
    phrase: str
    business_meaning: str
    product_meaning: str
    tech_meaning: str
    chosen_meaning: str | None = None
    status: FalseFriendStatus = FalseFriendStatus.UNDEFINED


class PromiseGap(StrictModel):
    id: str
    promised_text: str
    scoped_text: str
    buildable_text: str
    promised_source_id: str
    scoped_source_id: str
    buildable_source_id: str
    owner: str | None = None
    status: PromiseGapStatus = PromiseGapStatus.OPEN


class Constraint(StrictModel):
    id: str
    text: str
    tech_source_id: str
    appears_in_product: bool = False
    appears_in_business: bool = False
    owner: str | None = None
    status: ConstraintStatus = ConstraintStatus.ORPHANED


class Contradiction(StrictModel):
    id: str
    failure_mode: FailureMode
    title: str
    summary: str
    source_ids: list[str]
    status: BoardItemStatus = BoardItemStatus.OPEN
    owner: str | None = None
    waiver_reason: str | None = None


class BusinessProjection(StrictModel):
    narrative: str
    customer_facing_claims: list[str]
    will_not_say: list[str]
    risks: list[str]
    claim_ids: list[str] = Field(default_factory=list)


class ProductProjection(StrictModel):
    narrative: str
    in_scope: list[str]
    out_of_scope: list[str]
    acceptance: list[str]
    claim_ids: list[str] = Field(default_factory=list)


class TechProjection(StrictModel):
    narrative: str
    interfaces: list[str]
    failure_modes: list[str]
    eval_gates: list[str]
    claim_ids: list[str] = Field(default_factory=list)


class AltitudeView(StrictModel):
    altitude: Altitude
    summary: str
    linked_claim_ids: list[str] = Field(default_factory=list)
    linked_contradiction_ids: list[str] = Field(default_factory=list)
    will_promise: list[str] = Field(default_factory=list)
    will_not_promise: list[str] = Field(default_factory=list)


class SignOff(StrictModel):
    persona: Persona
    signer: str
    epic_version: str


class Waiver(StrictModel):
    contradiction_id: str
    signer: str
    persona: Persona
    reason: str
    epic_version: str


class CanonicalEpic(StrictModel):
    """The one versioned object. Declared alignment is a claim; evals decide if it is legal."""

    id: str
    title: str
    version: str
    intent: str
    declared_status: AlignmentStatus
    sources: list[SourceRef]
    claims: list[Claim]
    false_friends: list[FalseFriend]
    promise_gaps: list[PromiseGap]
    constraints: list[Constraint]
    contradictions: list[Contradiction]
    business: BusinessProjection
    product: ProductProjection
    tech: TechProjection
    intern_view: AltitudeView
    cxo_view: AltitudeView
    sign_offs: list[SignOff] = Field(default_factory=list)
    waivers: list[Waiver] = Field(default_factory=list)
    will_not_promise: list[str] = Field(default_factory=list)
