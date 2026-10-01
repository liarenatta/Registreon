from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout

from .models import Ocorrencia, MensagemOcorrencia



def inicio(request):
    return render(request, 'inicio.html')

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        celular = request.POST.get('celular')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'cadastro.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado')
            return render(request, 'cadastro.html')
        
        usuario = User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome
        )
        messages.success(
            request, 'Cadastro realizado com sucesso! Faça login para continuar. '

        )
        return redirect('login')
    return render(request, 'cadastro.html')
  



def login(request):
    if request.method == 'POST':        
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        try:
            usuario = User.objects.get(username=email)
        except User.DoesNotExist:
            messages.error(request, 'E-mail ou senha incorretos')
            return redirect('login')

        usuario_autenticado = authenticate(request, username=usuario.username, password=senha)

        if usuario_autenticado is not None:
            auth_login(request, usuario_autenticado)

            messages.success(request, 'Loguin realizado com sucesso!')
            return redirect('painel_cidadao')

        messages.error(request, 'E-mail ou senha incorretos.')
        return redirect('login')     
        
    return render(request, 'login.html')



def logout_cidadao(request):
    logout(request)
    return redirect('inicio')



def anonimo(request):
    return render(request, 'anonimo.html')


def ocorrencias(request):
    if request .method == 'POST':
        categoria = request.POST.get('categoria')
        endereco = request.POST.get('endereco')
        bairro = request.POST.get('bairro')
        descricao = request.POST.get('descricao')
        foto = request.FILES.get('foto')

        Ocorrencia.objects.create(
            categoria = categoria,
            endereco = endereco,
            bairro = bairro,
            descricao = descricao,
            foto = foto,
            cidadao=request.user
        )  

        messages.success(
            request,
            'Ocorrência registrada com sucesso!'
        )

        return redirect('ocorrencias')
    return render(request, 'ocorrencias.html')





def funcionario_login(request):
    return render(request, 'funcionario_login.html')


class DetalheOcorrenciaView(DetailView):
    model = Ocorrencia
    template_name = 'detalhe_ocorrencia.html'
    context_object_name = 'ocorrencia'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Ocorrencia.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        novo_status = request.POST.get('status')
        status_validos = dict(Ocorrencia.STATUS_CHOICES)

        if novo_status in status_validos:
            self.object.status = novo_status
            self.object.save()
            messages.success(request, 'Status atualizado!')

        return redirect('detalhe_ocorrencia', pk=self.object.pk)



@login_required(login_url='login')
def painel_cidadao(request):

    solicitacoes = Ocorrencia.objects.filter(
        cidadao=request.user
    ).order_by('-data_registro')  
    
    return render(
        request,
        'painel_cidadao.html',
        {'solicitacoes': solicitacoes}
    )






@login_required(login_url='login')
def detalhe_cidadao(request, num_solicitacao):
    ocorrencia = get_object_or_404(
        Ocorrencia,
        num_solicitacao = num_solicitacao,
        cidadao = request.user
    )
    mensagens_ocorrencia = ocorrencia.mensagens.order_by('data_envio')
    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()

        if texto:
            MensagemOcorrencia.objects.create(
                ocorrencia=ocorrencia,
                autor=request.user,
                texto=texto
            )
            messages.success(
                request, 'Mensagem adicionada com sucesso!'
            )
        else:
            messages.error(
                request, 'Digite uma mensagem antes de enviar'
            )

        return redirect(
            'detalhe_cidadao', num_solicitacao = ocorrencia.num_solicitacao
        )
        

    return render(
    request, 'detalhe_cidadao.html',
    {
        'ocorrencia':ocorrencia,
        'mensagens_ocorrencia': mensagens_ocorrencia
    }
)

def funcionario_required(user):
    return user.is_authenticated and user.is_staff

##Verificando se é funcionari 


def funcionario_login(request):

    print("================================")
    print("FUNCIONARIO LOGIN")
    print("METHOD:", request.method)
    print("POST:", request.POST)
    print("================================")

    if request.method == 'GET':
        return render(
            request,
            'funcionario_login.html'
        )

    if request.method == 'POST':

        email = request.POST.get('email')
        senha = request.POST.get('senha')

        print("EMAIL:", email)
        print("SENHA:", senha)

        try:
            usuario = User.objects.get(
                username=email
            )

        except User.DoesNotExist:

            print("USUÁRIO NÃO ENCONTRADO")

            messages.error(
                request,
                'E-mail ou senha incorretos.'
            )

            return redirect(
                'funcionario_login'
            )

        print("USUÁRIO ENCONTRADO:", usuario.username)
        print("IS STAFF:", usuario.is_staff)

        usuario_autenticado = authenticate(
            request,
            username=usuario.username,
            password=senha
        )

        print(
            "AUTENTICADO:",
            usuario_autenticado
        )

        if usuario_autenticado is None:

            print("SENHA INCORRETA")

            messages.error(
                request,
                'E-mail ou senha incorretos.'
            )

            return redirect(
                'funcionario_login'
            )

        if not usuario_autenticado.is_staff:

            print("NÃO É FUNCIONÁRIO")

            messages.error(
                request,
                'Este usuário não possui acesso ao painel do funcionário.'
            )

            return redirect(
                'funcionario_login'
            )

        print("LOGIN FUNCIONÁRIO REALIZADO")

        auth_login(
            request,
            usuario_autenticado
        )

        return redirect(
            'painel_funcionario'
        )

    return redirect(
        'funcionario_login'
    )

#
def funcionario_logina(request):

    # Quando a página é aberta normalmente,
    # apenas mostra a tela de login.
    if request.method == 'GET':
        return render(request, 'funcionario_login.html')

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        try:
            usuario = User.objects.get(username=email)

        except User.DoesNotExist:

            messages.error(
                request,
                'E-mail ou senha incorretos.'
            )

            return redirect('funcionario_login')
        usuario_autenticado = authenticate(
            request,
            username=usuario.username,
            password=senha
        )
        if usuario_autenticado is None:

            messages.error(
                request,
                'E-mail ou senha incorretos.'
            )
            return redirect('funcionario_login')

        if not usuario_autenticado.is_staff:

            messages.error(
                request,
                'Este usuário não possui acesso ao painel do funcionário.'
            )
            return redirect('funcionario_login')

        auth_login(request, usuario_autenticado)
        return redirect('painel_funcionario')
    return redirect('funcionario_login')




@login_required(login_url='funcionario_login')
@user_passes_test(funcionario_required, login_url='funcionario_login')
def logout_funcionario(request):
    logout(request)
    return redirect('inicio')

class PainelFuncionarioView(ListView):

    model = Ocorrencia

    template_name = 'painel_funcionario.html'

    context_object_name = 'ocorrencias'

    ordering = ['-data_registro']

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('funcionario_login')

        if not request.user.is_staff:
            messages.error(
                request,
                'Você não possui acesso ao painel do funcionário.'
            )
            return redirect('funcionario_login')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

class PaineelFuncionarioView(ListView):
    model = Ocorrencia
    template_name = 'painel_funcionario.html'
    context_object_name = 'ocorrencias'
    ordering = ['-data_registro']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('funcionario_login')

        if not request.user.is_staff:
            messages.error(
                request, 'Você não possui acesso ao painel no funcionario'
            )
        return redirect('funcionario_login')
    
        return super().dispatch(request, *args, **kwargs)




