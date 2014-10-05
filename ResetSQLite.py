from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BetaBriteUser import *
from BetaBriteSpace import *
import os

if __name__ == '__main__':
    if os.path.isfile('BetaBrite.db'):
        os.remove('BetaBrite.db')
    engine = create_engine('sqlite:///BetaBrite.db')
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
    s = session()

    for z in range(1, 95):
        s.add(BetaBriteSpace(fileName=str(z)))

    s.commit()
    s.close
