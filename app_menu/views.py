from django.shortcuts import render
from django.views.generic import View


class IndexView(View):

    @classmethod
    def get(cls, request, pk=None):
        return render(
            request,
            template_name='index.html'
        )
