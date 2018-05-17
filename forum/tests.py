from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase
from .views import forum, forum_topics, new_topic
from .models import Board, Topic, Post

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

    def test_forum_topics_url_resolves_board_topics_view(self):
        view = resolve('/forum/1/')
        self.assertEquals(view.func, forum_topics)

    def test_forum_topics_view_contains_return_link(self):
        forum_topics_url = reverse('forum_topics', kwargs={'pk':1})
        response = self.client.get(forum_topics_url)
        homepage_url = reverse('forum')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
    
    def test_board_topics_view_contains_nav_links(self):
        forum_topics_url = reverse('forum_topics', kwargs={'pk':1})
        forum_url = reverse('forum')
        new_topic_url = reverse('new_topic', kwargs={'pk':1})

        response = self.client.get(forum_topics_url)

        self.assertContains(response, 'href="{0}"'.format(forum_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))

class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name="Legend of Zelda", description="LoZ discussion board")
        User.objects.create_user(username='max', email='max@payne.com', password='123')

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/forum/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk':1})
        forum_topics_url = reverse('forum_topics', kwargs={'pk':1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(forum_topics_url))

    def test_csrf(self):
        '''
        Html must have csrf token
        '''
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject':'Test Title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())
    
    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        Expected behavior is to show form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        Expected behavior is to show form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk':1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())