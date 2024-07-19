# test/test_app.py

import unittest
import os
os.environ["TESTING"] = "true"

from app import app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

        # Clear existing timeline posts before each test
        self.clear_timeline_posts()
    
    # This will clear timeline posts in the test database
    def clear_timeline_posts(self):
        from app import TimelinePost
        TimelinePost.delete().execute()
    
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        # TODO: Add more tests related to the home page
        assert '<a class="nav-item nav-link active" href="/">About Me' in html
        assert '<a class="nav-item nav-link" href="/work"> Work and Education </a>' in html
        assert '<a class="nav-item nav-link" href="/hobbies"> Hobbies </a>' in html

    def test_timeline(self):
        response = self.client.get('/api/timeline_post')
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        # TODO: Add more tests related to the api/timeline_post GET and POST apis
    
    def test_post_timeline(self):
        response = self.client.post('/api/timeline_post', data={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "content": "Hello World, I'm Jane!"
        })
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json["name"] == "Jane Doe"
        assert json["email"] == "jane@example.com"
        assert json["content"] == "Hello World, I'm Jane!"
        # TODO: Add more tests relating to the timeline page

    def test_timeline_page(self):
        response = self.client.get('/timeline')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<h2>Messages</h2>' in html
    
    def test_malformed_timeline_post(self):
        response = self.client.post('/api/timeline_post', data={"email": "john@example.com", "content": "Hello World, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post('/api/timeline_post', data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post('/api/timeline_post', data={"name": "John Doe", "email": "not-an-email", "content": "Hello World, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
