from django.test import TestCase
from django.urls import reverse,resolve
from ..views import TopicListView
from ..models import Board
from django.contrib.auth.models import User

# Create your tests here.
class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board')

    def test_board_topics_view_status_code(self):
        url = reverse('board_topics',kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
    
    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics',kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code,404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func.view_class, TopicListView)
    
    def test_board_topics_view_contains_link_back_to_homepage(self):
        url = reverse('board_topics',kwargs={'pk':1})
        home_url = reverse('home')
        new_topic_url = reverse('new_topic',kwargs={'pk':1})
        response = self.client.get(url)
        self.assertContains(response,'href="{0}"'.format(home_url))
        self.assertContains(response,'href="{0}"'.format(new_topic_url))