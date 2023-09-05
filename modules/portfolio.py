from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from modules.database import Base

class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    #establish the relationship betwen the user module and also transaction
    owner = relationship("User", back_populates="portfolios")
    transactions = relationship("Transaction", back_populates='portfolio')
    