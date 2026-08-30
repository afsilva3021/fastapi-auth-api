from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from api.database.base import Base

class Usuario(Base):

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False
    )


    senha: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )