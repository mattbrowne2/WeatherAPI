from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    date = Column(Date, index=True)
    min_temp = Column(Float)
    max_temp = Column(Float)
    avg_temp = Column(Float)
    humidity = Column(Float)