from django.urls import path

from .api.views import (CoursesListAPIView,
                        CoursesDetailsAPIView,
                        CoursesCreateAPIView,
                        CoursesUpdateAPIView,
                        CoursesDeleteAPIView,
                        )

urlpatterns = [
    path('create/', CoursesCreateAPIView.as_view()),
    path('', CoursesListAPIView.as_view()),
    path('<int:course_id>', CoursesDetailsAPIView.as_view()),
    path('update/', CoursesUpdateAPIView.as_view()),
    path('delete/', CoursesDeleteAPIView.as_view()),
]

