from django.test import TestCase
from .models import Article
from datetime import timedelta
from django.utils import timezone


# Create your tests here.

class ArticleTestCase(TestCase):
    """Articles with pub_date > 7 days isn't add recently"""
    def test_is_add_recently_for_article_in_long_past(self):
        article = Article(pub_date=timezone.now() - timedelta(days=7, seconds=1))
        self.assertEqual(article.is_add_recently(), False)
