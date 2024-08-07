from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from index_libri.sanitize import sanitize


class Message(BaseModel):
    message: str


# Schemas da rota Contas


class ContaSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    def sanitize_username(cls, v):
        return sanitize(v)


class ContaPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class ContaList(BaseModel):
    contas: list[ContaPublic]


# Schemas da rota romancistas
class RomancistaPublic(BaseModel):
    id: int
    nome: str


class RomancistaSchema(BaseModel):
    nome: str

    @field_validator('nome')
    def sanitize_nome(cls, v):
        return sanitize(v)


class RomancistaList(BaseModel):
    romancistas: list[RomancistaPublic]


class RomancistaUpdate(BaseModel):
    id: int | None = None
    nome: str | None = None

    @field_validator('nome')
    def sanitize_nome(cls, v):
        return sanitize(v)


# Schemas da rota livro
class LivroPublic(BaseModel):
    titulo: str
    ano: int
    id_romancista: int


class LivroSchema(BaseModel):
    titulo: str
    ano: int
    id_romancista: int

    @field_validator('titulo')
    def sanitize_titulo(cls, v):
        return sanitize(v)


class LivroList(BaseModel):
    livros: list[LivroPublic]


class LivroUpdate(BaseModel):
    id: int | None = None
    titulo: str | None = None
    ano: int | None = None
    id_romancista: int | None = None

    @field_validator('titulo')
    def sanitize_titulo(cls, v):
        return sanitize(v)


# Schemas de autenticação
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
