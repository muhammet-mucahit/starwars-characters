from django.urls import path

from starwars_apps.characters.views import (
    CollectionsView,
    CollectionsDetailView,
    download_collections_view,
    get_collection_data_view,
)

app_name = 'characters'

urlpatterns = [
    path('collections/', CollectionsView.as_view(), name='collections'),
    path('collections/<int:pk>', CollectionsDetailView.as_view(), name='collections-detail'),
    path('collections/<int:pk>/data', get_collection_data_view, name='collections-detail-data'),
    path('collections/download', download_collections_view, name='collections-download'),
]
