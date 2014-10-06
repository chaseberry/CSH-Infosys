from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from BetaBriteBase import Base

class BetaBriteSpace(Base):
    __tablename__ = 'BetaBriteSpace'
    id = Column(Integer, primary_key=True)
    inUse = Column(Boolean, default=False)
    fileName = Column(String) 
    userId = Column(Integer, ForeignKey('BetaBriteUser.id'))
    type = Column(String)
    value = Column(String)
