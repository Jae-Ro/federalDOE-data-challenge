from sqlalchemy import Column, Integer, String, Date, Table
from sqlalchemy.orm import registry
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

mapper_registry = registry()

@mapper_registry.mapped
@dataclass
class Places:
    # table name
    __tablename__ = "people"

    # sqlaclchemy metada key
    __sa_dataclass_metadata_key__ = "sa"

    # fields
    id: int = field(init=False, metadata={"sa": Column("id", Integer, primary_key=True, autoincrement="auto", nullable=False)})
    City: Optional[str] = field(default=None, metadata={"sa":  Column("City", String(80), nullable=True)})
    County: Optional[str] = field(default=None, metadata={"sa": Column("County", String(80), nullable=True)})
    Country: Optional[str] = field(default=None, metadata={"sa": Column("Country", String(80), nullable=True)})

    def __post_init__(self):
        if not isinstance(self.City, str) and self.City is not None:
            raise TypeError(f"'City' expected type <class string>, but recieved an {type(self.City)} instead")
        if not isinstance(self.County, str) and self.County is not None:
            raise TypeError(f"'County' expected type <class string>, but recieved an {type(self.County)} instead")
        if not isinstance(self.Country, str) and  self.Country is not None:
            raise TypeError(f"'Country' expected type <class string>, but recieved an {type(self.Country)} instead")
        

if __name__ == "__main__":
    data = { 'City':'Boston', 'County': 1, 'Country': "USA" }
    p = Places(**data)
    print(p)