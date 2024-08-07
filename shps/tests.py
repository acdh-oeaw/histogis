from django.apps import apps
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


MODELS = list(apps.all_models["shps"].values())

client = Client()
USER = {"username": "testuser", "password": "somepassword"}


class ArchivTestCase(TestCase):
    fixtures = ["dump.json"]

    def setUp(self):
        # Create two users
        User.objects.create_user(**USER)

    def test_002_listviews(self):
        for x in MODELS:
            try:
                url = x.get_listview_url()
            except AttributeError:
                url = False
            if url:
                response = client.get(url)
                self.assertEqual(response.status_code, 200)
        client.login(**USER)
        for x in MODELS:
            try:
                url = x.get_listview_url()
            except AttributeError:
                url = False
            if url:
                response = client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_003_detailviews(self):
        for x in MODELS:
            item = x.objects.first()
            try:
                url = item.get_absolute_url()
            except AttributeError:
                url = False
            if url:
                response = client.get(url, {"pk": item.id})
                self.assertEqual(response.status_code, 200)

    def test_004_editviews(self):
        client.login(**USER)
        for x in MODELS:
            item = x.objects.first()
            try:
                url = item.get_edit_url()
            except AttributeError:
                url = False
            if url:
                response = client.get(url, {"pk": item.id})
                self.assertEqual(response.status_code, 200)

    def test_005_createviews_not_logged_in(self):
        for x in MODELS:
            item = x.objects.first()
            try:
                url = item.get_createview_url()
            except AttributeError:
                url = False
            if url:
                response = client.get(url, {"pk": item.id})
                self.assertEqual(response.status_code, 302)

    def test_006_createviews_logged_in(self):
        client.login(**USER)
        for x in MODELS:
            item = x.objects.first()
            try:
                url = item.get_createview_url()
            except AttributeError:
                url = False
            if url:
                response = client.get(url, {"pk": item.id})
                self.assertEqual(response.status_code, 200)

    def test_007_where_was(self):
        url = reverse("where_was_api")
        r = client.get(url)
        self.assertFalse(r.json()["features"])

        params = {"lat": "48.36", "lng": "14.3"}
        r = client.get(url, params)
        self.assertTrue(r.json()["features"])

        params = {"lat": "48.36", "lng": "14.3", "when": "1870-01-01"}
        r = client.get(url, params)
        self.assertTrue(r.json()["features"])

        params = {"lat": "48.36", "lng": "14.3", "when": "187110-01-01"}
        r = client.get(url, params)
        self.assertTrue(r.json()["features"])

    def test_008_shps_api_filters(self):
        url = "/api/tempspatial/"
        params = {
            "name": "Linz",
        }
        r = client.get(url)
        all_shapes = r.json()["count"]
        r = client.get(url, params)
        some_shapes = r.json()["count"]
        self.assertTrue(all_shapes > some_shapes)
