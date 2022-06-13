from django.test import TestCase
from .models import Article
from datetime import timedelta
from django.utils import timezone


# Create your tests here.

class ArticleTestCase(TestCase):
    def test_is_add_recently_for_article_in_long_past(self):
        """Articles with pub_date > 7 days isn't add recently"""
        article = Article(pub_date=timezone.now() - timedelta(days=7, seconds=1))
        self.assertEqual(article.is_add_recently(), False)

    def test_is_add_recently_for_article_in_future(self):
        """Article with pub_date in future isn't add recently"""
        article = Article(pub_date=timezone.now() + timedelta(seconds=1))
        self.assertEqual(article.is_add_recently(), False)
