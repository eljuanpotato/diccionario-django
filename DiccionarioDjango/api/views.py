from django.http import JsonResponse
from spellchecker import SpellChecker
from rest_framework.decorators import api_view

# Crear una instancia de SpellChecker para el idioma español
spell = SpellChecker(language='es')

# Función para corregir la ortografía de una palabra
def corregir_ortografia(palabra):
    correccion = spell.correction(palabra)
    return correccion

# Función para determinar el tipo de palabra
def tipo_palabra(palabra):
    if len(palabra) < 2:
        return "Desconocido"
    
    vocales = "aeiouáéíóúü"
    acentos = "áéíóú"

    num_silabas = 0
    tiene_tilde = False
    for letra in palabra:
        if letra in vocales:
            num_silabas += 1
        if letra in acentos:
            tiene_tilde = True

    if palabra[-1] in "ns" and palabra[-2] in vocales:
        silaba_tonica = -2
    elif palabra[-1] in vocales:
        silaba_tonica = -1
    else:
        silaba_tonica = -1

    if tiene_tilde:
        if palabra[-3] in acentos:
            silaba_tonica = -3
        elif palabra[-2] in acentos:
            silaba_tonica = -2
        elif palabra[-1] in acentos:
            silaba_tonica = -1

    if silaba_tonica == -1:
        return "Aguda"
    elif silaba_tonica == -2:
        return "Grave"
    elif silaba_tonica == -3:
        return "Esdrújula"
    elif silaba_tonica <= -4:
        return "Sobreesdrújula"
    else:
        return "Desconocido"

@api_view(['POST'])
def corregir(request):
    palabra = request.data.get('palabra', '')
    if not palabra:
        return JsonResponse({'error': 'No se ha proporcionado ninguna palabra.'}, status=400)
    
    palabra_corregida = corregir_ortografia(palabra)
    tipo = tipo_palabra(palabra_corregida)

    return JsonResponse({'palabra_corregida': palabra_corregida, 'tipo_palabra': tipo})
