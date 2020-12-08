from django.test import TestCase
from django.urls import reverse,resolve
from ..views import reply_topic
from ..models import Board, Topic, Post
from ..forms import NewTopicForm, PostForm
from django.contrib.auth.models import User

# Create your tests here.

class ReplyTopicTestCase(TestCase):
    '''
    Base test case to be used in all `reply_topic` view tests
    '''
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(subject='test post', board = self.board, starter = user)
        Post.objects.create(message='topic message', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic',kwargs={'pk':self.board.pk, 'topic_pk': self.topic.pk})

class LoginRequiredReplyTopicTests(ReplyTopicTestCase):

    def test_redirection(self):
        login_url=reverse('login')
        respone=self.client.get(self.url)
        self.assertRedirects(respone,'{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class ReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response=self.client.get(self.url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view=resolve('/boards/1/topics/1/reply/')
        self.assertEquals(view.func, reply_topic)

    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')
     
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input',1)
        self.assertContains(self.response, '<textarea',1)

class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response=self.client.post(self.url, {'message':'hello'})
    
    def test_redirection(self):
        url=reverse('topic_posts', kwargs={'pk':self.board.pk,'topic_pk':self.topic.pk})
        topic_post_url = '{url}?page=1#2'.format(url=url)
        self.assertRedirects(self.response, topic_post_url)

    def test_reply_created(self):
        self.assertEquals(self.board.get_posts_count(),2)

class InvalidReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response=self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    

        