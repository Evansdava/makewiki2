# wiki/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from wiki.models import Page


class PageListViewTests(TestCase):
    def test_multiple_pages(self):
        # Make some test data to be displayed on the page.
        user = User.objects.create()

        Page.objects.create(title="My Test Page", content="test", author=user)
        Page.objects.create(title="Another Test Page", content="test",
                            author=user)

        # Issue a GET request to the MakeWiki homepage.
        # When we make a request, we get a response back.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the number of pages passed to the template
        # matches the number of pages we have in the database.
        responses = response.context['pages']
        self.assertEqual(len(responses), 2)

        self.assertQuerysetEqual(
            responses,
            ['<Page: My Test Page>', '<Page: Another Test Page>'],
            ordered=False
        )


class PageDetailViewTests(TestCase):
    def test_single_page(self):
        # Create a test page
        user = User.objects.create()

        page = Page(title="Test Page", content="Test", author=user)
        page.save()

        response = self.client.get(reverse('wiki-details-page',
                                   args=[page.slug]))

        self.assertEqual(response.status_code, 200)

    def test_new_page_form(self):
        response = self.client.get(reverse('wiki-new-page'))
        self.assertIn(b'Title of your page', response.content)

    def test_create_page(self):
        user = User.objects.create()
        args = {'title': "Test Page", 'content': 'TEST', 'author': user.id}

        response = self.client.post(reverse('wiki-new-page'), args)

        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        responses = response.context['pages']
        self.assertQuerysetEqual(responses, ['<Page: Test Page>'])


class WikiTestCase(TestCase):
    def test_true_is_true(self):
        """ Tests if True is equal to True. Should always pass. """
        self.assertEqual(True, True)

    def test_page_slugify_on_save(self):
        """ Tests the slug generated when saving a Page. """
        # Author is a required field in our model.
        # Create a user for this test and save it to the test database.
        user = User()
        user.save()

        # Create and save a new page to the test database.
        page = Page(title="My Test Page", content="test", author=user)
        page.save()

        # Make sure the slug that was generated in Page.save()
        # matches what we think it should be.
        self.assertEqual(page.slug, "my-test-page")
