from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User

USERNAME = 'test'
GROUP_SLUG = 'test-slug'
HOMEPAGE = reverse('posts:index')
GROUP_LIST = reverse('posts:group_list', args=[GROUP_SLUG])
LOGIN = reverse('login')
PROFILE = reverse('posts:profile', args=[USERNAME])
CREATE_POST = reverse('posts:create_post')
WRONG_PAGE = '/wrong_page/'


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = User.objects.create(username=USERNAME)
        cls.group = Group.objects.create(
            title='test',
            slug=GROUP_SLUG,
            description='test description',
        )
        cls.post = Post.objects.create(
            text='Тестовое описание поста',
            author=cls.test_user
        )
        cls.POST_DETAIL = reverse('posts:post_detail',
                                  args=[cls.post.id])
        cls.EDIT_POST = reverse('posts:post_edit',
                                args=[cls.post.id])

    def setUp(self):
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.test_user)
        self.authorized_non_author = Client()
        self.authorized_non_author.force_login(self.user)

    def test_urls(self):
        client_url_status = [
            [self.client, HOMEPAGE, HTTPStatus.OK],
            [self.client, GROUP_LIST, HTTPStatus.OK],
            [self.authorized_client, CREATE_POST, HTTPStatus.OK],
            [self.client, PROFILE, HTTPStatus.OK],
            [self.client, WRONG_PAGE, HTTPStatus.NOT_FOUND],
            [self.client, PostURLTests.POST_DETAIL, HTTPStatus.OK],
            [self.client, PostURLTests.EDIT_POST, HTTPStatus.FOUND],
            [self.authorized_non_author,
             PostURLTests.EDIT_POST,
             HTTPStatus.FOUND
             ],
            [self.authorized_client, PostURLTests.EDIT_POST, HTTPStatus.OK],
        ]
        for client, url, status_code in client_url_status:
            with self.subTest(client=client, url=url, status_code=status_code):
                self.assertEqual(client.get(url).status_code, status_code)

    def test_urls_correct_templates(self):
        templates_page_names = [
            ['posts/index.html', HOMEPAGE],
            ['posts/group_list.html', GROUP_LIST],
            ['posts/create_post.html', CREATE_POST],
            ['posts/profile.html', PROFILE],
            ['posts/post_detail.html', PostURLTests.POST_DETAIL],
            ['posts/create_post.html', PostURLTests.EDIT_POST],
        ]
        for template, url in templates_page_names:
            with self.subTest(url=url):
                self.assertTemplateUsed(self.authorized_client.get(url),
                                        template)
