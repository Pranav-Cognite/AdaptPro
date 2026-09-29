import pytest
from pydantic import ValidationError

from adaptpro.fixtures.ask_the_graph import legally_aligned
from adaptpro.schema.models import CanonicalEpic


def test_canonical_epic_rejects_unknown_fields() -> None:
    payload = legally_aligned().model_dump()
    payload["unexpected"] = True
    with pytest.raises(ValidationError):
        CanonicalEpic.model_validate(payload)
