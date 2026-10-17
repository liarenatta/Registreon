from django.db import models
from django.contrib.auth.models import User


class Bairro(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    class Meta:
        ordering = ['nome']
        verbose_name = 'Bairro'
        verbose_name_plural = 'Bairros'
    def save(self, *args, **kwargs):
        self.nome = ' '.join(self.nome.split()).strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome



class Rua(models.Model):

    nome = models.CharField(max_length=150)
    bairro = models.ForeignKey(
        Bairro,
        on_delete=models.PROTECT,
        related_name='ruas'
    )
    class Meta:
        ordering = ['nome']
        verbose_name = 'Rua'
        verbose_name_plural = 'Ruas'
        constraints = [
            models.UniqueConstraint(
                fields=['nome', 'bairro'],
                name='rua_unica_por_bairro'
            )
        ]

    def save(self, *args, **kwargs):
        self.nome = ' '.join(self.nome.split()).strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome} - {self.bairro.nome}'





class Ocorrencia(models.Model):
    num_solicitacao = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    bairro = models.ForeignKey(
        Bairro,
        on_delete=models.PROTECT,
        related_name='ocorrencias',
        null=True,
        blank=True
    )
    

    numero = models.CharField(max_length=30, blank=True, default='')
    ponto_referencia = models.CharField(max_length=255, blank=True, default='')
    data_registro = models.DateTimeField(auto_now_add=True)

    descricao = models.TextField()

    cidadao = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solicitacoes'
    )

    cod_acompanhamento = models.CharField(
        max_length=20,
        unique=True,
        blank=True
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


