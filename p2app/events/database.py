# p2app/events/database.py
#
# ICS 33 Fall 2022
# Project 2: Learning to Fly
#
# Events related to the opening and closing of the database.
#
# See the project write-up for details on when these events are sent and by whom.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

from pathlib import Path



class OpenDatabaseEvent:
    def __init__(self, path: Path):
        self._path = path


    def path(self) -> Path:
        return self._path



class CloseDatabaseEvent:
    pass



class DatabaseOpenedEvent:
    def __init__(self, path: Path):
        self._path = path


    def path(self) -> Path:
        return self._path



class DatabaseOpenFailedEvent:
    def __init__(self, reason: str):
        self._reason = reason


    def reason(self) -> str:
        return self._reason



class DatabaseClosedEvent:
    pass
