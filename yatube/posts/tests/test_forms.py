from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from ..models import Post, Group
from django.urls import reverse

from http import HTTPStatus

User = get_user_model()



class PostCreateFormTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовое описание поста',
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        count_post = Post.objects.count()
        print(count_post)
        form_data = {
            'text': 'Тестовое описание поста',
            'group': self.post.group.pk,

        }
        response = self.authorized_client.post(
            reverse('posts:post_create'), data=form_data)
        print(response)

        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user.username}))
        print(Post.objects.count())

        self.assertEqual(Post.objects.count(), count_post + 1)

        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                text='Тестовое описание поста',
                group=self.post.group.pk
            )
        )


