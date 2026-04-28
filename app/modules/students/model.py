from datetime import datetime
import uuid
from sqlalchemy import String, Integer, Column, DateTime, Float, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship , Mapped, mapped_column

from app.models.base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)