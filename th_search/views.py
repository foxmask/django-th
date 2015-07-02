from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from th_search.forms import TriggerHappySearchForm


class TriggerHappySearchView(SearchView):
    template_name = 'search.html'
    searchqueryset = SearchQuerySet().all(),
    form_class = TriggerHappySearchForm

    def get_queryset(self):
        queryset = super(TriggerHappySearchView, self).get_queryset()
        return queryset.filter(user=self.request.user.id)
