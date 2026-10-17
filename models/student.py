from sqlmodel import SQLModel, Field

class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    semester: str
    active: bool = True