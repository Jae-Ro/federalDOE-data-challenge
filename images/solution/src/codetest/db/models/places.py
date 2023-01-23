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
    __tablename__ = "places"

    # sqlaclchemy metada key
    __sa_dataclass_metadata_key__ = "sa"

    # fields
    id: int = field(init=False, metadata={"sa": Column("id", Integer, primary_key=True, autoincrement="auto", nullable=False)})
    city: Optional[str] = field(default=None, metadata={"sa":  Column("city", String(80), nullable=True)})
    county: Optional[str] = field(default=None, metadata={"sa": Column("county", String(80), nullable=True)})
    country: Optional[str] = field(default=None, metadata={"sa": Column("country", String(80), nullable=True)})

    def __post_init__(self):
        if not isinstance(self.city, str) and self.city is not None:
            raise TypeError(f"'city' expected type <class string>, but recieved an {type(self.city)} instead")
        if not isinstance(self.county, str) and self.county is not None:
            raise TypeError(f"'county' expected type <class string>, but recieved an {type(self.county)} instead")
        if not isinstance(self.country, str) and  self.country is not None:
            raise TypeError(f"'country' expected type <class string>, but recieved an {type(self.country)} instead")
        

if __name__ == "__main__":
    data = { 'city':'Boston', 'county': 1, 'country': "United States" }
    p = Places(**data)
    print(p)