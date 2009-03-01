from exceptions import TypeError, ValueError
from django.contrib.auth.models import User
from models import PermissionModel # importing custom permission models
from djime.models import Slip as Model #importing a custom model to show princip.
import new
import inspect

# MetaClass and MetaObject is taken form the django-granular-permissions app.
class MetaClass(type):
    def __new__(self, classname, classbases, classdict):
        try:
            frame = inspect.currentframe()
            frame = frame.f_back
            if frame.f_locals.has_key(classname):
                old_class = frame.f_locals.get(classname)
                for name,func in classdict.items():
                    if inspect.isfunction(func):
                        setattr(old_class, name, func)
                return old_class
            return type.__new__(self, classname, classbases, classdict)
        finally:
            del frame

class MetaObject(object):
    __metaclass__ = MetaClass

class Model(MetaObject):
    def has_permission(self, user_input):
        # we are both accepting a user object or a user id.
        if type(user_input) == int:
            # a user id has been entered. We're on purpose letting django
            # handle raising an error if the user does not exist.
            user = User.objects.get(pk=user_input)
        elif type(user_input) == User:
            # a userobject has been entered
            user = user_input
        else:
            # an invalid input, raise an error.
            raise TypeError("The input for %s must be either an integer or userobject." % self.has_permission)
        # if user is superuser, we will return information about that, acapella
        # wont hindel superusers access.
        if user.is_superuser:
            return "User %s is superuser and has all access" % user
        perm = PermissionModel.objects.filter(model=self, user=user)
        # check to see if there is any info for the given user and object
        if not perm:
            return "No permissions has been entered for user %(user)s and object %(object)s" % {'user': user, 'object': self}
        else:
            return perm[0].PERMISSION_CHOICES[perm[0].permission][1]

    def check_permission(self, user_input, permissions=[0, 1, 2, 3, 4, 5, 6, 7]):
        if type(user_input) == int:
            user = User.objects.get(pk=user_input)
        elif type(user_input) == User:
            user = user_input
        else:
            raise TypeError("The user input for %s must be either an integer or userobject." % self.has_permission)
        if user.is_superuser:
            return True
        # Check to see if the permission is a list, only integers are accepted.
        if type(permissions) != list:
            raise TypeError("The permissions input for %s must be entered in a list." % self.check_permission)
        perm = PermissionModel.objects.filter(model=self, user=user)
        # if no permissions has been entered for the user on this object,
        # returning True as acapella wont hinder access unless explicit ordered.
        if not perm:
            return True
        # check to see if the permission is in the list of provided permissions.
        if perm[0].permission in permissions:
            return True
        return False

