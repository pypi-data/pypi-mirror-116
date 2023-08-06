

class ColonyException(Exception):

    DEAD: int = 1
    LOOP: int = 2

    def __init__(self, code: int = 0, message: str = ''):
        self.code = code
        self.message = message

    @classmethod
    def is_dead(cls):
        return ColonyException(cls.DEAD, 'The colony seems to be DEAD :(')

    @classmethod
    def is_repeated(cls):
        return ColonyException(cls.LOOP, 'The colony seems to repeat its state')

