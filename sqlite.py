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

    def registerSpaceAsText(self,  space, value):
        try:
            space = self.sqlSession.query(BetaBriteSpace).filter_by(fileName=space).one()
        except Exception:
            return False
        space.type = "TEXT"
        space.value = value
        self.sqlSession.commit()
        return True 

    def registerSpaceAsString(self,  space, value):
        try:
            space = self.sqlSession.query(BetaBriteSpace).filter_by(fileName=space).one()
        except Exception:
            return False

        space.type = "STRING"
        space.value = value
        self.sqlSession.commit()
        return True

    def registerSpaceAsPicture(self, space, value):
        try:
            space = self.sqlSession.query(BetaBriteSpace).filter_by(fileName=space).one()
        except Exception:
            return False

        space.type = "PICTURE"
        space.value = value
        self.sqlSession.commit()
        return True 

    def getRegisteredSpaces(self):
        return self.sqlSession.query(BetaBriteSpace).filter(type!=None)

    def deleteSpaces(self, userKey):
        try:
            user = self.sqlSession.query(BetaBriteUser).filter_by(key=userKey).one()
        except Exception as e:
            print(e)
            return False

        spaces = user.fileList
        self.sqlSession.delete(user)
        for space in spaces:
            space.inUse = False
            space.userId = None

        self.sqlSession.commit()
        return True

    def getFileLabels(self, userKey):
        try:
            user = self.sqlSession.query(BetaBriteUser).filter_by(key=userKey).one()
        except Exception as e:
            print(e)
            return False
        
        spaces = user.fileList
        files = []
        for space in spaces:
            files.append(space.fileName)

        return files

    def validUser(self, userKey):
        try:
            user = self.sqlSession.query(BetaBriteUser).filter_by(key=userKey).one()
        except Exception:
            return False
        return True

    def getSpace(self, space):
        try:
            return self.sqlSession.query(BetaBriteSpace).filter_by(fileName=space).one()
        except Exception:
            return None

if __name__ == '__main__':
    pass
