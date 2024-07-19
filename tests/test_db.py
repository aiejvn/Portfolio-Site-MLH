# test_db.py

import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(
            name="John Doe",
            email="john@example.com",
            content="Hello World! I'm John Doe."
        )
        assert first_post.id == 1
        second_post = TimelinePost.create(
            name="Jane Doe",
            email="jane@example.com",
            content="Hello World! I'm Jane Doe."
        )
        assert second_post.id == 2
        
        # TODO: Get the timeline posts and assert that they are in the correct order
        timeline_posts = TimelinePost.select().order_by(TimelinePost.created_at.asc())
        assert timeline_posts.count() == 2

        first_retrieved = timeline_posts[0]
        second_retrieved = timeline_posts[1]

        assert first_retrieved.id == 1
        assert first_retrieved.name == "John Doe"
        assert first_retrieved.email == "john@example.com"
        assert first_retrieved.content == "Hello World! I'm John Doe."

        assert second_retrieved.id == 2
        assert second_retrieved.name == "Jane Doe"
        assert second_retrieved.email == "jane@example.com"
        assert second_retrieved.content == "Hello World! I'm Jane Doe."