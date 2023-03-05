import os

from django.conf import settings
from django.db import models

import petl as etl
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Collection(models.Model):
    filepath = models.FilePathField(path=settings.COLLECTION_FILES_DIRECTORY)
    created = models.DateTimeField(auto_now_add=True)

    def get_filename(self):
        base_path = f"{str(settings.COLLECTION_FILES_DIRECTORY)}/"
        return self.filepath.removeprefix(base_path)

    def get_file_data(self):
        return etl.fromcsv(self.filepath)

    def get_file_table_headers(self):
        return self.get_file_data()[0]

    def get_file_table_data(self, data_size: int = 10):
        initial = 1
        return self.get_file_data()[initial:initial + data_size]


@receiver(post_delete, sender=Collection)
def remove_file(sender, instance: Collection, *args, **kwargs):
    # Remove file when a Collection object is deleted
    if os.path.exists(instance.filepath):
        os.remove(instance.filepath)
