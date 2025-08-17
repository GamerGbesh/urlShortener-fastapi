from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from sqlmodel import select
from pydantic import BaseModel
from sqlmodel import Session, create_engine, SQLModel
from .models import Link

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# Lifespan is used as an event listener for when the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("Database has been created")
    yield

app = FastAPI(lifespan=lifespan)

class CreateUrl(BaseModel):
    """Request body for creating a new url"""
    original_url: str

@app.post("/create", response_model=Link)
async def create(url: CreateUrl, session: Session = Depends(get_session)):
    link: Link = Link(original_url=url.original_url)
    # Custom saving logic which is defined in the Link class
    link.save(session)
    return link

@app.get("/{slug}")
async def get_url(slug: str, session: Session = Depends(get_session)):
    statement = select(Link).where(Link.url_slug == slug)
    result = session.exec(statement=statement).first()
    if not result:
        return {"error": "URL not found"}
    return RedirectResponse(url=result.original_url)