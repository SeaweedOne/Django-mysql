from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from .tasks import get, remove, add, update, create
from .cache_function import getAllKey, getKey
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .cache_function import get_todo_list_from_cache, set_todo_list_to_cache, invalidate_todo_cache

# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets, status
from django.shortcuts import render, redirect
from .forms import TodoForm
from .models import Todo

class TodoViewSet(viewsets.ViewSet):
    def create(self, request):
        if request.method == 'POST':
            form = TodoForm(request.POST)
            if form.is_valid():  # 폼 유효성 검사
                # form.cleaned_data를 request.data로 변환하여 add 함수 호출
                data = {
                    'work': form.cleaned_data['work'],
                    'done': form.cleaned_data['done']
                }
                add_response = add(request=request._request)  # request._request로 raw HttpRequest 전달
                return redirect('todo_list')  # 생성 후 리스트 페이지로 리디렉션
        else:
            form = TodoForm()  # GET 요청일 경우 빈 폼 렌더링
        return render(request, 'todo_create.html', {'form': form})


    def create_form(self, request):
        if request.method == 'POST':
            form = TodoForm(request.POST)
            if form.is_valid():
                form.save()
                invalidate_todo_cache()
                return redirect('todo_list')  # 생성 후 리스트 페이지로 리디렉션
        else:
            form = TodoForm()
        return render(request, 'todo_create.html', {'form': form})


    def list_todos(self,request):
        todos = get_todo_list_from_cache()

        if todos is None:
            print("no cache")
            # 2. Redis에 데이터가 없으면 DB에서 데이터를 가져옴
            todos = get()

            # 3. 가져온 데이터를 Redis에 캐싱
            set_todo_list_to_cache(todos)
        else:
            print("cache")
            # 4. Redis에서 가져온 데이터는 이미 시리얼라이즈된 상태이므로 그대로 반환
        return render(request, 'todo_list.html', {'todos': todos})



    def list(self,request):
        todos = get_todo_list_from_cache()

        if todos is None:
            print("no cache")
            # 2. Redis에 데이터가 없으면 DB에서 데이터를 가져옴
            todos = get()

            # 3. 가져온 데이터를 Redis에 캐싱
            set_todo_list_to_cache(todos)
        else:
            print("cache")
            # 4. Redis에서 가져온 데이터는 이미 시리얼라이즈된 상태이므로 그대로 반환
            return Response(todos)

        return Response(todos)

    def get(self, request):
        data = get()
        return Response(data)

    def add(self, request):
        data = add(request)
        invalidate_todo_cache()
        return Response(data)

    def update(self, request, pk=None):
        data = update(request, pk)
        invalidate_todo_cache()
        return Response(data)

    def remove(self, request, pk=None):
        data = remove(request, pk)
        invalidate_todo_cache()
        return Response(data)

    def getCache(self, request, key="*"):
        return Response(getAllKey(key))

    def getKey(self, request, key="*"):
        return Response(getKey(key))