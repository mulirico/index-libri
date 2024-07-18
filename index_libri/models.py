from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]


@table_registry.mapped_as_dataclass
class Romancista:
    __tablename__ = 'romancista'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)
    livros: Mapped[list['Livro']] = relationship(
        init=False,
        back_populates='romancista',
        cascade='all, delete-orphan',
    )


@table_registry.mapped_as_dataclass
class Livro:
    __tablename__ = 'livro'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    titulo: Mapped[str] = mapped_column(unique=True)
    ano: Mapped[int]

    id_romancista: Mapped[int] = mapped_column(ForeignKey('romancista.id'))

    romancista: Mapped[Romancista] = relationship(
        init=False, back_populates='livros'
    )
