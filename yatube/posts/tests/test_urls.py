from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post


User = get_user_model()


class PostsURLTests(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        Post.objects.create(
            author=cls.user,
            text='Тестовый пост'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test__urls_uses_correct_template(self):
        templates_url_names = {
            'http://127.0.0.1:8000/': '/',
            'http://127.0.0.1:8000/group/<slug>/': '/group/<slug>/',
            'http://127.0.0.1:8000/profile/<username>/': '/profile<username>',
            'http://127.0.0.1:8000/posts/<post_id>/': '/posts/<post_id>/',
            'http://127.0.0.1:8000/posts/<post_id>/edit/': '/posts/<post_id>/edit/',
            'http://127.0.0.1:8000/create/': '/create/',
        }
        for page, address in templates_url_names.items():
            with self.subTest(address=address):
                if '/create/' in page:
                    response = self.authorized_client.get(address)
                else:
                    response = self.guest_client.get(address)
                self.assertEqual(response.status_code, 200)




