from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from django.views.generic import TemplateView
from .models import Post
from .forms import PostForm
from .forms import SimpleForm
from django.urls import reverse
import json
from django.utils import timezone
from django.core import serializers

data = None


# Не важно
def post_list(request):
    global data
    text = None
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = PostForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = PostForm(request.POST)
        data = request.POST
        if form.is_valid():
            form.save()
            text = form.cleaned_data['content']
            return HttpResponseRedirect(reverse('pyinjs:post_list'))
    context = {'form': form, 'text': text}
    return render(request, 'pyinjs/post_list.html', context)
# Конец не важно


# ================= То что нужно ============================================================
def hpr(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        script = received_json_data["script"]

        exec(script)
        result = eval('f(4)')

        return JsonResponse({"script": script, "result": str(result)}, safe=False)
    else:
        return render(request, 'pyinjs/handling_post_request.html')
###############################################################################################

# Create your views here.
# def post_list(request):
#     return render(request, 'templates/post_list.html')


