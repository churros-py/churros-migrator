from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str