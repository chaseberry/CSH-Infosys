from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BetaBriteBase import Base
from BetaBriteUser import *
from BetaBriteSpace import *
import uuid

class sqlite():
    '''A class containing functions to interact with the sqlite db'''
 
    def setup(self):
        '''Sets up the sqlite DB'''
        global Base
        engine = create_engine('sqlite:///BetaBrite.db', connect_args={'check_same_thread':False})
        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(engine)
        self.sqlSession = session()

    def findOpenSpaces(self, maxCount):
        '''Finds the unused spaces for user registration
            This will find maxCount files in sequential order. I had a reason for that, I dont remember why'''
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
        '''Register maxCount spaces to a new user and return the users KEY'''
        spaces = self.findOpenSpaces(maxCount)#gets the spaces
        if spaces == False:
            return False
        key = str(uuid.uuid4())#Generates the key for the user
        user = BetaBriteUser(key=key, fileList=spaces)
        self.sqlSession.add(user)
        for space in spaces:
            space.inUse = True
            space.userId = user

        self.sqlSession.commit()
        return key

    def registerSpaceAsText(self,  space, value):
        '''Register the space as a text type'''
        try:
            space = self.sqlSession.query(BetaBriteSpace).filter_by(fileName=space).one()#find a single space
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
        '''Register the space as a string type'''
        try:
            space = self.sqlSession.query(BetaBriteSpace).filter_by(fileName=space).one()
        except Exception:
            return False

        space.type = "PICTURE"
        space.value = value
        self.sqlSession.commit()
        return True 

    def getUsedSpaces(self):
        '''gets all spaces that don't have a type(these are unsued)'''
        return self.sqlSession.query(BetaBriteSpace).filter(type!=None)

    def deleteSpaces(self, userKey):
        '''removes the spaces registered to a specific key'''
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
            space.type = None
            space.value = None
        self.sqlSession.commit()
        return True

    def getFileLabels(self, userKey):
        '''Get all file labels from a key'''
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
        '''Finds if the key cooresponds to a valid user'''
        try:
            user = self.sqlSession.query(BetaBriteUser).filter_by(key=userKey).one()
        except Exception:
            return False
        return True

    def getSpace(self, space):
        '''Gets data stored at a specific space'''
        try:
            return self.sqlSession.query(BetaBriteSpace).filter_by(fileName=space).one()
        except Exception:
            return None

    def getTextandOtherSpaces(self):
        '''Get all spaces that are text. Then all spaces that are String or Picture'''
        text = self.sqlSession.query(BetaBriteSpace).filter_by(type='TEXT')
        other = self.sqlSession.query(BetaBriteSpace).filter(type!='TEXT', type!=None)
        return [text, other]

    def getUsers(self):
        '''Gets all users and returns an array of key to fileList arrays'''
        userList = []
        users = self.sqlSession.query(BetaBriteUser).all()
        for user in users:
            files = []
            for space in user.fileList:
                files.append(space.fileName)
            userList.append('key: ' + user.key + '   spaces:' + str(files))

        return userList
if __name__ == '__main__':
    sqlite = sqlite()
    sqlite.setup()
    print(sqlite.getUsers())
