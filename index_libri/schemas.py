from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class ContaSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class ContaPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class ContaDB(ContaSchema):
    id: int


class ContaList(BaseModel):
    contas: list[ContaPublic]
