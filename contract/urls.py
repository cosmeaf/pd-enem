from django.urls import path
from django.conf.urls import handler404
from django.shortcuts import render
from .views import get_data, OCR_image, login, Enem_form, Confirm_data

urlpatterns = [
    path('', login, name='login'),
    path('formulario/', get_data, name='get_data'),
    path('upload-pdf/', OCR_image, name='OCR_image'),
    path('formulario-enem/', Enem_form, name='Enem_form'),
    path('confirm-data/', Confirm_data, name='Confirm_data'),
]

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = 'contract.urls.custom_404'
