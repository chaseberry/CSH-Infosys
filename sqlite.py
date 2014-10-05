from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BetaBriteBase import Base
from BetaBriteUser import *
from BetaBriteSpace import *
import uuid

class sqlite():

    def setup(self):
        global Base
        engine = create_engine('sqlite:///BetaBrite.db')
        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(engine)
        self.sqlSession = session()

    def findOpenSpaces(self, maxCount):
        spaces = self.sqlSession.query(BetaBriteSpace).all()
        count = 0
        validSpaces = []
        for z in range(len(spaces)):
            if count == maxCount:
                return validSpaces
            if not spaces[z].inUse:
                count += 1
                validSpaces.append(spaces[z])
            else:
                count = 0
                validSpaces = []

        return False;

    def registerSpaces(self, maxCount):
        spaces = self.findOpenSpaces(maxCount)
        if spaces == False:
            return False
        key = str(uuid.uuid4())
        user = BetaBriteUser(key=key, fileList=spaces)
        self.sqlSession.add(user)
        for space in spaces:
            space.inUse = True
            space.userId = user

        self.sqlSession.commit()
        return key

if __name__ == '__main__':
    sql = sqlite()
    sql.setup()
    key = sql.registerSpaces(3)
    print(key)
