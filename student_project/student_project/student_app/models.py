from django.db import models

# fields represents the attributes of the model.
class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField()


    def __str__(self):
        return self.name