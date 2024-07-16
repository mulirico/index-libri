from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


# Schemas da rota Contas


class ContaSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


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


class RomancistaList(BaseModel):
    romancistas: list[RomancistaPublic]


# Schemas de autenticação
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
