import json
from django.db import models


class CourseQuerySet(models.QuerySet):
    def serialize(self):
        list_values = \
            list(self.values('id', 'name', 'start_date', 'end_date',
                             'lectures_quantity'))
        return json.dumps(list_values, default=str)


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)


class Course(models.Model):
    name = models.CharField(max_length=255, blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    lectures_quantity = models.IntegerField()

    objects = CourseManager()

    def serialize(self):
        data = {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'lectures_quantity': self.lectures_quantity
        }
        return json.dumps(data, default=str)

    def __str__(self):
        return self.name
