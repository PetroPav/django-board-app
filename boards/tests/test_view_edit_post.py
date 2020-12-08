from django.test import TestCase
from django.urls import reverse,resolve
from ..views import PostUpdateView
from ..models import Board, Topic, Post
from ..forms import NewTopicForm, PostForm
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your tests here.

class PostUpdateViewTestCase(TestCase):
    '''
    Base test case to be used in all `edit_topic` view tests
    '''
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(subject='test post', board = self.board, starter = user)
        self.post = Post.objects.create(message = 'this is a test post', topic = self.topic, created_by = user)
        self.url = reverse('edit_post',kwargs={'pk':self.board.pk, 'topic_pk': self.topic.pk, 'post_pk': self.post.pk})

class LoginRequiredPostUpdateTests(PostUpdateViewTestCase):
    def test_redirection(self):
        '''
        Test if only logged in users can edit the posts
        '''
        login_url=reverse('login')
        respone=self.client.get(self.url)
        self.assertRedirects(respone,'{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        '''
        Create a new user different from the one who posted
        '''
        super().setUp()
        username = 'user'
        pwd = 'strong'
        user = User.objects.create_user(username=username, email='user@test.com', password=pwd)
        self.client.login(username=username, password=pwd)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        '''
        Accessing edit_post view should return error (404)
        '''
        self.assertEquals(self.response.status_code, 404)

class PostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response=self.client.get(self.url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view=resolve('/boards/1/topics/1/posts/1/edit/')
        self.assertEquals(view.func.view_class, PostUpdateView)

    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')
     
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input',1)
        self.assertContains(self.response, '<textarea',1)

class SuccessfulPostUpdateTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response=self.client.post(self.url, {'message':'update post'})
    
    def test_redirection(self):
        topic_post_url=reverse('topic_posts', kwargs={'pk':self.board.pk,'topic_pk':self.topic.pk})
        self.assertRedirects(self.response, topic_post_url)

    def test_post_updated(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.message, 'update post')

class InvalidPostUpdateTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response=self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    