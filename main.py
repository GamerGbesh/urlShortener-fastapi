from fastapi import Depends, FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse, JSONResponse
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

@app.post("/create", response_model=Link, status_code=status.HTTP_201_CREATED)
async def create(url: CreateUrl, session: Session = Depends(get_session)):
    link: Link = Link(original_url=url.original_url)
    # Custom saving logic which is defined in the Link class
    link.save(session)
    return link

@app.get("/info/{slug}")
async def get_info(slug: str, session: Session = Depends(get_session)):
    statement = select(Link).where(Link.url_slug == slug)
    result = session.exec(statement=statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="URL not found")
    return result

@app.get("/{slug}")
async def get_url(slug: str, session: Session = Depends(get_session)):
    statement = select(Link).where(Link.url_slug == slug)
    result = session.exec(statement=statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="URL not found")
    # This was done to keep track of the number of times a specific shortened url was clicked
    result.clicks += 1
    session.add(result)
    session.commit()
    session.refresh(result)
    return RedirectResponse(url=result.original_url)

