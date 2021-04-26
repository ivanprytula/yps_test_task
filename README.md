# Project setup/run

## Execute following commands in project's local repo/working dir
```shell
pipenv install
pipenv shell
./manage.py migrate
./manage.py test  # couple of initial sanity post/get tests
./manage.py runserver
```

# You can use endpoints in multiple ways, for example:

 - directly in a browser (only GET requests)
 - with HTTP Requests collection for PyCharm IDE
 - with Postman (collection file in project repo)

### HTTP Requests for PyCharm
```http request

### Add course to catalog
POST http://localhost:8000/api/courses/create/
Content-Type: application/json

{
  "id": "1",
  "name": "Python course",
  "start_date": "2021-05-19",
  "end_date": "2021-07-01",
  "lectures_quantity": "25"
}

### List of courses from catalog
GET http://localhost:8000/api/courses/
Accept: application/json


### Search course by name
GET http://localhost:8000/api/courses/?name=python
Accept: application/json


### Search courses that start LATER than entered date
GET http://localhost:8000/api/courses/?start_date_gte=2021-04-01
Accept: application/json


### Search courses that start BEFORE than entered date
GET http://localhost:8000/api/courses/?end_date_lte=2021-09-15
Accept: application/json


### Retrieve details about course
GET http://localhost:8000/api/courses/1
Accept: application/json


### Update info about course
PUT http://localhost:8000/api/courses/update/
Content-Type: application/json

{
  "id": "2",
  "name": "Java course.New 21",
  "start_date": "2021-06-15",
  "end_date": "2021-08-02",
  "lectures_quantity": "30"
}

### Delete/remove course from catalog
DELETE http://localhost:8000/api/courses/delete/
Content-Type: application/json

{
  "id": "1"
}
```