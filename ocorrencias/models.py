from django.db import models
from django.contrib.auth.models import User

class Ocorrencia(models.Model):
    num_solicitacao = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    descricao = models.TextField()
    data_registro = models.DateTimeField(auto_now_add=True)

    cidadao = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solicitacoes'
    )

   
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Em análise', 'Em análise'),
        ('Em andamento', 'Em andamento'),
        ('Concluída', 'Concluída'),       
    ]

    status = models.CharField(
        max_length = 50,
        choices = STATUS_CHOICES,
        default = 'Pendente'
    )


    foto=models.ImageField(upload_to='ocorrencias/', blank=True, null=True)

    def __str__(self):
        return f'Solicitação {self.num_solicitacao}'


class MensagemOcorrencia(models.Model):

    ocorrencia = models.ForeignKey(
        Ocorrencia,
        on_delete = models.CASCADE,
        related_name='mensagens'
    )

    autor = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null=True,
        blank=True
    )

    texto = models.TextField()

    data_envio = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return(
            f'Mensagem da solicitação'
            f'{self.ocorrencia.num_solicitacao}'
        )


