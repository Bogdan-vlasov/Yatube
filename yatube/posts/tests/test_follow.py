from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Follow, Post, User

PUPA = 'test_pupa'
LUPA = 'test_lupa'
FOLLOW_PUPA = reverse('posts:profile_follow', args=[PUPA])
UNFOLLOW_PUPA = reverse('posts:profile_unfollow', args=[PUPA])
FOLLOW_INDEX = reverse('posts:follow_index')


class FollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user_pupa = User.objects.create(username=PUPA)
        cls.test_user_lupa = User.objects.create(username=LUPA)
        cls.post = Post.objects.create(
            text='Тестовое описание поста',
            author=cls.test_user_pupa,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.test_user_lupa)

    def test_follow(self):
        self.authorized_client.get(FOLLOW_PUPA)
        self.assertTrue(Follow.objects.filter(
            user=FollowTests.test_user_lupa,
            author=FollowTests.test_user_pupa).exists())

    def test_unfollow(self):
        Follow.objects.create(user=FollowTests.test_user_lupa,
                              author=FollowTests.test_user_pupa)
        self.authorized_client.get(UNFOLLOW_PUPA, follow=True)
        self.assertFalse(Follow.objects.filter(
            user=FollowTests.test_user_lupa,
            author=FollowTests.test_user_pupa).exists())

    def test_view_post_followed_users(self):
        Follow.objects.create(user=FollowTests.test_user_lupa,
                              author=FollowTests.test_user_pupa)
        response_lupa = self.authorized_client.get(FOLLOW_INDEX)
        context_lupa = response_lupa.context['page_obj']
        self.assertIn(FollowTests.post, context_lupa)

    def test_do_not_view_post_unfollowed_users(self):
        authorized_client_pupa = Client()
        authorized_client_pupa.force_login(self.test_user_lupa)
        response_pupa = authorized_client_pupa.get(FOLLOW_INDEX)
        self.assertNotIn(FollowTests.post,
                         response_pupa.context['page_obj'])
