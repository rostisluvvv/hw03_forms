from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from ..models import Post, Group

User = get_user_model()


class PostPagesTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание'
        )

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='NoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(
            author=self.user,
            text='Тестовое описание поста')

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names: dict = {
            reverse('posts:index'): 'posts/index.html',

            reverse('posts:group_list', kwargs={'slug': 'test_slug'}): (
                'posts/group_list.html'
            ),

            reverse('posts:profile', kwargs={'username': self.user}): (
                'posts/profile.html'
            ),

            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}): (
                'posts/post_detail.html'
            ),

            reverse('posts:post_create'): 'posts/create_post.html',

            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}): (
                'posts/create_post.html'
            )
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""

        response = self.authorized_client.get(reverse('posts:index'))

        form_fields: dict = {
            'text': forms.fields.CharField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
