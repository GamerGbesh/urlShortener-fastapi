from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from sqlmodel import select
from pydantic import BaseModel
from sqlmodel import Session, create_engine, SQLModel
import models
from models import Link

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Lifespan is used to as a event listener for when the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("Database has been created")
    yield

app = FastAPI(lifespan=lifespan)

class CreateUrl(BaseModel):
    """Request body for creating a new url"""
    original_url: str

@app.post("/create", response_model=models.Link)
async def create(url: CreateUrl):
    with Session(engine) as session:
        link: Link = Link(original_url=url.original_url)
        # Custom saving logic which is defined in the Link class
        link.save(session)
    return link

@app.get("/{slug}")
async def get_url(slug: str):
    statement = select(Link).where(Link.url_slug == slug)
    with Session(engine) as session:
        result = session.exec(statement=statement).first()
        if not result:
            return {"error": "URL not found"}
        return RedirectResponse(url=result.original_url)