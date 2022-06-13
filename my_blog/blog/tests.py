from django.test import TestCase
from .models import Article
from datetime import timedelta
from django.utils import timezone
from django.test import Client


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


class IndexTestCase(TestCase):
    def test_empty_index_page(self):
        """If there is no article index page should be empty"""
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['article_list'], [])

    def test_past_article(self):
        """If there is article with pub_date <= now() it should be shown"""
        article = Article.objects.create(pub_date=timezone.now())
        response = self.client.get('/blog/')
        self.assertQuerysetEqual(response.context['article_list'], [article])

    def test_future_article(self):
        """Articles with pub_date in future shouldn't be appeared in index page"""
        article = Article.objects.create(pub_date=timezone.now() + timedelta(seconds=1))
        response = self.client.get('/blog/')
        self.assertQuerysetEqual(response.context['article_list'], [])

    def test_future_and_past_article(self):
        """If there is future and past article only past should be appeared"""
        article_future = Article.objects.create(pub_date=timezone.now() + timedelta(seconds=1))
        article_past = Article.objects.create(pub_date=timezone.now() - timedelta(seconds=1))
        response = self.client.get('/blog/')
        self.assertQuerysetEqual(response.context['article_list'], [article_past])
