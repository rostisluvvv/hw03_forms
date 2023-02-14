from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group


User = get_user_model()


class PostPagesTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='NoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(
            author=self.user,
            text='Тестовое описание поста',
            )
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание'
        )

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

    def test_post_added_correctly(self):
        post = Post.objects.create(
            author=self.user,
            text='Тестовое описание поста',
            group=self.group)
        response_index = self.authorized_client.get(reverse('posts:index'))

        response_group = self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': f'{self.group.slug}'}))

        response_profile = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': f'{self.user.username}'}))

        index = response_index.context['page_obj']
        group = response_group.context['page_obj']
        profile = response_profile.context['page_obj']
        self.assertIn(post, index)
        self.assertIn(post, group)
        self.assertIn(post, profile)

    def test_index_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response.context.get('page_obj')[0].text,
                         'Тестовое описание поста')

        self.assertEqual(response.context.get('page_obj')[0].author,
                         self.user)

    def test_group_posts_context(self):
        response = self.authorized_client.get(reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        self.assertEqual(response.context.get('group')[0].title, 'Тестовая группа')


TEST_OF_POST: int = 13
COUNT_POST_FIRST_PAGE: int = 10
COUNT_POST_SECOND_PAGE: int = 3


class PaginatorViewTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='NoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title='test group',
            slug='test_slug'
        )
        blank_post: list = []
        for i in range(TEST_OF_POST):
            blank_post.append(Post(text=f'test text {i}',
                                   group=self.group,
                                   author=self.user))
        Post.objects.bulk_create(blank_post)

    def test_index_first_page_contains_ten_records(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']),
                         COUNT_POST_FIRST_PAGE)

    def test_index_second_page_contains_three_records(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']),
                         COUNT_POST_SECOND_PAGE)

    def test_group_first_page_contains_ten_records_group(self):
        response = self.authorized_client.get(reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        self.assertEqual(len(response.context['page_obj']),
                         COUNT_POST_FIRST_PAGE)

    def test_group_second_page_contains_three_records(self):
        response = self.authorized_client.get(reverse('posts:group_list', kwargs={'slug': self.group.slug}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']),
                         COUNT_POST_SECOND_PAGE)