class NotFoundError(Exception):
    def __init__(self):
        super().__init__("Club or player not found. Check id's")