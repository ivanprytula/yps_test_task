import datetime
from http import HTTPStatus

from django.test import TestCase, Client

from .models import Course


class ModelTestCase(TestCase):
    """This class defines the test suite for the Course model."""

    def setUp(self):
        self.course_name = "Yalantis Python course"
        self.start_date = datetime.datetime.now()
        self.end_date = self.start_date + datetime.timedelta(days=30)
        self.lectures_quantity = 1
        self.course = Course(name=self.course_name,
                             start_date=self.start_date,
                             end_date=self.end_date,
                             lectures_quantity=self.lectures_quantity)

    def test_model_can_create_a_course(self):
        """Test the Course model can create a course/instance."""
        old_count = Course.objects.count()
        self.course.save()
        new_count = Course.objects.count()
        self.assertNotEqual(old_count, new_count)


class APIViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = Client()
        self.course_data = {
            'id': '1',
            'name': 'Python course',
            'start_date': '2021-05-01',
            'end_date': '2021-07-01',
            'lectures_quantity': '20',
        }
        self.response = self.client.post(
            '/api/courses/create/',
            self.course_data,
            content_type='application/json',
            format='json')

    def test_api_can_create_a_course(self):
        """Test the API has course creation capability."""
        self.assertEqual(self.response.status_code, HTTPStatus.CREATED)

    def test_api_can_retrieve_courses_list(self):
        """Test the API has courses list retrieving capability."""
        response = self.client.get('/api/courses/', format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
