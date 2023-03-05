import abc
import petl as etl
import requests

from typing import List, Dict

from django.conf import settings


class PaginatedDataFetchMixin:
    def get_all_paginated_data(self, url: str) -> List[Dict]:
        """Get all paginated data"""
        all_data = []
        has_next_page = True
        while has_next_page:
            response = requests.get(url)
            json_data = response.json()
            all_data.extend(list(json_data['results']))
            if bool(json_data['next']):
                url = json_data['next']
            else:
                has_next_page = False

        return all_data


class StarWarsService(PaginatedDataFetchMixin):
    URL_KEY = None

    URLS = {
        'people': 'https://swapi.dev/api/people',
        'planets': 'https://swapi.dev/api/planets',
    }

    def __init__(self):
        if self.URL_KEY not in self.URLS:
            raise KeyError(f"The url_key {self.URL_KEY} is not exists!")
        self.url = self.URLS[self.URL_KEY]

    def get_all_data(self):
        return self.get_all_paginated_data(url=self.url)


class PeopleService(StarWarsService):
    URL_KEY = 'people'

    def __init__(self):
        super().__init__()
        self.planet_service = PlanetsService()

    def extract_data(self, data: List[Dict]):
        return etl.fromdicts(data)

    def transform_data(self, table):
        # Add a date column (%Y-%m-%d) based on edited date
        table = etl.addfield(table, 'edited', lambda record: record['edited'].split('T')[0])

        # Resolve the homeworld field into the homeworld's name
        planet_names_dictionary = self.planet_service.get_planet_names_dictionary()
        table = etl.convert(table, 'homeworld', lambda record: planet_names_dictionary.get(record))

        # Drop redundant fields
        table = etl.cutout(table, 'films', 'species', 'vehicles', 'starships', 'created', 'edited', 'url')

        return table

    def export_data(self, filename: str) -> str:
        all_data = self.get_all_paginated_data(self.url)

        extracted_data = self.extract_data(all_data)
        transformed_data = self.transform_data(extracted_data)

        filepath = str(settings.COLLECTION_FILES_DIRECTORY.joinpath(filename))

        etl.tocsv(transformed_data, filepath)

        return filepath


class PlanetsService(StarWarsService):
    URL_KEY = 'planets'

    def get_planet_names_dictionary(self):
        all_data = self.get_all_data()
        return {data['url']: data['name'] for data in all_data}
