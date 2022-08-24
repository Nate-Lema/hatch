from django.test import TestCase
from django.urls import reverse
from config.consts import *
from unittest import mock
from posts.mock import side_effect_parallel_requests


# Mock the external api response
@mock.patch('parallel_requests.get', side_effect=side_effect_parallel_requests)
class PostTests(TestCase):

    def test_error_no_tags(self, mock_parallel_requests):
        response = self.client.get('/api/posts')
        response_json = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['error'], 'Tags parameter is required')

    def test_error_invalid_sortby(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=tech&sortBy=xxx')
        response_json = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['error'], 'sortBy parameter is invalid')

    def test_error_invalid_direction(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=tech&sortBy=id&direction=xxx')
        response_json = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['error'], 'direction parameter is invalid')

    def test_error_external_url_is_not_working(self, mock_parallel_requests):
        # When tag is `show_error`, Mock api return a 404 error
        response = self.client.get('/api/posts?tags=show_error')
        response_json = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['error'], 'Could not connect to external API')

    def test_tech_tags_pass(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=tech')
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json['posts']), 28)
        self.assertEqual(response_json['posts'][0]['id'], 1)
        self.assertEqual(response_json['posts'][1]['id'], 2)
        self.assertEqual(response_json['posts'][2]['id'], 4)

    def test_science_tags_pass(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=science')
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json['posts']), 25)
        self.assertEqual(response_json['posts'][0]['id'], 4)
        self.assertEqual(response_json['posts'][1]['id'], 6)
        self.assertEqual(response_json['posts'][2]['id'], 7)

    def test_tags_duplicate_pass(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=tech,tech')
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json['posts']), 28)

    def test_sort_id_asc_pass(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=tech&direction=asc')
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['posts'][0]['id'], 1)
        self.assertEqual(response_json['posts'][1]['id'], 2)
        self.assertEqual(response_json['posts'][2]['id'], 4)

    def test_sort_id_desc_pass(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=tech&sortBy=id&direction=desc')
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['posts'][0]['id'], 99)
        self.assertEqual(response_json['posts'][1]['id'], 95)
        self.assertEqual(response_json['posts'][2]['id'], 93)

    def test_sort_reads_asc_pass(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=tech&sortBy=reads&direction=asc')
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['posts'][0]['id'], 54)
        self.assertEqual(response_json['posts'][1]['id'], 77)
        self.assertEqual(response_json['posts'][2]['id'], 82)

    def test_sort_reads_desc_pass(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=tech&sortBy=reads&direction=desc')
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['posts'][0]['id'], 51)
        self.assertEqual(response_json['posts'][1]['id'], 99)
        self.assertEqual(response_json['posts'][2]['id'], 2)

    def test_sort_likes_asc_pass(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=tech&sortBy=likes&direction=asc')
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['posts'][0]['id'], 85)
        self.assertEqual(response_json['posts'][1]['id'], 46)
        self.assertEqual(response_json['posts'][2]['id'], 37)

    def test_sort_likes_desc_pass(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=tech&sortBy=likes&direction=desc')
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['posts'][0]['id'], 95)
        self.assertEqual(response_json['posts'][1]['id'], 18)
        self.assertEqual(response_json['posts'][2]['id'], 59)

    def test_sort_popularity_asc_passes(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=tech&sortBy=popularity&direction=asc')
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['posts'][0]['id'], 51)
        self.assertEqual(response_json['posts'][1]['id'], 76)
        self.assertEqual(response_json['posts'][2]['id'], 43)

    def test_sort_popularity_desc(self, mock_parallel_requests):
        response = self.client.get('/api/posts?tags=tech&sortBy=popularity&direction=desc')
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['posts'][0]['id'], 46)
        self.assertEqual(response_json['posts'][1]['id'], 4)
        self.assertEqual(response_json['posts'][2]['id'], 15)
