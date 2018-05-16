import csv
from io import TextIOWrapper, BytesIO, StringIO
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .skos import SkosImporter, Csv2SkosImporter
from .models import *

# http://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes

@login_required
def import_csv(request):
    context = {}
    if request.method == 'POST':
        context["form"] = UploadFileForm(request.POST, request.FILES)
        if context["form"].is_valid():
            file = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
            skos = Csv2SkosImporter(file)
            context['worked'] = skos.importConcepts()
            return render(request, 'vocabs/import_skos.html', context)
    else:
        context["form"] = UploadFileForm()
        context['worked'] = "upload something first"
    return render(request, 'vocabs/import_skos.html', context)


@login_required
def import_skos(request):
    context = {}
    if request.method == 'POST':
        context["form"] = UploadFileForm(request.POST, request.FILES)
        if context["form"].is_valid():
            file = request.FILES['file']
            skos = SkosImporter(file)
            context['worked'] = skos.importConcepts()
            return render(request, 'vocabs/import_skos.html', context)
    else:
        context["form"] = UploadFileForm()
        context['worked'] = "upload something first"
    return render(request, 'vocabs/import_skos.html', context)
