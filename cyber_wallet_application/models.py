from django.contrib.auth.models import User
from django.db import models


class Operation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    execution_moment = models.DateTimeField()
    accounting_moment = models.DateTimeField()
    description = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def is_income(self):
        return self.amount > 0


class Category(models.Model):
    name = models.CharField(max_length=30)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_moment = models.DateTimeField()
    to_moment = models.DateTimeField()


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_moment = models.DateTimeField()
    to_moment = models.DateTimeField()
    text = models.CharField(max_length=5000)


class LocalConfiguration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=30)
    value = models.CharField(max_length=5000)


class GlobalConfiguration(models.Model):
    key = models.CharField(max_length=30)
    value = models.CharField(max_length=5000)
