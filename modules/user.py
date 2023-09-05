# user.py
import pytz
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# Define the East African Time (EAT) timezone
eat_timezone = pytz.timezone('Africa/Nairobi')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    registration_date = Column(DateTime, default=lambda: datetime.now(eat_timezone))

    # Establish the relationship between the user and portfolios
    portfolios = relationship("Portfolio", back_populates='owner')

    