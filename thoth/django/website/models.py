from django.db import models

# Create your models here.

class Question(models.Model):
    quesiton = models.CharField(max_length=500)
    value = models.PositiveIntegerField(default=0)
    answer = models.CharField(max_length=500, default=None)
    #lecture = models.ForeignKey(Lecture)

    def __str__(self):
        return self.quesiton


