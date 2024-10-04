import json
import redis
from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        r = redis.StrictRedis(host='localhost', port=6379, db=1)
        p = r.pubsub()
        p.psubscribe("notify")
        for message in p.listen():
            if message:
                if isinstance(message.get("data"), int):
                    self.stdout.write(f"[notify] message >> init, {message.get('data')}")
                    continue

                request_method = json.loads(message.get("data").decode('utf-8'))
                message["cache"] = cache.get(request_method)
                self.stdout.write(self.style.SUCCESS(f"[notify] message >> {message}"))