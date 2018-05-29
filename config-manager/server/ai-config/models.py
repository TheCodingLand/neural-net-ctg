from django.db import models


class Config(models.Model):
    source = models.CharField(max_length=200, unique=True)
    version = models.CharField(max_length=200, unique=True)
    Process = models.ForeignKey(Process, on_delete='cascade')

class Source(models.Model):
    name = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=200, unique=True)
    inputtype = models.ForeignKey(InputType, on_delete='cascade')
    def __str__(self):
        return "%s" % self.name

class Destination(models.Model):
    name = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=200, unique=True)
    outputtype = models.ForeignKey(OutputType, on_delete='cascade')
    def __str__(self):
        return "%s" % self.name
    
class Process(models.Model):
    name = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=200, unique=True)
    source = models.ForeignKey(Source, on_delete='cascade')
    destination = models.ForeignKey(Destination, on_delete='cascade')


class InputType(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return "%s" % self.name


class OutputType(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return "%s" % self.name



