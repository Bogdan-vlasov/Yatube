from django import forms
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

USERNAME = 'test'
INDEX = reverse('posts:index')
GROUP_SLUG = 'test-group'
GROUP = reverse('posts:group_list', args=[GROUP_SLUG])
SECOND_GROUP_SLUG = 'second-test-group'
SECOND_GROUP_URL = reverse('posts:group_list', args=[SECOND_GROUP_SLUG])
CREATE_POST = reverse('posts:create_post')
PROFILE = reverse('posts:profile', args=[USERNAME])


class PostViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = User.objects.create(username=USERNAME)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.test_user)
        cls.group = Group.objects.create(
            title='Заголовок',
            slug=GROUP_SLUG,
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовое описание поста',
            author=cls.test_user,
            group=cls.group
        )
        cls.POST_DETAIL = reverse('posts:post_detail',
                                  args=[cls.post.id])
        cls.EDIT_POST = reverse('posts:post_edit',
                                args=[cls.post.id])

    def test_views_correct_templates(self):
        templates_page_names = [
            ['posts/index.html', INDEX],
            ['posts/group_list.html', GROUP],
            ['posts/create_post.html', CREATE_POST],
            ['posts/profile.html', PROFILE],
            ['posts/post_detail.html', PostViewTests.POST_DETAIL],
            ['posts/create_post.html', PostViewTests.EDIT_POST],
        ]
        for template, url in templates_page_names:
            with self.subTest(url=url):
                self.assertTemplateUsed(self.authorized_client.get(url),
                                        template)

    def test_new_post_on_pages(self):
        urls_pages = [INDEX, GROUP, PROFILE]
        expect_context = self.post
        for url in urls_pages:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(len(response.context['page_obj']), 1)
                entering_context = response.context['page_obj'][0]
                self.assertEqual(entering_context, expect_context)

    def test_new_post_with_other_group(self):
        Group.objects.create(
            title='Другой заголовок',
            slug=SECOND_GROUP_SLUG,
            description='Другое тестовое описание',
        )
        response = self.authorized_client.get(SECOND_GROUP_URL)
        self.assertNotIn(PostViewTests.post, response.context['page_obj'])

    def test_profile_correct_context(self):
        response = self.authorized_client.get(PROFILE)
        self.assertEqual(response.context['author'], PostViewTests.test_user)

    def test_index_correct_context(self):
        response = self.authorized_client.get(INDEX)
        object_post_list = response.context['page_obj'].object_list
        self.assertTrue(self.post in object_post_list)

    def test_group_posts_correct_context(self):
        response = self.authorized_client.get(GROUP)
        object_page_obj = response.context['page_obj']
        self.assertEqual(
            object_page_obj.object_list[0].group,
            self.group)
        self.assertEqual(len(object_page_obj.object_list), 1)

    def test_post_detail_correct_context(self):
        response = self.authorized_client.get(PostViewTests.POST_DETAIL)
        self.assertEqual(response.context['post'], PostViewTests.post)
        self.assertEqual(response.context['author'], PostViewTests.test_user)

    def test_paginator_correct_context(self):
        Post.objects.bulk_create(
            [Post(author=self.test_user, text='T',
                  group_id=self.group.id)
             ] * 15
        )
        name_pages = [INDEX, GROUP, PROFILE]
        for name_page in name_pages:
            with self.subTest(reverse_name=name_page):
                response = self.client.get(name_page)
                posts_in_page = len(response.context['page_obj'].object_list)
                self.assertEqual(posts_in_page, settings.POST_COUNT)

    def test_new_and_edit_post_page_context(self):
        urls = [
            CREATE_POST,
            PostViewTests.EDIT_POST]
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                for value, expected in form_fields.items():
                    form_field = response.context['form'].fields.get(value)
                    self.assertIsInstance(form_field, expected)
