from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the plant_disease_classification_ui index.")
