from django.shortcuts import render as __render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from .forms import PostForm
from django.urls import reverse as __reverse
import json

# Библиотеки для приходящего кода
import numpy


result = 888  # глобальная переменная для сохранения в нее результата


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

        # запрещенные библиотеки и оператор import для запрета импортирования модулей внутри
        taboos = ['__render',
                  'HttpResponseRedirect',
                  'JsonResponse',
                  'PostForm',
                  '__reverse',
                  'import',
                  'stderr',
                  'HttpResponseBadRequest']
        flag = True

        for taboo in taboos:
            if taboo in script or taboo in variables:
                flag = False
                break

        exception_flag = False

        if flag:
            ''' Выполнение кода, если не исползуется ничего из taboos '''
            try:
                exec(variables, globals())
                exec(script, globals())
                state['result'] = result
            except ValueError:
                status = '400: Bad Request'
                result = 'ValueError'
                response = HttpResponseBadRequest(result, status=400)
                response.__setitem__(header='status', value=status)
                return response
            except SyntaxError:
                status = '400: Bad Request'
                result = 'SyntaxError'
                response = HttpResponseBadRequest(result, status=400)
                response.__setitem__(header='status', value=status)
                return response
            except NameError:
                status = '400: Bad Request'
                result = 'NameError'
                response = HttpResponseBadRequest(result, status=400)
                response.__setitem__(header='status', value=status)
                return response
            except ZeroDivisionError:
                status = '400: Bad Request'
                result = 'ZeroDivisionError'
                response = HttpResponseBadRequest(result, status=400)
                response.__setitem__(header='status', value=status)
                return response
            except MemoryError:
                status = '400: Bad Request'
                result = 'MemoryError'
                response = HttpResponseBadRequest(result, status=400)
                response.__setitem__(header='status', value=status)
                return response
            except ModuleNotFoundError:
                status = '400: Bad Request'
                result = 'ModuleNotFoundError'
                response = HttpResponseBadRequest(result, status=400)
                response.__setitem__(header='status', value=status)
                return response

        else:
            script = None
            variables = None
            result = "AcceptError: using unavailable expression"
            state['result'] = result

        return JsonResponse({"script": script, "result_variables": variables, "state": state, }, safe=False)
    else:
        return __render(request, 'pyinjs/handling_post_request.html')
###############################################################################################

# Create your views here.

