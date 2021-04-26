import json
from datetime import datetime
from http import HTTPStatus
from typing import Union

from django.db import ProgrammingError
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import make_aware
from django.views.generic import View

from courses.models import Course
from .mixins import CSRFExemptMixin, JsonResponseMixin
from .utils import is_json

DATE_FORMAT = '%Y-%m-%d'


def validate_input_data_format(new_data: dict) -> Union[dict, JsonResponse]:
    try:
        filter_kwargs = {
            'id': int(new_data.get('id')),
            'name': new_data.get('name'),
            'start_date': new_data.get('start_date'),
            'end_date': new_data.get('end_date'),
            'lectures_quantity': int(
                new_data.get('lectures_quantity'))
        }

        for k, v in filter_kwargs.items():
            if not v:
                resp_msg = {
                    'message': f'`{k}` value is missing in '
                               f'submitted data.'
                }
                return JsonResponse(resp_msg,
                                    status=HTTPStatus.BAD_REQUEST)
        return filter_kwargs
    except (ValueError, TypeError):
        resp_msg = {
            'message': 'Please, check the format of you data.'
        }
        return JsonResponse(resp_msg,
                            status=HTTPStatus.BAD_REQUEST)


def transform_naive_datetime(data: dict) -> Union[dict, JsonResponse]:
    try:
        data['start_date'] = make_aware(
            datetime.strptime(data['start_date'], DATE_FORMAT),
            is_dst=True)
        data['end_date'] = make_aware(
            datetime.strptime(data['end_date'], DATE_FORMAT),
            is_dst=True)
        return data
    except ValueError:
        resp_msg = {
            'message': 'Please, check the format of you `Start/End date`.'
        }
        return JsonResponse(resp_msg,
                            status=HTTPStatus.BAD_REQUEST)


def is_valid_date(date: str):
    try:
        datetime.strptime(date, DATE_FORMAT)
        is_correct_date = True
    except ValueError:
        is_correct_date = False
    return is_correct_date


class CoursesCreateAPIView(CSRFExemptMixin, JsonResponseMixin, View):
    def post(self, request, *args, **kwargs):
        resp_msg = {}
        status_code = ''
        if not is_json(request.body):
            resp_msg = {
                'message': 'Invalid data sent, please send using JSON.'
            }
            status_code = HTTPStatus.BAD_REQUEST
        else:
            req_data = json.loads(request.body)
            try:

                valid_data = validate_input_data_format(req_data)
                filter_kwargs = transform_naive_datetime(valid_data)

                try:
                    if Course.objects.get(**filter_kwargs):
                        resp_msg = {
                            'message': 'This course is already in catalog.'
                        }
                        return self.to_json_response(resp_msg,
                                                     status=HTTPStatus.OK)
                except Course.DoesNotExist:
                    Course.objects.create(**filter_kwargs)
                    resp_msg = {'message': 'Created.'}
                    status_code = HTTPStatus.CREATED
            except ProgrammingError:
                resp_msg = {'message': 'Database error.'}
                status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        return self.to_json_response(resp_msg, status=status_code)


class CoursesListAPIView(JsonResponseMixin, View):

    def get(self, request, *args, **kwargs):

        json_data = ''
        if request.GET:
            name_param = request.GET.get('name')
            start_date_param = request.GET.get('start_date_gte')
            end_date_param = request.GET.get('end_date_lte')

            if name_param:
                json_data = Course.objects.filter(
                    name__icontains=name_param).serialize()

            if start_date_param and is_valid_date(start_date_param):
                json_data = Course.objects.filter(
                    start_date__gte=start_date_param).serialize()

            if end_date_param and is_valid_date(end_date_param):
                json_data = Course.objects.filter(
                    start_date__lte=end_date_param).serialize()

            if (start_date_param and not is_valid_date(start_date_param)) or (
                    end_date_param and not is_valid_date(end_date_param)):
                resp_msg = {
                    'message': 'Incorrect data format, should be YYYY-MM-DD.'
                }
                status_code = HTTPStatus.BAD_REQUEST
                return self.to_json_response(resp_msg, status=status_code)
        else:
            json_data = Course.objects.all().serialize()
        return HttpResponse(json_data, content_type='application/json')


class CoursesDetailsAPIView(JsonResponseMixin, View):
    def get(self, request, course_id, *args, **kwargs):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            resp_msg = {
                'message': 'Course does not exist.'
            }
            return self.to_json_response(resp_msg, status=HTTPStatus.NOT_FOUND)

        json_data = course.serialize()
        return HttpResponse(json_data, content_type='application/json')


class CoursesUpdateAPIView(CSRFExemptMixin, JsonResponseMixin, View):

    def put(self, request, *args, **kwargs):
        if not is_json(request.body):
            resp_msg = {
                'message': 'Invalid data sent, please send using JSON.'
            }
            status_code = HTTPStatus.BAD_REQUEST
        else:
            req_data = json.loads(request.body)

            valid_data = validate_input_data_format(req_data)
            data_for_update = transform_naive_datetime(valid_data)

            updated_course = Course.objects.filter(
                id=data_for_update['id']).update(
                name=data_for_update.get('name'),
                start_date=data_for_update.get('start_date'),
                end_date=data_for_update.get('end_date'),
                lectures_quantity=data_for_update.get('lectures_quantity')
            )

            resp_msg = {
                'message': 'Course was updated.'
            }
            status_code = HTTPStatus.OK

            if not updated_course:
                status_code = HTTPStatus.NOT_FOUND
                resp_msg = {
                    'message': 'Course does not exist.'
                }

        return self.to_json_response(resp_msg, status=status_code)


class CoursesDeleteAPIView(CSRFExemptMixin, JsonResponseMixin, View):
    def delete(self, request, *args, **kwargs):
        if not is_json(request.body):
            resp_msg = {
                'message': 'Invalid data sent, please send using JSON.'
            }
            status_code = HTTPStatus.BAD_REQUEST
        else:

            try:
                req_data = json.loads(request.body)

                course_to_delete = Course.objects.get(id=req_data.get('id'))
                course_to_delete.delete()
                status_code = HTTPStatus.OK
                resp_msg = {
                    'message': 'Course was deleted.'
                }
            except Course.DoesNotExist:
                status_code = HTTPStatus.NOT_FOUND
                resp_msg = {
                    'message': 'Course does not exist.'
                }

        return self.to_json_response(resp_msg, status=status_code)
