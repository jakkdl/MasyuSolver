class MasyuException(Exception):
    '''Base class for all solver exceptions'''

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return(self.msg)

class MasyuSolverException(MasyuException):
    '''Exception encountered during the solving process'''

    def __init__(self, msg, location):
        super().__init__(msg)
        self.location = location    # this is a tuple

    def __str__(self):
        return(self.msg + " : " + repr(self.location))

class MasyuFileSaveException(MasyuException):
    '''Exception encountered during saving of a file'''

    def __init__(self, msg):
        super().__init__(msg)

class MasyuFileOpenException(MasyuException):
    '''Exception encountered during opening of a file'''

    def __init__(self, msg):
        super().__init__(msg)

class MasyuInvalidPuzzleFileException(MasyuException):
    '''Exception encountered during the processing of a puzzle board file'''

    def __init__(self, msg):
        super().__init__(msg)
