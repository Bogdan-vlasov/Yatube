from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


USERNAME = 'test'
GROUP_SLUG = 'test-group'
CREATE_POST = reverse('posts:create_post')
PROFILE = reverse('posts:profile', args=[USERNAME])
TEXT = 'Тестовый пост из формы'
NEW_TEXT = 'Новый текст'


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username=USERNAME)
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug=GROUP_SLUG,
            description='Тестовое описание группы'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый пост',
            group=cls.group
        )
        cls.POST_DETAIL = reverse('posts:post_detail',
                                  args=[cls.post.id])
        cls.EDIT_POST = reverse('posts:post_edit',
                                args=[cls.post.id])

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_create_post_in_form(self):
        post_count = Post.objects.count()
        form_data = {'text': TEXT, 'group': self.group.id}
        self.authorized_client.post(CREATE_POST, data=form_data)
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(Post.objects.latest('id').text, TEXT)
        self.assertEqual(Post.objects.latest('id').group, self.group)

    def test_edit_post_in_form(self):
        form_data = {'text': NEW_TEXT, 'group': self.group.id}
        self.authorized_client.post(
            PostFormTests.EDIT_POST,
            data=form_data
        )
        response = self.authorized_client.get(
            PostFormTests.POST_DETAIL
        )
        self.assertEqual(response.context['post'].text, NEW_TEXT)
        self.assertEqual(response.context.get('post').group, self.group)
