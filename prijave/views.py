from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

from django.views.generic import ListView, DetailView, CreateView, DeleteView
from prijave.models import Poziv

class PozivCreateView(CreateView):
    model = Poziv
    template_name = 'prijave_create.html'
    success_url = '/'

    fields = ['lokacija', 'opis', 'kolicina_pomoci']

    def get(self, request, *args, **kwargs):
        # we can't let them create multiple entries
        if(request.COOKIES.get('pokretac')):
            return HttpResponseRedirect('/')
        else:
            return super(PozivCreateView, self).get(request, args, kwargs)

    def form_valid(self, form):
        response = super(PozivCreateView, self).form_valid(form)
        response.set_cookie('pokretac',
                            self.object.pk,
                            expires = datetime.now() + timedelta(hours = 2))

        return response


class PozivDeleteView(DeleteView):
    model = Poziv
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if(request.COOKIES.get('pokretac')):
            response = super(PozivDeleteView, self).post(request, args, kwargs)
            response.delete_cookie('pokretac')

            return response
        else:
            raise Http404


def gateway(request):
    prijavljen = request.COOKIES.get('prijavljen')
    pokretac = request.COOKIES.get('pokretac')

    if(prijavljen):
        response = DetailView.as_view(model = Poziv,
                                      template_name = 'prijave_detail.html',
                                      context_object_name = 'poziv')(request,
                                                                pk = prijavljen)
        return response

    elif(pokretac):
        response = DetailView.as_view(model = Poziv,
                                      template_name = 'prijave_pregled.html',
                                      context_object_name = 'poziv')(request,
                                                                pk = pokretac)
        return response

    else:
        response = ListView.as_view(model = Poziv,
                                    template_name = 'prijave_list.html',
                                    context_object_name = 'pozivi')(request)
        return response


def dolazim(request, pk):
    prijavljen = request.COOKIES.get('prijavljen')

    response = HttpResponseRedirect('/')

    if(not prijavljen):
        poziv = Poziv.objects.get(pk = pk)

        if(poziv):
            poziv.prijavljeno_pomoci += 1
            poziv.save()

            response.set_cookie('prijavljen', pk, expires=datetime.today() + timedelta(days=1))
        else:
            return HttpResponseRedirect('/obustavljena-akcija')

    return response

def ne_dolazim(request, pk):
    prijavljen = request.COOKIES.get('prijavljen')

    response = HttpResponseRedirect('/')

    if(prijavljen):
        poziv = Poziv.objects.get(pk = pk)

        if(poziv):
            poziv.prijavljeno_pomoci -= 1
            poziv.save()

        response.delete_cookie('prijavljen')

    return response
