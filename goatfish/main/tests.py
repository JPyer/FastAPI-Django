from django.test import TestCase

# Create your tests here.

# We use this as TestCase doesn't work.
from django.test import TransactionTestCase
from django.test.runner import DiscoverRunner
from fastapi.testclient import TestClient

from .models import User
from goatfish.wsgi import app


# A convenient helper for getting URL paths by name.
reverse = app.router.url_path_for


class TestRunner(DiscoverRunner):
    def teardown_databases(self, old_config, **kwargs):
        # This is necessary because either FastAPI/Starlette or Django's
        # ORM isn't cleaning up the connections after it's done with
        # them.
        # The query below kills all database connections before
        # dropping the database.
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT
                pg_terminate_backend(pid) FROM pg_stat_activity WHERE
                pid <> pg_backend_pid() AND
                pg_stat_activity.datname =
                  '{settings.DATABASES["default"]["NAME"]}';"""
            )
            print(f"Killed {len(cursor.fetchall())} stale connections.")
        super().teardown_databases(old_config, **kwargs)


class SmokeTests(TransactionTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Warning: Naming this `self.client` leads Django to overwrite it
        # with its own test client.
        self.c = TestClient(app)

    def setUp(self):
        self.user = User.objects.create(username="user", api_key="mykey")
        self.headers = {"X-API-Key": self.user.api_key}

    def test_read_main(self):
        response = self.c.get(reverse("simulations-get"), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"username": "user"})