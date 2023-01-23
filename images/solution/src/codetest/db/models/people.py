from sqlalchemy import Column, Integer, String, Date, Table
from sqlalchemy.orm import registry
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

mapper_registry = registry()

@mapper_registry.mapped
@dataclass
class People:
    # table name
    __tablename__ = "people"

    # sqlaclchemy metada key
    __sa_dataclass_metadata_key__ = "sa"

    # fields
    id: int = field(init=False, metadata={"sa": Column("id", Integer, primary_key=True, autoincrement="auto", nullable=False)})
    Given_name: Optional[str] = field(default=None, metadata={"sa":  Column("Given_name", String(80), nullable=True)})
    Family_name: Optional[str] = field(default=None, metadata={"sa": Column("Family_name", String(80), nullable=True)})
    Date_of_birth: Optional[date] = field(default=None, metadata={"sa": Column("Date_of_birth", Date, nullable=True)})
    Place_of_birth: Optional[str] = field(default=None, metadata={"sa": Column("Place_of_birth", String(80), nullable=True)})

    def __post_init__(self):
        if not isinstance(self.Given_name, str) and self.Given_name is not None:
            raise TypeError(f"'Given_name' expected type <class string>, but recieved an {type(self.Given_name)} instead")
        if not isinstance(self.Family_name, str) and self.Family_name is not None:
            raise TypeError(f"'Family_name' expected type <class string>, but recieved an {type(self.Family_name)} instead")
        if not isinstance(self.Place_of_birth, str) and self.Place_of_birth is not None:
            raise TypeError(f"'Place_of_birth' expected type <class string>, but recieved an {type(self.Place_of_birth)} instead")
        if not isinstance(self.Date_of_birth, date) and self.Date_of_birth is not None:
            raise TypeError(f"'Date_of_birth' expected type <class datetime.date>, but recieved an {type(self.Date_of_birth)} instead")
        

if __name__ == "__main__":
    data = { 'Given_name':'Jae', 'Family_name': 'Ro', 'Date_of_birth': 'January 23, 2023', 'Place_of_birth': 'Boston' }
    p = People(**data)
    print(p)