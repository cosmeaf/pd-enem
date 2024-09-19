from django import forms

class PostData(forms.Form):
    nome_diretor = forms.CharField(
        label="Nome Diretor ou Diretora",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control form-input"})
    )
    nome_escola = forms.CharField(
        label="Nome da Escola",
        required=True,
        max_length=70,
        widget=forms.TextInput(attrs={"class": "form-control form-input"})
    )
    endereco_escola = forms.CharField(
        label="Endereço da Escola",
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control form-input"})
    )
    nome_aluno = forms.CharField(
        label="Nome do aluno",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control form-input"})
    )
    nota = forms.CharField(
        label="Nota",
        required=True,
        max_length=6,
        widget=forms.TextInput(attrs={"class": "form-control form-input"})
    )
    data_preenchimento = forms.DateField(
        label="Data",
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",  
                "class": "form-control form-input"
            }
        )
    )

class SendForm(forms.Form):
    pdf_file = forms.FileField(
        label="Upload do PDF",
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control form-file-input",  
                "accept": "application/pdf", 
            }
        )
    )

class LoginForm(forms.Form):
    cpf_input = forms.CharField(
        label='Insira seu CPF:',
        required= True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-input",
            }
        )
    )

class EnemForm(forms.Form):
    enem_form = forms.FileField(
    label="Upload do PDF",
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control form-file-input",  
                "accept": "application/pdf", 
            }
        )
    )
    