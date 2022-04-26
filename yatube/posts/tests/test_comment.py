from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Comment, Post, User

USERNAME = 'test'


class CommentTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = User.objects.create(username=USERNAME)
        cls.post = Post.objects.create(
            text='Тестовое описание поста',
            author=cls.test_user,
        )
        cls.ADD_COMMENT_URL = reverse('posts:add_comment',
                                      args=[cls.post.id])

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.test_user)

    def test_authorized_client_comment(self):
        text_comment = 'Тестовый комментарий'
        self.authorized_client.post(CommentTests.ADD_COMMENT_URL,
                                    data={'text': text_comment}
                                    )
        comment = Comment.objects.filter(post=CommentTests.post).last()
        self.assertEqual(comment.text, text_comment)
        self.assertEqual(comment.author, CommentTests.test_user)

    def test_guest_client_comment_redirect_login(self):
        count_comments = Comment.objects.count()
        self.client.post(CommentTests.ADD_COMMENT_URL)
        self.assertEqual(count_comments, Comment.objects.count())
