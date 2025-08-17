import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from .main import app, get_session
from .models import Link


path = "./test.db"
TEST_DATABASE_URL = f"sqlite:///{path}"

test_engine = create_engine(
    TEST_DATABASE_URL,
    echo=True,
)

def get_test_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)

client = TestClient(app)


def test_create():
    response = client.post("/create", json={
                "original_url": "https://example.com"
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["original_url"] == "https://example.com"
    assert data["url_slug"] is not None
    assert data["clicks"] == 0

    slug = data["url_slug"]
    redirect_response = client.get(f"/{slug}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://example.com"

    info_response = client.get(f"/info/{slug}")
    assert info_response.status_code == 200
    info_data = info_response.json()
    assert info_data["clicks"] == 1

def test_not_found_redirect():
    response = client.get("/nonexistent", follow_redirects=False)
    assert response.status_code == 200
    assert response.json() == {"error": "URL not found"}