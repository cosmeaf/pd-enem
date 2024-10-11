from django.shortcuts import render

# View para mensagens de sucesso
def confirm_success_view(request):
    message = 'Dados enviados com sucesso!'
    return render(request, 'confirm_success.html', {'message': message})

# View para mensagens de erro
def confirm_error_view(request):
    message = 'Ocorreu um erro ao tentar enviar os dados. Por favor, tente novamente mais tarde.'
    return render(request, 'confirm_error.html', {'message': message})



def render_message(request, template_name, title=None, message=None, code=None, error=None):
    """
    Método reutilizável para renderizar templates de mensagens com título, mensagem, código de erro e detalhes.
    """
    context = {
        'title': title,
        'message': message,
        'code': code,
        'error': error
    }

    return render(request, template_name, context)

