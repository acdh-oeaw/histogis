from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.urls import reverse

from .utils import (
    as_arche_graph,
    serialize_project,
    ARCHE_BASE_URL,
    get_arche_id,
    title_img,
    ARCHE_DEFAULT_EXTENSION,
    ARCHE_PAYLOAD_MIMETYPE
)

from shps.models import TempSpatial


def res_as_arche_graph(request, pk):
    format = request.GET.get('format', 'xml')
    try:
        res = TempSpatial.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404(f"No object with id: {pk} found")
    g = as_arche_graph(res)
    if format == 'turtle':
        return HttpResponse(
            g.serialize(encoding='utf-8', format='turtle'), content_type='text/turtle'
        )
    else:
        return HttpResponse(
            g.serialize(encoding='utf-8'), content_type='application/xml'
        )


def project_as_arche_graph(request):
    g = serialize_project()
    if format == 'turtle':
        return HttpResponse(
            g.serialize(encoding='utf-8', format='turtle'), content_type='text/turtle'
        )
    else:
        return HttpResponse(
            g.serialize(encoding='utf-8'), content_type='application/xml'
        )


def get_ids(request):
    base_uri = request.build_absolute_uri().split('/shapes')[0]
    data = {
        "arche_constants": f"{base_uri}{reverse('shapes:project_as_arche')}",
        "id_prefix": f"{ARCHE_BASE_URL}",
        "ids": [
            {
                "id": f"{ARCHE_BASE_URL}/{x.source.slug_name()}/{x.slug_name()}",
                "filename": f"{x.slug_name()}.{ARCHE_DEFAULT_EXTENSION}",
                "md": f"{base_uri}{x.get_arche_url()}",
                "html": f"{base_uri}{x.get_absolute_url()}",
                "payload": f"{base_uri}{x.get_json_url()}?format=json",
                "mimetype": f"{ARCHE_PAYLOAD_MIMETYPE}"
            } for x in TempSpatial.objects.all()],
    }
    data['ids'].append(
        {
            "id": f"{ARCHE_BASE_URL}/histogis_projektlogo_black.png",
            "filename": f"histogis_projektlogo_black.png",
            "md": f"{base_uri}{reverse('shps:arche_title_img')}",
            "payload": "https://histogis.acdh.oeaw.ac.at/static/webpage/img/histogis_projektlogo_black.png",
            "mimetype": "image/png"
        }
    )
    return JsonResponse(data)


def get_title_img(request):
    g = title_img()
    if format == 'turtle':
        return HttpResponse(
            g.serialize(encoding='utf-8', format='turtle'), content_type='text/turtle'
        )
    else:
        return HttpResponse(
            g.serialize(encoding='utf-8'), content_type='application/xml'
        )
