from django.contrib.auth import get_user_model
from django.db.models import get_app, get_models
from django.test import TestCase

from ..models import Post, Group


User = get_user_model()


class PostModelTest(TestCase):
    """Class testing post model"""

    @classmethod
    def setUp(cls) -> None:
        super().setUpClass()

        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост'
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        self.assertEqual(str(group.title), group.title)
