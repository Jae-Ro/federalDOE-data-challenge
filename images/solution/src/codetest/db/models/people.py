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
    given_name: Optional[str] = field(default=None, metadata={"sa":  Column("given_name", String(80), nullable=True)})
    family_name: Optional[str] = field(default=None, metadata={"sa": Column("family_name", String(80), nullable=True)})
    date_of_birth: Optional[date] = field(default=None, metadata={"sa": Column("date_of_birth", Date, nullable=True)})
    place_of_birth: Optional[str] = field(default=None, metadata={"sa": Column("place_of_birth", String(80), nullable=True)})

    def __post_init__(self):
        if not isinstance(self.given_name, str) and self.given_name is not None:
            raise TypeError(f"'given_name' expected type <class string>, but recieved an {type(self.given_name)} instead")
        if not isinstance(self.family_name, str) and self.family_name is not None:
            raise TypeError(f"'family_name' expected type <class string>, but recieved an {type(self.family_name)} instead")
        if not isinstance(self.place_of_birth, str) and self.place_of_birth is not None:
            raise TypeError(f"'place_of_birth' expected type <class string>, but recieved an {type(self.place_of_birth)} instead")
        if not isinstance(self.date_of_birth, date) and self.date_of_birth is not None:
            raise TypeError(f"'date_of_birth' expected type <class datetime.date>, but recieved an {type(self.date_of_birth)} instead")
        

if __name__ == "__main__":
    data = { 'given_name':'Jae', 'family_name': 'Ro', 'date_of_birth': 'January 23, 2023', 'place_of_birth': 'Boston' }
    p = People(**data)
    print(p)