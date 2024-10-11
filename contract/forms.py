from django import forms
from contract.utility.cpf_validate import CPFValidator

class CPFForm(forms.Form):
    cpf = forms.CharField(
        max_length=14,
        label="CPF",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF'})
    )

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')

        # Remover qualquer formatação anterior (pontos e traços)
        cpf_limpo = cpf.replace('.', '').replace('-', '')

        # Inicializar o CPFValidator com o CPF limpo
        validator = CPFValidator(cpf_limpo)

        # Verificar se o CPF é válido
        if not validator.is_valid():
            raise forms.ValidationError("CPF inválido.")
        
        # Em vez de retornar o CPF formatado, retornar o CPF "limpo" (sem formatação)
        return cpf_limpo  # Agora o CPF será retornado sem pontos ou traços


class EnemPDFUploadForm(forms.Form):
    pdf_file = forms.FileField(
        label="Upload do PDF do ENEM",
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
    )

    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            # Verificar se a extensão do arquivo é .pdf
            if not pdf_file.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Apenas arquivos no formato PDF são permitidos. Por favor, baixe o arquivo oficial do site do ENEM.")
            # Verificar o tipo MIME do arquivo
            if pdf_file.content_type != 'application/pdf':
                raise forms.ValidationError("O arquivo enviado não é um PDF válido.")
        return pdf_file


class MeritoAcademicoForm(forms.Form):
    nome_aluno = forms.CharField(
        label='Nome do Aluno', 
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do aluno'})
    )
    nome_diretor = forms.CharField(
        label='Nome do Diretor', 
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do diretor'})
    )
    nome_escola = forms.CharField(
        label='Nome da Escola', 
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da escola'})
    )
    
    endereco_escola = forms.CharField(
        label='Endereço Completo da Escola', 
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o endereço completo da escola'})
    )

    data = forms.DateField(
        label='Data',
        widget=forms.TextInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'Selecione a data'
        })
    )
    
    media_ensino_medio = forms.DecimalField(
        label='Média do Ensino Médio',
        max_digits=5, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a média final'})
    )
