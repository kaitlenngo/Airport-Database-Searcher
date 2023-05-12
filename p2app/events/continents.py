# p2app/events/continents.py
#
# ICS 33 Fall 2022
# Project 2: Learning to Fly
#
# Events that are either related to searching for, creating, or editing continents
# in the database.
#
# See the project write-up for details on when these events are sent and by whom.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

from collections import namedtuple



Continent = namedtuple('Continent', ['continent_id', 'continent_code', 'name'])

Continent.__annotations__ = {
    'continent_id': str | None,
    'continent_code': str | None,
    'name': str | None
}



class StartContinentSearchEvent:
    def __init__(self, continent_code: str, name: str):
        self._continent_code = continent_code
        self._name = name


    def continent_code(self) -> str:
        return self._continent_code


    def name(self) -> str:
        return self._name



class ContinentSearchResultEvent:
    def __init__(self, continent: Continent):
        self._continent = continent


    def continent(self) -> Continent:
        return self._continent



class LoadContinentEvent:
    def __init__(self, continent_id: int):
        self._continent_id = continent_id


    def continent_id(self) -> int:
        return self._continent_id



class ContinentLoadedEvent:
    def __init__(self, continent: Continent):
        self._continent = continent


    def continent(self) -> Continent:
        return self._continent



class SaveNewContinentEvent:
    def __init__(self, continent: Continent):
        self._continent = continent


    def continent(self) -> Continent:
        return self._continent



class SaveContinentEvent:
    def __init__(self, continent: Continent):
        self._continent = continent


    def continent(self) -> Continent:
        return self._continent



class ContinentSavedEvent:
    def __init__(self, continent: Continent):
        self._continent = continent


    def continent(self) -> Continent:
        return self._continent



class SaveContinentFailedEvent:
    def __init__(self, reason: str):
        self._reason = reason


    def reason(self) -> str:
        return self._reason
