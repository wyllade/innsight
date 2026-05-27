import json
from sqlalchemy import Column, Integer, String, Text, Float
from app.database import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    city = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    price_per_night = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    rating = Column(Float, default=4.5)
    _amenities = Column("amenities", Text, default="[]") 

    @property
    def amenities(self):
        return json.loads(self._amenities)

    @amenities.setter
    def amenities(self, value):
        self._amenities = json.dumps(value)
