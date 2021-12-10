from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Client, Record

if settings.DEBUG:
    collector_view_allowed_methods = ['GET', 'POST']
else:
    collector_view_allowed_methods = ['POST']


def index(request: WSGIRequest):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'main/index.html')


def get_client_addr(request: WSGIRequest):
    if settings.BEHIND_PROXY:
        addr = request.META.get('HTTP_X_FORWARDED_FOR')
        if addr:
            return addr
    addr = request.META.get('REMOTE_ADDR')
    return addr


@require_http_methods(collector_view_allowed_methods)
@csrf_exempt
def collector(request: WSGIRequest, client_name: str, tag=''):
    # TODO: authenticate the client
    try:
        client = Client.objects.get(name=client_name)
    except Client.DoesNotExist as e:
        return HttpResponseNotFound('<p style="color:red">Error: Client name %s is not found.</p>' % client_name)

    if not client.active:
        return HttpResponseNotFound('<p style="color:red">Error: Client %s is inactive.</p>' % client_name)

    if request.method == 'GET':
        content: bytes = b'(GET)'
    elif request.method == 'POST':
        content: bytes = request.body

    try:
        content = content.decode('utf-8')
    except Exception as e:
        return HttpResponseServerError('Can\'t Decode request body as UTF-8.')

    print(content)

    rec = Record(target=client,
                 addr=get_client_addr(request),
                 tag=tag,
                 content=content)
    rec.save()

    response = "%s.%s\n%s\n"
    return HttpResponse(response % (client_name, tag, client.name))


def clients(request: WSGIRequest):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    client_list = Client.objects.all()
    context = {
        'client_list': client_list,
    }
    return render(request, 'main/clients.html', context)


def records(request: WSGIRequest):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    record_list = Record.objects.all()
    context = {
        'record_list': record_list,
    }
    return render(request, 'main/records.html', context)


def record(request: WSGIRequest, record_id: int):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    try:
        record = Record.objects.get(id=record_id)
    except Record.DoesNotExist as e:
        record = None
    context = {
        'record': record,
    }
    if record:
        status = None
    else:
        status = 404
    return render(request, 'main/record.html', context, status=status)
