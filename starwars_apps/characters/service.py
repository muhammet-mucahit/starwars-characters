from django.conf import settings
from django.db import transaction

from starwars_apps.characters.models import Collection
from starwars_apps.core.service import PeopleService


class CollectionService:
    def __init__(self):
        self.people_service = PeopleService()

    @transaction.atomic()
    def download_collection(self):
        collection_obj = Collection.objects.create()

        collection_created_str = collection_obj.created.strftime("%d-%m-%Y_%H:%M:%S")
        filename = f"{settings.COLLECTION_FILE_PREFIX}_{collection_created_str}.csv"
        filepath = self.people_service.export_data(filename=filename)

        collection_obj.filepath = filepath
        collection_obj.save()
