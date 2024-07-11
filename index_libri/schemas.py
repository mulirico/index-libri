from pydantic import BaseModel, ConfigDict, EmailStr


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
    model_config = ConfigDict(from_attributes=True)


class ContaList(BaseModel):
    contas: list[ContaPublic]
