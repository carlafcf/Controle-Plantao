from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from datetime import date
from django.contrib import messages

from plantao.models import Plantao

class CriarPlantao(LoginRequiredMixin, generic.CreateView):
    fields = ("data_plantao", "turno", 'horas')
    model = Plantao

    def form_valid(self, form):
        form.instance.plantonista = self.request.user
        if Plantao.objects.filter(plantonista = self.request.user, data_plantao = form.cleaned_data['data_plantao'], turno = form.cleaned_data['turno']).exists():
            messages.add_message(self.request, messages.WARNING, "Um plantão nesta mesma data e turno já foi cadastrado por você")
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super(CriarPlantao, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse("plantao:listar")

@login_required
def listar(request):
    this_month = date.today().month
    plantoes = Plantao.objects.filter(data_plantao__month=this_month)
    total_horas = list(Plantao.objects.filter(data_plantao__month=this_month).aggregate(Sum('horas')).values())[0]
    context = {'plantao_list': plantoes, 'total_horas': total_horas}
    return render(request, 'Plantao/plantao_list.html', context)

