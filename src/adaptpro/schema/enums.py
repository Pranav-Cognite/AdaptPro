from enum import StrEnum


class Persona(StrEnum):
    BUSINESS = "business"
    PRODUCT = "product"
    TECH = "tech"


class Altitude(StrEnum):
    INTERN = "intern"
    IC = "ic"
    LEAD = "lead"
    DIRECTOR = "director"
    CXO = "cxo"


class AlignmentStatus(StrEnum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    BLOCKED = "blocked"
    ALIGNED = "aligned"


class FailureMode(StrEnum):
    FALSE_FRIEND = "false_friend"
    UNPRICED_PROMISE = "unpriced_promise"
    ORPHANED_CONSTRAINT = "orphaned_constraint"
    ARTIFACT_SILO = "artifact_silo"
    SENIORITY_LOSSY = "seniority_lossy"


class SourceKind(StrEnum):
    CXO_SLIDE = "cxo_slide"
    GTM = "gtm"
    PRD = "prd"
    ADR = "adr"
    TICKET = "ticket"
    INTERN_NOTE = "intern_note"
    SLACK = "slack"


class ClaimProvenance(StrEnum):
    SOURCED = "sourced"
    UNSOURCED = "unsourced"
    PROPOSAL = "proposal"


class BoardItemStatus(StrEnum):
    OPEN = "open"
    RESOLVED = "resolved"
    ACCEPTED_RISK = "accepted_risk"


class FalseFriendStatus(StrEnum):
    UNDEFINED = "undefined"
    DEFINED = "defined"


class ConstraintStatus(StrEnum):
    ORPHANED = "orphaned"
    PROMOTED = "promoted"
    WAIVED = "waived"


class PromiseGapStatus(StrEnum):
    OPEN = "open"
    RESOLVED = "resolved"
    ACCEPTED_RISK = "accepted_risk"
