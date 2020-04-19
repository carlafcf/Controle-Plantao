from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from datetime import date, datetime
from django.contrib import messages
from calendar import monthrange

from plantao.models import Plantao
from usuario.models import User

class CriarPlantao(LoginRequiredMixin, generic.CreateView):
    fields = ("data_plantao", "turno", 'horas')
    model = Plantao
    template_name = 'Plantao/plantao_form.html'

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        form.instance.plantonista = user
        if Plantao.objects.filter(plantonista = user, data_plantao = form.cleaned_data['data_plantao'], turno = form.cleaned_data['turno']).exists():
            messages.add_message(self.request, messages.WARNING, "Um plantão nesta mesma data e turno já foi cadastrado por você")
            return self.render_to_response(self.get_context_data(form=form))
        elif ((form.cleaned_data['turno'] == '1' or form.cleaned_data['turno'] == '2') and form.cleaned_data['horas'] > 6) or (form.cleaned_data['turno'] == '3' and form.cleaned_data['horas'] > 12):
            messages.add_message(self.request, messages.WARNING,
                                 "Quantidade de horas cadastradas inválida.")
            return self.render_to_response(self.get_context_data(form=form))
        elif (form.cleaned_data['data_plantao'].month != date.today().month):
            messages.add_message(self.request, messages.WARNING,
                                 "Não é possível cadastrar plantões para outros meses.")
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super(CriarPlantao, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse("plantao:listar")

class CriarPlantaoAdmin(LoginRequiredMixin, generic.CreateView):
    fields = ('plantonista', "data_plantao", "turno", 'horas')
    model = Plantao
    template_name = 'Plantao/plantao_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['plantonista'].queryset = User.objects.filter(is_active=True)
        return form

    def get_initial(self):
        initial_base = super(CriarPlantaoAdmin, self).get_initial()
        initial_base['plantonista'] = User.objects.filter(username=self.request.user.username)[0]
        return initial_base

    def form_valid(self, form):
        if Plantao.objects.filter(plantonista = form.cleaned_data['plantonista'], data_plantao = form.cleaned_data['data_plantao'], turno = form.cleaned_data['turno']).exists():
            messages.add_message(self.request, messages.WARNING, "Um plantão nesta mesma data e turno já foi cadastrado para este plantonista.")
            return self.render_to_response(self.get_context_data(form=form))
        elif ((form.cleaned_data['turno'] == '1' or form.cleaned_data['turno'] == '2') and form.cleaned_data['horas'] > 6) or (form.cleaned_data['turno'] == '3' and form.cleaned_data['horas'] > 12):
            messages.add_message(self.request, messages.WARNING,
                                 "Quantidade de horas cadastradas inválida.")
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super(CriarPlantaoAdmin, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse("plantao:listar")

class EditarPlantao(LoginRequiredMixin, generic.UpdateView):
    model = Plantao
    fields = ['data_plantao', 'turno', 'horas']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        if ((form.cleaned_data['turno'] == '1' or form.cleaned_data['turno'] == '2') and form.cleaned_data['horas'] > 6) or (form.cleaned_data['turno'] == '3' and form.cleaned_data['horas'] > 12):
            messages.add_message(self.request, messages.WARNING,
                                 "Quantidade de horas cadastradas inválida.")
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super(EditarPlantao, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse("plantao:listar")

class DeletarPlantao(LoginRequiredMixin, generic.DeleteView):
    model = Plantao
    success_url = reverse_lazy('plantao:listar')

@login_required
def listar(request, list_all=1):
    this_month = date.today().month
    this_year = date.today().year
    if request.user.is_superuser and list_all:
        plantoes = Plantao.objects.filter(data_plantao__month=this_month, data_plantao__year=this_year)
        total_horas = list(Plantao.objects.filter(data_plantao__month=this_month, data_plantao__year=this_year)
                           .aggregate(Sum('horas')).values())[0]
    else:
        plantoes = Plantao.objects.filter(data_plantao__month=this_month, data_plantao__year=this_year,
                                          plantonista=request.user)
        total_horas = list(Plantao.objects.filter(data_plantao__month=this_month, data_plantao__year=this_year,
                                                  plantonista=request.user).aggregate(Sum('horas')).values())[0]
    context = {'plantao_list': plantoes, 'total_horas': total_horas}
    return render(request, 'Plantao/plantao_list.html', context)

@login_required
def resumo_mes(request, year, month):
    lista_final = []
    plantonistas = User.objects.all()
    horas = 0
    if year == 0 and month == 0:
        this_month = date.today().month
        this_year = date.today().year
    else:
        this_month = month
        this_year = year
    for plantonista in plantonistas:
        total_horas = list(Plantao.objects.filter(data_plantao__month=this_month, data_plantao__year=this_year,
                                                  plantonista=plantonista).aggregate(Sum('horas')).values())[0]
        horas += int(0 if total_horas is None else total_horas)
        lista_final.append([plantonista, int(0 if total_horas is None else total_horas)])
    context = {'lista_final': lista_final, 'total_horas': horas}
    return render(request, 'Plantao/resumo_mes.html', context)

def calendario_mes(request, year, month, dia_selecionado):
    if year == 0 and month == 0:
        ano = date.today().year
        mes = date.today().month
    else:
        ano = year
        mes = month
    qnt_dias = monthrange(ano, mes)[1]
    resumo = []
    total_horas = 0
    for dia in range(1,qnt_dias+1):
        data = datetime.strptime(str(ano)+str(mes)+str(dia), '%Y%m%d').date()
        horas_dia = list(Plantao.objects.filter(data_plantao = data).
                         aggregate(Sum('horas')).values())[0]
        total_horas += int(0 if horas_dia is None else horas_dia)
        resumo.append({'data': data, 'horas': int(0 if horas_dia is None else horas_dia)})
    print(dia_selecionado)
    if dia_selecionado == 0:
        plantao_list = []
    else:
        plantao_list = Plantao.objects.filter(data_plantao__day=dia_selecionado, data_plantao__month=mes,
                                              data_plantao__year=ano)
    print(plantao_list)
    context = {'resumo': resumo, 'total_horas': total_horas, 'plantao_list': plantao_list}
    return render(request, 'Plantao/calendario_mes.html', context)
