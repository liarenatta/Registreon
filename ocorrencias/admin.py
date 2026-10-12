from django.contrib import admin
from .models import Ocorrencia, MensagemOcorrencia, Bairro, Rua

admin.site.register(Ocorrencia)
admin.site.register(MensagemOcorrencia)
admin.site.register(Rua)
admin.site.register(Bairro)



