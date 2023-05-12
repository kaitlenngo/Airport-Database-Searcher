# p2app/engine/main.py
#
# ICS 33 Fall 2022
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.
import sqlite3
import p2app.events.continents as continents
import p2app.events.app as app
import p2app.events.database as database
import p2app.events.countries as countries
import p2app.events.regions as regions


class Engine:  #
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.connection = None

    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        if type(event) == app.QuitInitiatedEvent:
            self.connection.commit()
            self.connection.close()
            yield app.EndApplicationEvent()
        elif type(event) == database.OpenDatabaseEvent:
            try:
                self.connection = sqlite3.connect(event.path())
                yield database.DatabaseOpenedEvent(event.path())
            except:
                yield database.DatabaseOpenFailedEvent('Failed to open database.')
        elif type(event) == database.CloseDatabaseEvent:
            yield database.DatabaseClosedEvent()

        elif type(event) == continents.StartContinentSearchEvent:
            cursor = self.connection.execute(f"SELECT continent_id FROM continent WHERE continent_code = '{event.continent_code()}' OR name = '{event.name()}'")
            while True:
                result = cursor.fetchone()
                if result is None:
                    break
                else:
                    value = continents.Continent(result[0], event.continent_code(), event.name())
                    yield continents.ContinentSearchResultEvent(value)
        elif type(event) == continents.LoadContinentEvent:
            cursor = self.connection.execute(f'SELECT * FROM continent WHERE continent_id = {event.continent_id()}')
            while True:
                result = cursor.fetchone()
                if result is None:
                    break
                else:
                    value = continents.Continent(result[0], result[1], result[2])
                    yield continents.ContinentLoadedEvent(value)
        elif type(event) == continents.SaveNewContinentEvent:
            try:
                cursor1 = self.connection.execute(f"SELECT * FROM continent ORDER BY continent_id DESC LIMIT 1")
                result = cursor1.fetchone()
                cursor2 = self.connection.execute(f"INSERT INTO continent (continent_id, continent_code, name) VALUES ({result[0] + 1}, '{event.continent().continent_code}', '{event.continent().name}')")
                yield continents.ContinentSavedEvent(event.continent())
            except:
                yield continents.SaveContinentFailedEvent('Failed to save new continent.')
        elif type(event) == continents.SaveContinentEvent:
            try:
                cursor = self.connection.execute(f"UPDATE continent SET continent_code = '{event.continent().continent_code}', name = '{event.continent().name}' WHERE continent_id = {event.continent().continent_id}")
                yield continents.ContinentSavedEvent(event.continent())
            except:
                yield continents.SaveContinentFailedEvent('Failed to save new continent.')

        elif type(event) == countries.StartCountrySearchEvent:
            cursor = self.connection.execute(f"SELECT * FROM country WHERE country_code = '{event.country_code()}' OR name = '{event.name()}'")
            while True:
                result = cursor.fetchone()
                if result is None:
                    break
                else:
                    value = countries.Country(result[0], result[1], result[2], result[3], result[4], result[5])
                    yield countries.CountrySearchResultEvent(value)
        elif type(event) == countries.LoadCountryEvent:
            cursor = self.connection.execute(f"SELECT * FROM country WHERE country_id = {event.country_id()}")
            while True:
                result = cursor.fetchone()
                if result is None:
                    break
                else:
                    value = countries.Country(result[0], result[1], result[2], result[3], result[4], result[5])
                    yield countries.CountryLoadedEvent(value)
        elif type(event) == countries.SaveNewCountryEvent:
            try:
                cursor1 = self.connection.execute(f"SELECT * FROM country ORDER BY country_id DESC LIMIT 1")
                result = cursor1.fetchone()
                cursor2 = self.connection.execute(f"INSERT INTO country (country_id, country_code, name, continent_id, wikipedia_link, keywords) VALUES ({result[0] + 1}, '{event.country().country_code}', '{event.country().name}', '{event.country().continent_id}', '{event.country().wikipedia_link}', '{event.country().keywords}')")
                yield countries.CountrySavedEvent(event.country())
            except:
                yield continents.SaveContinentFailedEvent('Failed to save new country.')
        elif type(event) == countries.SaveCountryEvent:
            try:
                cursor = self.connection.execute(f"UPDATE country SET country_code = '{event.country().country_code}', name = '{event.country().name}', continent_id = {event.country().continent_id}, wikipedia_link = '{event.country().wikipedia_link}', keywords = '{event.country().keywords}' WHERE country_id = {event.country().country_id}")
                yield countries.CountrySavedEvent(event.country())
            except:
                yield countries.SaveCountryFailedEvent('Failed to save new country.')

        elif type(event) == regions.StartRegionSearchEvent:
            cursor = self.connection.execute(f"SELECT * FROM region WHERE region_code = '{event.region_code()}' OR local_code = '{event.local_code()}' OR name = '{event.name()}'")
            while True:
                result = cursor.fetchone()
                if result is None:
                    break
                else:
                    value = regions.Region(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
                    yield regions.RegionSearchResultEvent(value)
        elif type(event) == regions.LoadRegionEvent:
            cursor = self.connection.execute(f'SELECT * FROM region WHERE region_id = {event.region_id()}')
            while True:
                result = cursor.fetchone()
                if result is None:
                    break
                else:
                    value = regions.Region(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
                    yield regions.RegionLoadedEvent(value)
        elif type(event) == regions.SaveNewRegionEvent:
            try:
                cursor1 = self.connection.execute(f"SELECT * FROM region ORDER BY region_id DESC LIMIT 1")
                result = cursor1.fetchone()
                cursor2 = self.connection.execute(f"INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES ({result[0] + 1}, '{event.region().region_code}', '{event.region().local_code}', '{event.region().name}', {event.region().continent_id}, {event.region().country_id}, '{event.region().wikipedia_link}', '{event.region().keywords}')")
                yield regions.RegionSavedEvent(event.region())
            except:
                yield regions.SaveRegionFailedEvent('Failed to save new region.')
        elif type(event) == regions.SaveRegionEvent:
            try:
                cursor = self.connection.execute(f"UPDATE region SET region_code = '{event.region().region_code}', local_code = '{event.region().local_code}', name = '{event.region().name}', continent_id = {event.region().continent_id}, country_id = {event.region().country_id}, wikipedia_link = '{event.region().wikipedia_link}', keywords = '{event.region().keywords}' WHERE region_id = {event.region().region_id}")
                yield regions.RegionSavedEvent(event.region())
            except:
                yield regions.SaveRegionFailedEvent('Failed to save new region.')
