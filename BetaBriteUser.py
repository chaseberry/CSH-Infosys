from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from BetaBriteBase import Base

class BetaBriteUser(Base):
    __tablename__ = 'BetaBriteUser'
    id = Column(Integer, primary_key=True)
    key = Column(String)
    fileList = relationship('BetaBriteSpace')
