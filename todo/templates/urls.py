from django.urls import path

from .views import TodoViewSet

urlpatterns = [
    path("todo", TodoViewSet.as_view({"get": "get", "post": "add"})),
    path("todo/create", TodoViewSet.as_view({"get": "create", "post": "create"}),  name="todo_create"),
    path("todo/create-form", TodoViewSet.as_view({"get": "create_form", "post": "create_form"}),
         name="todo_create_form"),
    path("todo/list", TodoViewSet.as_view({"get": "list"}), name="list"),
    path("todo/list-todo", TodoViewSet.as_view({"get": "list_todos"}), name="todo_list"),
    path("todoAllCache/<str:key>", TodoViewSet.as_view({"get": "getCache"})),
    path("getKey/<str:key>", TodoViewSet.as_view({"get": "getKey"})),
    path("todo/<str:pk>", TodoViewSet.as_view({"put": "update", "delete": "remove"}))
]