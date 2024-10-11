# contract/views.py
from django.shortcuts import redirect
from contract.tasks import send_enem_data  # Importa a task
from contract.views.messages_view import confirm_success_view, confirm_error_view, render_message  # Importa as views de mensagem
import logging

logger = logging.getLogger('django')

def confirm_send_view(request):
    if request.method == 'POST':
        try:
            # Obter os dados da sessão
            id_value = request.session.get('user_id')
            nota_geral = request.session.get('nota_geral')
            apply_method = request.session.get('apply_method')

            # Verificar se os dados estão presentes
            if not id_value or not nota_geral or not apply_method:
                logger.error("Dados ausentes na sessão: id_value, nota_geral ou apply_method")
                return confirm_error_view(request)

            # Debug para verificar os dados
            logger.info(f"Id User: {id_value}, Nota Geral: {nota_geral}, Metodo: {apply_method}")

            # Enviar os dados individualmente via Celery
            send_enem_data.delay(id_value, nota_geral, apply_method)

            # Limpar a sessão
            request.session.flush()

            # Redirecionar para a view de sucesso
            return confirm_success_view(request)

        except Exception as e:
            logger.error(f"Erro ao enviar os dados: {e}")
            return confirm_error_view(request)

    # Se o método da requisição não for POST, redirecionar para a página de resultados
    return redirect('enem_result')
