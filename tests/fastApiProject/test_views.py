import json
from http import HTTPStatus

import pytest
import requests


@pytest.fixture
def get_response_posts_page1():
    return [
        {"id": 1, "name": "name1", "subject": "subject1", "content": "content1", "rating" :2},
        {"id": 2, "name": "name2", "subject": "subject2", "content": "content2", "rating": 3},
        {"id": 3, "name": "name3", "subject": "subject3", "content": "content3", "rating": 7},
        {"id": 4, "name": "name4", "subject": "subject4", "content": "content4", "rating": 9},
        {"id": 5, "name": "name5", "subject": "subject5", "content": "content5", "rating": 1},
        {"id": 6, "name": "name6", "subject": "subject6", "content": "content6", "rating": 8},
        {"id": 7, "name": "name7", "subject": "subject7", "content": "content7", "rating": 6},
        {"id": 8, "name": "name8", "subject": "subject8", "content": "content8", "rating": 4},
        {"id": 9, "name": "name9", "subject": "subject9", "content": "content9", "rating": 3},
        {"id": 10, "name": "name10", "subject": "subject10", "content": "content10", "rating": 9}
    ]


@pytest.fixture
def get_response_posts_page2():
    return [
        {"id": 11, "name": "name11", "subject": "subject11", "content": "content11", "rating": 5},
        {"id": 12, "name": "name12", "subject": "subject3", "content": "content12", "rating": 4},
        {"id": 13, "name": "name13", "subject": "python text", "content": "content13", "rating": 7},
        {"id": 14, "name": "python data", "subject": "subject14", "content": "content14", "rating": 8}
    ]


@pytest.fixture
def get_response_posts_rating_between8_9():
    return [
        {"id": 4, "name": "name4", "subject": "subject4", "content": "content4", "rating": 9},
        {"id": 6, "name": "name6", "subject": "subject6", "content": "content6", "rating": 8},
        {"id": 10, "name": "name10", "subject": "subject10", "content": "content10", "rating": 9},
        {"id": 14, "name": "python data", "subject": "subject14", "content": "content14", "rating": 8}
    ]


@pytest.fixture
def get_response_fail_page():
    return {"detail": [{"loc": ["query", "page"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"}]}


def test_posts_success(requests_mock, get_response_posts_page1, get_response_posts_page2,
                       get_response_posts_rating_between8_9):
    requests_mock.get('http://127.0.0.1:8000/api/v1/posts',
                      json=get_response_posts_page1)
    response = requests.get('http://127.0.0.1:8000/api/v1/posts')

    assert json.dumps(get_response_posts_page1) == response.text
    assert HTTPStatus.OK == response.status_code

    requests_mock.get('http://127.0.0.1:8000/api/v1/posts?page=2',
                      json=get_response_posts_page2)
    response = requests.get('http://127.0.0.1:8000/api/v1/posts?page=2')

    assert json.dumps(get_response_posts_page2) == response.text
    assert HTTPStatus.OK == response.status_code

    requests_mock.get('http://127.0.0.1:8000/api/v1/posts?theme=python',
                      json=[{"id":13,"name":"name13","subject":"python text",
                             "content":"content13","rating":7}])
    response = requests.get('http://127.0.0.1:8000/api/v1/posts?theme=python')

    assert json.dumps([{"id":13,"name":"name13","subject":"python text","content":"content13","rating":7}]) == \
           response.text
    assert HTTPStatus.OK == response.status_code

    requests_mock.get('http://127.0.0.1:8000/api/v1/posts?rating=8__9',
                      json=get_response_posts_rating_between8_9)
    response = requests.get('http://127.0.0.1:8000/api/v1/posts?rating=8__9')

    assert json.dumps(get_response_posts_rating_between8_9) == response.text
    assert HTTPStatus.OK == response.status_code

    requests_mock.get('http://127.0.0.1:8000/api/v1/posts?rating=9',
                      json=[{"id":4,"name":"name4","subject":"subject4","content":"content4","rating":9},
                            {"id":10,"name":"name10","subject":"subject10","content":"content10","rating":9}])
    response = requests.get('http://127.0.0.1:8000/api/v1/posts?rating=9')

    assert json.dumps([{"id":4,"name":"name4","subject":"subject4","content":"content4","rating":9},
                       {"id":10,"name":"name10","subject":"subject10","content":"content10","rating":9}]) == \
           response.text
    assert HTTPStatus.OK == response.status_code

    requests_mock.get('http://127.0.0.1:8000/api/v1/posts?q=python',
                      json=[{"id":13,"name":"name13","subject":"python text","content":"content13","rating":7},
                            {"id":14,"name":"python data","subject":"subject14","content":"content14","rating":8}])

    response = requests.get('http://127.0.0.1:8000/api/v1/posts?q=python')
    assert json.dumps([{"id":13,"name":"name13","subject":"python text","content":"content13","rating":7},
                       {"id":14,"name":"python data","subject":"subject14","content":"content14","rating":8}]) == \
           response.text
    assert HTTPStatus.OK == response.status_code

    requests_mock.get('http://127.0.0.1:8000/api/v1/posts?q=python&theme=subject&rating=5__10',
                      json=[{"id":14,"name":"python data","subject":"subject14","content":"content14","rating":8}])
    response = requests.get('http://127.0.0.1:8000/api/v1/posts?q=python&theme=subject&rating=5__10')

    assert json.dumps([{"id":14,"name":"python data","subject":"subject14","content":"content14","rating":8}]) == \
           response.text
    assert HTTPStatus.OK == response.status_code


def test_posts_fail(requests_mock, get_response_fail_page):
    requests_mock.get('http://127.0.0.1:8000/api/v1/posts?page=g',
                      json=get_response_fail_page, status_code=404)
    response = requests.get('http://127.0.0.1:8000/api/v1/posts?page=g')

    assert json.dumps(get_response_fail_page) == response.text
    assert HTTPStatus.NOT_FOUND == response.status_code

    requests_mock.get('http://127.0.0.1:8000/api/v1/posts?rating=g',
                      json=[])
    response = requests.get('http://127.0.0.1:8000/api/v1/posts?rating=g')

    assert json.dumps([]) == response.text
    assert HTTPStatus.OK == response.status_code
