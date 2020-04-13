from django.db import models
from datetime import date
from django.contrib.auth import get_user_model

User=get_user_model()

class Plantao(models.Model):
    TURNOS = [
        ('1', 'Manhã'),
        ('2', 'Tarde'),
        ('3', 'Noite'),
    ]

    plantonista = models.ForeignKey(User, related_name='plantoes', on_delete=models.CASCADE)
    data_plantao = models.DateField(default=date.today)
    turno = models.CharField(max_length=1, choices=TURNOS, default='1')
    horas = models.PositiveIntegerField(blank=False)

    def __str__(self):
        return "{}: {} {} {} horas".format(self.plantonista, self.data_plantao, self.turno, self.horas)

    class Meta:
        ordering = ['data_plantao', 'turno']
