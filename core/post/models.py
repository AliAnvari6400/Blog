from django.db import models
from django.urls import reverse


# Create Task model:
class Task(models.Model):
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE, related_name='post_tasks')
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE, related_name='post_tasks')
    title = models.CharField(max_length=250, default="test")
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_snippet(self):
        return self.title[0:2]

    def get_absolute_api_url(self):
        return reverse("post:api-v1:task-detail", kwargs={"pk": self.pk})
