from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Article, UsersVotes
from datetime import timedelta
from django.utils import timezone


# Create your tests here.

def create_user(username, password):
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()


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
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['article_list'], [])

    def test_past_article(self):
        """If there is article with pub_date <= now() it should be shown"""
        article = Article.objects.create(pub_date=timezone.now())
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context['article_list'], [article])

    def test_future_article(self):
        """Articles with pub_date in future shouldn't be appeared in index page"""
        article = Article.objects.create(pub_date=timezone.now() + timedelta(seconds=1))
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context['article_list'], [])

    def test_future_and_past_article(self):
        """If there is future and past article only past should be appeared"""
        article_future = Article.objects.create(pub_date=timezone.now() + timedelta(seconds=1))
        article_past = Article.objects.create(pub_date=timezone.now() - timedelta(seconds=1))
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context['article_list'], [article_past])

    def test_multiply_article(self):
        """Index page should display all available past article"""
        article_1 = Article.objects.create(pub_date=timezone.now() - timedelta(seconds=1))
        article_2 = Article.objects.create(pub_date=timezone.now() - timedelta(days=15))
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context['article_list'], [article_1, article_2], ordered=False)


class DetailTestCase(TestCase):
    def test_article_detail(self):
        """Detail page should show title and text of the article"""
        article = Article.objects.create(title="title", text='text', pub_date=timezone.now())
        response = self.client.get(reverse('blog:detail', args=(article.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, article.title)
        self.assertContains(response, article.text)

    def test_future_article(self):
        """Detail page should show 404 for article with pub_date in future"""
        article = Article.objects.create(pub_date=timezone.now() + timedelta(seconds=1))
        response = self.client.get(reverse('blog:detail', args=(article.id,)))
        self.assertEqual(response.status_code, 404)


class LoginTestCase(TestCase):
    def test_anonymous_login(self):
        """Login page should be available for anonymous user"""
        response = self.client.get(reverse('blog:login'))
        self.assertEqual(response.status_code, 200)

    def test_logged_login(self):
        """Login page shouldn't be available for logged-in user."""
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('blog:login'))
        self.assertContains(response, "You're already logged-in")


class RegisterTestCase(TestCase):
    def test_anonymous_register(self):
        """Register page should be available for anonymous user"""
        response = self.client.get(reverse('blog:register'))
        self.assertEqual(response.status_code, 200)

    def test_logged_register(self):
        """Register page shouldn't be available for logged-in user"""
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('blog:register'))
        self.assertContains(response, "You're already logged-in")


class TestPanelTestCase(TestCase):
    def test_anonymous_test_panel(self):
        """Test panel shouldn't be available for non-admin user"""
        response = self.client.get(reverse('blog:test_panel'))
        self.assertURLEqual(response.url, reverse('blog:index'))


class VotePostTestCase(TestCase):
    def test_anonymous_vote(self):
        """Anonymous users can't vote"""
        article = Article(pub_date=timezone.now())
        article.save()

        response = self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "True"}))
        self.assertEqual(UsersVotes.objects.filter(post_id=article).count(), 0)

    def test_one_positive_vote_from_one_user(self):
        """One positive vote should add 1 positive vote to article's votes"""
        create_user('testuser', '12345')
        self.client.login(username='testuser', password='12345')

        article = Article(pub_date=timezone.now())
        article.save()

        response = self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "True"}))
        self.assertEqual(UsersVotes.objects.filter(post_id=article).filter(positive=True).count(), 1)

    def test_one_negative_vote_from_one_user(self):
        """One negative vote should add 1 negative vote to article's votes"""
        create_user('testuser', '12345')
        self.client.login(username='testuser', password='12345')

        article = Article(pub_date=timezone.now())
        article.save()

        response = self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "False"}))
        self.assertEqual(UsersVotes.objects.filter(post_id=article).filter(positive=False).count(), 1)

    def test_two_positive_votes_from_one_user(self):
        """If one user send two positive votes for one article second one delete first one"""
        create_user('testuser', '12345')
        self.client.login(username='testuser', password='12345')

        article = Article(pub_date=timezone.now())
        article.save()

        self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "True"}))
        self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "True"}))
        self.assertEqual(UsersVotes.objects.filter(post_id=article).filter(positive=False).count(), 0)

    def test_two_negative_votes_from_one_user(self):
        """If one user send two negative votes for one article second one delete first one"""
        create_user('testuser', '12345')
        self.client.login(username='testuser', password='12345')

        article = Article(pub_date=timezone.now())
        article.save()

        self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "False"}))
        self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "False"}))
        self.assertEqual(UsersVotes.objects.filter(post_id=article).filter(positive=False).count(), 0)

    def test_one_pos_vote_one_neg_vote_from_one_user(self):
        """If user send one positive vote and then one negative vote (or vice-versa) second one delete first one"""
        create_user('testuser', '12345')
        self.client.login(username='testuser', password='12345')

        article = Article(pub_date=timezone.now())
        article.save()

        self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "True"}))
        self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "False"}))
        self.assertEqual(UsersVotes.objects.filter(post_id=article).filter(positive=False).count(), 0)

        self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "False"}))
        self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "True"}))
        self.assertEqual(UsersVotes.objects.filter(post_id=article).filter(positive=False).count(), 0)

    def test_two_votes_from_two_users(self):
        """It should save all votes from different users"""
        article = Article(pub_date=timezone.now())
        article.save()

        create_user("user1", "123")
        self.client.login(username='user1', password='123')
        self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "True"}))

        create_user("user2", "123")
        self.client.login(username='user2', password='123')
        self.client.get(reverse('blog:vote_post', kwargs={'pk': 1, 'positive': "True"}))

        self.assertEqual(UsersVotes.objects.filter(post_id=article).count(), 2)