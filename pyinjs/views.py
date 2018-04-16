from django.shortcuts import render as __render
from django.http import HttpResponseRedirect, JsonResponse
from .forms import PostForm
from django.urls import reverse as __reverse
import json
import numpy
from networkx import Graph


result = 888


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
            return HttpResponseRedirect(__reverse('pyinjs:post_list'))
    context = {'form': form, 'text': text}
    return __render(request, 'pyinjs/post_list.html', context)
# Конец не важно


# ================= То что нужно ============================================================
def hpr(request):
    global result
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        script = received_json_data["script"]
        state = received_json_data["state"]

        state_keys = list(state.keys())
        state_values = list(state.values())

        for i in range(len(state_keys)):
            state_keys[i] = 'scope_'+state_keys[i]+' = '+str(state_values[i])

        variables = '\n'.join(state_keys)

        taboos = ['__render', 'HttpResponseRedirect', 'JsonResponse', 'PostForm', '__reverse', 'Graph', 'import']
        flag = True

        for taboo in taboos:
            if taboo in script or taboo in variables:
                flag = False
                break

        if flag:
            exec(variables, globals())
            exec(script, globals())
        else:
            script = None
            variables = None
            result = "NameError: using unavailable expression"

        return JsonResponse({"script": script, "result_variables": variables, "result": result, }, safe=False)
    else:
        return __render(request, 'pyinjs/handling_post_request.html')
###############################################################################################

# Create your views here.

