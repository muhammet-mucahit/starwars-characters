import petl as etl

from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from starwars_apps.characters.service import CollectionService
from starwars_apps.characters.models import Collection


class CollectionsView(ListView):
    """Collections page to list all collections"""

    model = Collection
    template_name = 'characters/collections.html'
    context_object_name = 'collections'

    def get_queryset(self):
        return Collection.objects.order_by('-created')


class CollectionsDetailView(DetailView):
    """Collections detail page to view data inside of specific collection"""

    model = Collection
    template_name = 'characters/collections_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()

        data_size = self.request.GET.get('data_size')
        data_size = int(data_size) if data_size else 10
        context_data.update(
            {
                'filename': self.object.get_filename(),
                'headers': self.object.get_file_table_headers(),
                'data': self.object.get_file_table_data(data_size),
                'load_more_data_size': data_size + 10,
            }
        )
        return context_data


def download_collections_view(request):
    """Download Collection View from StarWars API"""
    CollectionService().download_collection()
    return redirect('characters:collections')


def get_collection_data_view(request, pk):
    """Get Collection Data with load more pagination"""
    collection_obj = get_object_or_404(Collection, pk=pk)
    data = collection_obj.get_file_data()
    return JsonResponse(data=list(etl.dicts(data)), safe=False)
