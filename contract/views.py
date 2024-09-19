from django.shortcuts import render, redirect, HttpResponse
from .forms import PostData, SendForm, LoginForm, EnemForm
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import re
import PyPDF2
import shutil
import requests
import pytesseract
import os
import subprocess
from pdf2image import convert_from_path
from docx import Document
import traceback 


def login(request):
    print("Método HTTP:", request.method)
    form = LoginForm()
    error_message = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            current_cpf = form.cleaned_data['cpf_input']
            print("CPF recebido:", current_cpf)

            url_id = f'https://form.pdinfinita.com.br/form/cpf/{current_cpf}'
            key = 'Rm9ybUFwaUZlaXRhUGVsb0plYW5QaWVycmVQYXJhYURlc2Vudm9sdmU='
            headers = {'api-key': key}

            try:
                print("Fazendo requisição para obter ID do CPF...")
                response_id = requests.get(url_id, headers=headers)
                response_id.raise_for_status()
                print("Requisição para CPF bem sucedida")

                data_id = response_id.json()
                print("Dados recebidos:", data_id)

                if response_id.status_code == 200:
                    id_value = data_id.get('id')
                    print("ID obtido:", id_value)

                    if id_value:
                        request.session['id_value'] = id_value
                        url_method = f'https://form.pdinfinita.com.br/form/{id_value}/applyMethod'

                        print("Fazendo requisição para aplicar o método...")
                        response_method = requests.patch(url_method, headers=headers)
                        response_method.raise_for_status()

                        data_method = response_method.json()
                        print("Dados do método:", data_method)

                        if response_method.status_code == 200:
                            method = data_method.get('applyMethod')
                            print("Método retornado:", method)

                            if method == "Enem":
                                print("Redirecionando para Enem_form")
                                return redirect('Enem_form')
                            
                            if method == 'MeritoAcademico':
                                print("Redirecionando para MeritoAcademico")
                                return redirect('get_data')
                            
            except requests.RequestException as e:
                error_message = f"Erro ao consultar CPF. Contate o suporte. Erro: {str(e)}"
                print(f"Erro na requisição: {e}")
            except Exception as e:
                error_message = f"Ocorreu um erro. Tente novamente. Erro: {str(e)}"
                print("Erro inesperado:", traceback.format_exc())

    return render(request, "login.html", {"form": form, "error_message": error_message})



