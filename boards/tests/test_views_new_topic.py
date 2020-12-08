from django.test import TestCase
from django.urls import reverse,resolve
from ..views import new_topic
from ..models import Board, Topic, Post
from ..forms import NewTopicForm
from django.contrib.auth.models import User

# Create your tests here.

class NewTopicTest(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board')
        User.objects.create_user(username='john', email='john@mail.com', password='abcdef123456') 
        self.client.login(username='john', password='abcdef123456')  

    def test_new_topic_view_status_code(self):
        url = reverse('new_topic', kwargs={'pk':1}) 
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)

    def test_new_topics_view_not_found_status_code(self):
        url = reverse('new_topic',kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code,404)
    
    def test_new_topics_url_resolves_new_topics_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topics_view_contains_link_back_to_board_topics_view(self):
        url  = reverse('new_topic', kwargs={'pk':1}) 
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response  = self.client.get(url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        url = reverse('new_topic',kwargs={'pk':1})
        response = self.client.post(url,{})
        form = response.context.get('form')
        self.assertEquals(response.status_code,200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_empty_data(self):
        url = reverse('new_topic', kwargs={'pk':1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code,200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url = reverse('new_topic',kwargs={'pk':1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form,NewTopicForm)

class LoginRequiredNewtopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board')
        self.url = reverse('new_topic', kwargs={'pk':1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=url, url=self.url))