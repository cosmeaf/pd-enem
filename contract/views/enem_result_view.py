from django.shortcuts import render

# View para exibir os resultados
def enem_result_view(request):
    # Recuperar os dados da sessão
    nome = request.session.get('nome', '')
    cpf_extraido = request.session.get('cpf_extraido', '')
    nota_matematica = request.session.get('nota_matematica', '')
    nota_redacao = request.session.get('nota_redacao', '')
    nota_geral = request.session.get('nota_geral', '')

    # Debug: imprimir os valores recuperados da sessão
    print("nome:", nome)
    print("cpf_extraido:", cpf_extraido)
    print("nota_matematica:", nota_matematica)
    print("nota_redacao:", nota_redacao)
    print("nota_geral:", nota_geral)

    # Exibir os dados e pedir confirmação
    return render(request, 'enem_result.html', {
        'nome': nome,
        'cpf_extraido': cpf_extraido,
        'nota_matematica': nota_matematica,
        'nota_redacao': nota_redacao,
        'nota_geral': nota_geral,
        'confirm_message': 'Os dados estão corretos? Se sim, confirme o envio, ou entre em contato com o suporte.'
    })
