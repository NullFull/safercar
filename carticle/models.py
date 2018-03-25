from django.db import models as m


class Article(m.Model):
    title = m.CharField(max_length=200)
    content = m.TextField()
    time_published = m.DateTimeField(auto_now_add=True)
    time_modified = m.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title