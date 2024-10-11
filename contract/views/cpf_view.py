import requests
from django.shortcuts import render, redirect
from decouple import config
from contract.forms import CPFForm
from contract.views.messages_view import render_message 

API_BASE_URL = config('API_BASE_URL')
API_KEY = config('API_KEY')


def cpf_view(request):
    if request.method == 'POST':
        form = CPFForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            url = f'{API_BASE_URL}/form/cpf/{cpf}/'
            headers = {'api-key': API_KEY}

            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        data = response.json()

                        # Salvar os dados retornados na sessão
                        request.session['user_id'] = data.get('id')
                        request.session['cpf'] = data.get('cpf')
                        request.session['apply_method'] = data.get('applyMethod')

                        # Verificar o método de aplicação
                        if data.get('applyMethod') == 'Enem':
                            # Redirecionar para a view enem_upload
                            return redirect('enem_upload')
                        
                        elif data.get('applyMethod') == 'MeritoAcademico':
                            # Usuário faz input manual de dados
                            return redirect('merito_academico_input')

                    except ValueError:
                        return render_message(request, 'error.html', 
                                              title='Erro de JSON',
                                              message='JSON inválido retornado pela API.',
                                              code=500,
                                              error=response.text)
                else:
                    return render_message(request, 'error.html', 
                                          title='Erro na API',
                                          message='A requisição para a API falhou.',
                                          code=response.status_code,
                                          error=response.text)
            except requests.exceptions.RequestException as e:
                return render_message(request, 'error.html', 
                                      title='Erro de Conexão',
                                      message='Erro de conexão com a API.',
                                      code=503,
                                      error=str(e))
    else:
        form = CPFForm()

    return render(request, 'cpf_form.html', {'form': form})