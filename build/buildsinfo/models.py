from django.db import models
from mongoengine import *
# Create your models here.

from build.settings import DBNAME

connect(DBNAME)


class Employee(Document):
    name = StringField(max_length=50)
    age = IntField(required=False)

    meta = {'collection': 'Employee'}


class BuildInfo(Document):
    ipaddr = StringField(max_length=20)
    env = StringField(max_length=20)
    type = StringField()
    build = ListField()
    lastbuild = ListField()
    hostname = StringField()
    status = StringField()
    createtime = DateTimeField()
    lastmodifiedtime = DateTimeField()

    meta = {'collection': "buildinfo"}

    # def __unicode__(self):
    #     return self.build


class Envs(Document):
    name = StringField(max_length=20)

    meta = {'collection': "envs"}
