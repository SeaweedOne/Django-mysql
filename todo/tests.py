import pytest
from rest_framework.test import APIClient
from unittest.mock import patch
from .models import Todo
from django.urls import reverse




@pytest.fixture
def api_client():
    return APIClient()



@pytest.fixture
def create_todo():
    return Todo.objects.create(work="Sample Task", done=False)

# Redis 관련된 함수들을 Mocking
@pytest.fixture
def mock_redis_methods():
    with patch('todo.middleware.incrKey') as mock_incr_key, \
         patch('todo.middleware.publish_data_on_redis') as mock_publish:
        yield {
            'incr_key': mock_incr_key,
            'publish': mock_publish
        }


# 테스트 1: Todo 생성 (POST 요청)
def test_add_todo(api_client, mock_redis_methods):
    url = reverse('todo-list')  # 'todo' 엔드포인트 URL
    data = {"work": "New Task", "done": False}

    response = api_client.post(url, data, format='json')

    assert response.status_code == 200
    assert response.data['work'] == "New Task"
    assert response.data['done'] == False
    # Redis 메서드가 호출되었는지 확인
    mock_redis_methods['incr_key'].assert_called_with('POST', 1)


# 테스트 2: Todo 조회 (GET 요청)
def test_get_todos(api_client, create_todo, mock_redis_methods):
    url = reverse('todo-list')  # 'todo' 엔드포인트 URL

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['work'] == "Sample Task"
    # Redis 메서드가 호출되었는지 확인
    mock_redis_methods['incr_key'].assert_called_with('GET', 1)


# 테스트 3: Todo 업데이트 (PUT 요청)
def test_update_todo(api_client, create_todo, mock_redis_methods):
    url = reverse('todo-detail', args=[create_todo.id])
    data = {"work": "Updated Task", "done": True}

    response = api_client.put(url, data, format='json')

    assert response.status_code == 200
    assert response.data['work'] == "Updated Task"
    assert response.data['done'] == True
    # Redis 메서드가 호출되었는지 확인
    mock_redis_methods['incr_key'].assert_called_with('PUT', 1)


# 테스트 4: Todo 삭제 (DELETE 요청)
def test_delete_todo(api_client, create_todo, mock_redis_methods):
    url = reverse('todo-detail', args=[create_todo.id])

    response = api_client.delete(url)

    assert response.status_code == 200
    assert response.data == "deleted"
    # Redis 메서드가 호출되었는지 확인
    mock_redis_methods['incr_key'].assert_called_with('DELETE', 1)