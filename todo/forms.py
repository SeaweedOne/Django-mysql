# forms.py
from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['work', 'done']  # 사용자가 입력할 필드를 지정
