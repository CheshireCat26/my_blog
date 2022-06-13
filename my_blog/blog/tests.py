from django.test import TestCase
from .models import Article
from datetime import timedelta
from django.utils import timezone


# Create your tests here.

class ArticleTestCase(TestCase):
    def test_is_add_recently_for_article_in_long_past(self):
        """Articles with pub_date > 7 days from now isn't add recently"""
        article = Article(pub_date=timezone.now() - timedelta(days=7, seconds=1))
        self.assertEqual(article.is_add_recently(), False)

    def test_is_add_recently_for_article_in_future(self):
        """Articles with pub_date in future isn't add recently"""
        article = Article(pub_date=timezone.now() + timedelta(seconds=1))
        self.assertEqual(article.is_add_recently(), False)

    def test_is_add_recently_for_recent_article(self):
        """Articles with pub_date within 7 days from now is recently"""
        article = Article(pub_date=timezone.now() - timedelta(days=6, minutes=59, seconds=59))
        self.assertEqual(article.is_add_recently(), True)
