from django.db import models
from django.contrib.auth.models import User
from djime.models import Slip as Model #importing a custom model for testing

class Permission(models.Model):
    """
    This model is the base form, for models that will create a ACL.

    The structure for the permission model is still a bit uncertain, as it is
    still in progress. The idea is to create subclasses of this model, one for
    each model that need a ACL
    """

    PERMISSION_CHOICES = (
        (0, 'No access'),
        (1, 'Read'),
        (2, 'Write'),
        (3, 'Read and write'),
        (4, 'Delete'),
        (5, 'View and delete'),
        (6, 'Write and delete'),
        (7, 'Read, write and delete'),
    )
    permission = models.IntegerField(default=0, choices=PERMISSION_CHOICES)
    user = models.ForeignKey(User)


class PermissionModel(Permission):
    """
    This is an example and test model. It is designed to show the use of the to
    show the use and installation of django-acapella aswell as serve as a
    debugging tool.
    """

    model = models.ForeignKey(Model)

    def __unicode__(self):
        return self.model.__unicode__() + ': ' + self.PERMISSION_CHOICES[self.permission][1]

