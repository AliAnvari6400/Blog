from rest_framework.test import APIClient
from django.urls import reverse
import pytest

from accounts.models import User, Profile
from ..models import Task
from blog.models import Post 


@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="test@admin.com", password="anvari@7768", is_verified=True
    )
    return user


@pytest.fixture
def url(db, common_user):
    profile, created = Profile.objects.get_or_create(user=common_user)

    post = Post.objects.create(
        title="post title",
        content="post body",
        author=profile,
    )

    task = Task.objects.create(
        post=post,
        author=profile,
        title="test",
        status=True,
    )

    return reverse(
        "comment:api-v1:task-detail",
        kwargs={"pid": post.id, "pk": task.id}
    )

@pytest.fixture
def url_post(db, common_user):
    profile, _ = Profile.objects.get_or_create(user=common_user)
    post = Post.objects.create(title="post title", content="post body", author=profile)
    return reverse("comment:api-v1:task-list", kwargs={"pid": post.id}), post , profile


@pytest.mark.django_db
class TestTaskApi:

    def test_get_task_response_401(self, api_client, url):  # GET unauthorized
        response = api_client.get(url)
        assert response.status_code == 401

    def test_get_task_response_200(
        self, api_client, common_user, url
    ):  # GET with login user
        api_client.force_login(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_post_task_response_401(self, api_client, url):  # POST unauthorized
        data = {
            "title": "test",
            "status": True,
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    # def test_post_task_response_201(
    #     self, api_client, common_user, url_post
    # ):  # POST with login user
    #     api_client.force_login(user=common_user)
    #     data = {
    #         "title": "test",
    #         "status": True,
    #     }
    #     response = api_client.post(url_post, data)
    #     assert response.status_code == 201
        
    def test_post_task_response_201(self, api_client, common_user, url_post): # POST with login user
        api_client.force_login(user=common_user)
        url, post, profile = url_post
        data = {
            "author":profile.id,
            "post": post.id,
            "title": "test",
            "status": True,
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_post_task_response_400(
        self, api_client, common_user, url_post
    ):  # POST with incomplete data        
        api_client.force_login(user=common_user)
        url, post, profile = url_post
        data = {
            "author":profile.id,
            "post": post.id,
            "title": "",
            "status": "test",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400