# Função para processar o formulário e gerar o documento
def get_data(request):
    form = PostData()

    if request.method == "POST":
        form = PostData(request.POST)
        if form.is_valid():
            diretor = form["nome_diretor"].value()
            escola = form["nome_escola"].value()
            endereco = form["endereco_escola"].value()
            data = form["data_preenchimento"].value()
            aluno = form["nome_aluno"].value()
            nota = form["nota"].value()

            current_dir = Path(__file__).resolve().parent
            input_dir = current_dir / "upload"
            output_dir = current_dir / "output"
            output_dir.mkdir(parents=True, exist_ok=True)

            original_doc = input_dir / 'Carta.docx'
            temp_doc = input_dir / 'Carta_temp.docx'

            shutil.copyfile(original_doc, temp_doc)

            output_file = None

            try:
                # Abrir e manipular o documento usando python-docx
                doc = Document(str(temp_doc))

                substitutions = {
                    "[Nome do Diretor ou Diretora]": diretor,
                    "[Nome da Escola]": escola,
                    "[Endereço Completo da Escola]": endereco,
                    "[Data]": data,
                    "[Nome do Aluno]": aluno,
                    "[Nota]": nota,
                }

                for paragraph in doc.paragraphs:
                    for find_str, replace_with in substitutions.items():
                        if find_str in paragraph.text:
                            paragraph.text = paragraph.text.replace(find_str, replace_with)

                # Salvar o documento modificado
                modified_doc_path = output_dir / f"Manipulado_{temp_doc.stem}.docx"
                doc.save(modified_doc_path)

                # Converter para PDF usando libreoffice via subprocess
                pdf_output_file = output_dir / f"Manipulado_{temp_doc.stem}.pdf"
                convert_command = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', str(output_dir), str(modified_doc_path)]
                subprocess.run(convert_command, check=True)

                output_file = pdf_output_file

            except subprocess.CalledProcessError as e:
                print(f"Erro na conversão para PDF: {e}")
                return HttpResponse("Erro ao converter o documento para PDF", status=500)
            finally:
                if temp_doc.exists():
                    temp_doc.unlink()

            # Servir o PDF gerado para o cliente
            if output_file and output_file.exists():
                with open(output_file, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename={output_file.name}'
                    return response

    return render(request, "formulario.html", {"form": form})

# Função para extrair texto de um PDF usando PyPDF2
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

# Função para extrair texto de imagem usando OCR
def OCR_image(request):
    form = SendForm()

    id_value = request.session.get('id_value')
    print(id_value)

    if request.method == "POST" and request.FILES.get('pdf_file'):
        form = SendForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']

            fs = FileSystemStorage()
            filename = fs.save(pdf_file.name, pdf_file)
            uploaded_pdf_path = fs.path(filename)

            extracted_text = extract_text_from_pdf(uploaded_pdf_path)

            pattern = r"Média simples dos anos cursados no ensino médio \(comprovação em anexo\):\s*(.*)"
            match = re.search(pattern, extracted_text)

            if match:
                nota_extraida = match.group(1)
                nota_encontrada = True
            else:
                nota_extraida = "Campo não encontrado."
                nota_encontrada = False

            if nota_encontrada:
                url_method = f'https://form.pdinfinita.com.br/form/{id_value}/applyMethod'
                key = 'Rm9ybUFwaUZlaXRhUGVsb0plYW5QaWVycmVQYXJhYURlc2Vudm9sdmU='
                headers = {
                    'api-key': key
                }
                body = {
                    "applyMethod": "MeritoAcademico",
                    "applyMethodGrade": nota_extraida
                }

                try:
                    response_method = requests.patch(url_method, headers=headers, json=body)
                    response_method.raise_for_status()

                    return HttpResponse("Nota enviada com sucesso.")

                except requests.RequestException as e:
                    print(f"Erro ao enviar a nota: {e}", status=500)
                    return HttpResponse(f"Erro ao enviar nota, favor contate o suporte")

    return render(request, "upload_pdf.html", {"form": form})

# Função para processar o formulário do ENEM
def Enem_form(request):
    form = EnemForm()

    if request.method == "POST" and request.FILES.get('enem_form'):
        form = EnemForm(request.POST, request.FILES)
        if form.is_valid():
            enem_form = form.cleaned_data['enem_form']
            if not enem_form.name.endswith('.pdf'):
                return HttpResponse("Por favor, envie um arquivo PDF.")

            fs = FileSystemStorage()
            filename = fs.save(enem_form.name, enem_form)
            uploaded_pdf_path = fs.path(filename)

            pages = convert_from_path(uploaded_pdf_path)

            texto = ""
            for page in pages:
                texto += pytesseract.image_to_string(page)

            try:
                redacao_nota = float(re.search(r'Redacao\s(\d+)', texto).group(1))
                matematica_nota = float(re.search(r'Matematica e suas Tecnologias\s(\d+)', texto).group(1))

                # matematica_nota = matematica_nota / 10.0

                nome = re.search(r'Nome:\s(.+)', texto).group(1).strip()
                cpf = re.search(r'CPF:\s([\d\.\-]+)', texto).group(1).strip()

                cpf = re.sub(r'[^\d]', '', cpf)

                nota_geral = (matematica_nota * 0.8) + (redacao_nota * 0.2)

                request.session['nome'] = nome
                request.session['cpf'] = cpf
                request.session['nota_matematica'] = matematica_nota
                request.session['nota_redacao'] = redacao_nota
                request.session['nota_geral'] = nota_geral

                for page in pages:
                    if hasattr(page, 'filename') and os.path.exists(page.filename):
                        os.remove(page.filename)

            except Exception as e:
                return HttpResponse(f"Erro ao processar o arquivo: {str(e)}")

            return redirect('Confirm_data')

    return render(request, "formulario_enem.html", {"form": form})

# Função para confirmar os dados do ENEM
def Confirm_data(request):
    if request.method == "POST":
        id_value = request.session.get('id_value')
        nome = request.session.get('nome')
        cpf = request.session.get('cpf')
        nota_matematica = request.session.get('nota_matematica')
        nota_redacao = request.session.get('nota_redacao')
        nota_geral = request.session.get('nota_geral')

        url_method = f'https://form.pdinfinita.com.br/form/{id_value}/applyMethod'
        key = 'Rm9ybUFwaUZlaXRhUGVsb0plYW5QaWVycmVQYXJhYURlc2Vudm9sdmU='
        headers = {'api-key': key}
        body = {
            "applyMethod": "Enem",
            "applyMethodGrade": nota_geral,
        }

        try:
            print(f"Enviando nota para o ID {id_value} com a nota geral: {nota_geral}")
            response_method = requests.patch(url_method, headers=headers, json=body)
            response_method.raise_for_status()

            # Nota enviada com sucesso - redireciona para a página de sucesso
            return render(request, 'success.html')

        except requests.RequestException as e:
            print(f"Erro ao enviar a nota: {e}")
            return render(request, 'error.html', {"message": f"Erro ao enviar nota: {str(e)}"}, status=500)

    # Se não for uma requisição POST, renderize novamente o formulário
    nome = request.session.get('nome')
    cpf = request.session.get('cpf')
    nota_matematica = request.session.get('nota_matematica')
    nota_redacao = request.session.get('nota_redacao')
    nota_geral = request.session.get('nota_geral')

    return render(request, "confirm_data.html", {
        "nome": nome,
        "cpf": cpf,
        "nota_matematica": nota_matematica,
        "nota_redacao": nota_redacao,
        "nota_geral": nota_geral,
    })
