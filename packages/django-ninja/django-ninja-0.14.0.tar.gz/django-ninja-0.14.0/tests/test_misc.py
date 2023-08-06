import pytest
from pydantic import BaseModel
from ninja import NinjaAPI
from ninja.testing import TestClient
from ninja.signature.details import is_pydantic_model


def test_is_pydantic_model():
    class Model(BaseModel):
        x: int

    assert is_pydantic_model(Model)
    assert is_pydantic_model("instance") is False


def test_client():
    "covering evertying in testclient (includeing invalid paths)"
    api = NinjaAPI()
    client = TestClient(api)
    with pytest.raises(Exception):
        response = client.get("/404")


def test_kwargs():
    api = NinjaAPI()

    @api.get("/")
    def operation(request, a: str, *args, **kwargs):
        pass

    schema = api.get_openapi_schema()
    params = schema["paths"]["/api/"]["get"]["parameters"]
    print(params)
    assert params == [  # Only `a` should be here, not kwargs
        {
            "in": "query",
            "name": "a",
            "schema": {"title": "A", "type": "string"},
            "required": True,
        }
    ]
