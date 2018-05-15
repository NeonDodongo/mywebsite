from django.urls import reverse, resolve
from django.test import TestCase
from .views import forum, forum_topics
from .models import Board

# Create your tests here.
class ForumTests(TestCase):
    # Create new board for testing
    def setUp(self):
        self.board = Board.objects.create(name='Zelda', description='Legend of Zelda board.')
        url = reverse('forum')
        self.response = self.client.get(url)

    def test_forum_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_forum_url_resolves_home_view(self):
        view = resolve('/forum/')
        self.assertEquals(view.func, forum)

    def test_forum_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('forum_topics', kwargs={'pk':self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

class ForumTopicTests(TestCase):
    # Create new board for testing
    def setUp(self):
        Board.objects.create(name='Zelda', description='Legend of Zelda board.')
    
    def test_forum_topics_view_success_status_code(self):
        url = reverse('forum_topics', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_forum_topics_view_not_found_status_code(self):
        url = reverse('forum_topics', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/forum/1/')
        self.assertEquals(view.func, forum_topics)