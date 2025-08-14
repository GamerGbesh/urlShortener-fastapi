from sqlmodel import SQLModel, Field, Session, select
from typing import Optional
import random, string

def generate_random_url(characters = string.ascii_letters + string.digits, size = 8):
    return "".join(random.choice(characters) for _ in range(size))


class Link(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    original_url: str
    url_slug: Optional[str] = Field(nullable=True, unique=True, default=None)

    def save(self, session: Session):
        slug = generate_random_url()

        # Keep generating slug until it's unique
        while session.exec(select(Link).where(Link.url_slug == slug)).first() is not None:
            slug = generate_random_url()
        
        self.url_slug = slug
        session.add(self)
        session.commit()
        session.refresh(self)