from django.db import models


class Poem(models.Model):
    id = models.IntegerField
    title = models.CharField(max_length=200)
    poet = models.CharField(max_length=200)

    def __str__(self):
        return self.title + " by " + self.poet
