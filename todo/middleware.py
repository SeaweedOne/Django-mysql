import django_rq
from .cache_function import getKey, incrKey, addKey, setKey, deleteKey, getAllKey
from .pubsub import publish_data_on_redis


def middleware(get_response):
    #here code for intialize
    addKey("GET", 0)
    addKey("POST", 0)
    addKey("PUT", 0)
    addKey("DELETE", 0)

    def middlewareFunction(request):
        #before api hit
        queue = django_rq.get_queue("default", default_timeout=800)
        queue.enqueue(incrKey, args=(request.method, 1))
        response = get_response(request)
        print(response)
        test = {"response" : response.status_code, "req": request.method}
        #after api hit
        publish_data_on_redis(test, "notify")
        return response

    return middlewareFunction