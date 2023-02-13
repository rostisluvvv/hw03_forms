from django.contrib.auth import get_user_model
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
        post = PostModelTest.post

        str_tests = {
            str(group.title): group.title,
            str(post.text): post.text
        }

        for model_field, expected_value in str_tests.items():
            with self.subTest(model_field=model_field):
                self.assertEqual(
                    model_field, expected_value
                )

