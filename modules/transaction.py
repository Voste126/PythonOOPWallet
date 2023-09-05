from sqlalchemy import Column, Integer, String,Float, ForeignKey
from sqlalchemy.orm import relationship
from modules.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String)
    amount= Column(Float)
    portfolio_id = Column(Integer,ForeignKey('portfolios.id'))
    #establishing the relatonship between the portfolio and transaction tables 
    portfolio = relationship("Portfolio", back_populates="transactions")