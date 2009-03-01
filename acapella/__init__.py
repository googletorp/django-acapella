from exceptions import TypeError, ValueError
from django.contrib.auth.models import User
from models import PermissionModel # importing custom permission models
from djime.models import Slip as Model #importing a custom model to show princip.
import new
import inspect

# MetaClass and MetaObject is taken form the django-granular-permissions app.
# This enables us to inject new permission methods to any given model.
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

    def check_permission(self, user_input, permission):
        if type(user_input) == int:
            user = User.objects.get(pk=user_input)
        elif type(user_input) == User:
            user = user_input
        else:
            raise TypeError("The user input for %s must be either an integer or userobject." % self.has_permission)
        if user.is_superuser:
            return True
        # Check to see if the permission is a list, only integers are accepted.
        if type(permission) not in [str, unicode]:
            raise TypeError("The permissions input for %s must be entered in a string." % self.check_permission)
        if permission not in ['read', 'Read',
                                'write', 'Write',
                                'delete', 'Delete',
                                u'read', u'Read',
                                u'write', u'Write',
                                u'delete', u'Delete']:
            return ValueError("The permission inout for %s must be read, write or delete" % self.check_permission)
        if permission in ['read', 'Read', u'read', u'Read']:
            perm_list = [1,3,5,7]
        elif permission in ['write', 'Write', u'write', u'Write']:
            perm_list = [2,3,6,7]
        else:
            perm_list = [4,5,6,7]
        perm = PermissionModel.objects.filter(model=self, user=user)
        # if no permissions has been entered for the user on this object,
        # returning True as acapella wont hinder access unless explicit ordered.
        if not perm:
            return True
        # check to see if the permission is in the list of provided permissions.
        if perm[0].permission in perm_list:
            return True
        return False

    def add_permission(self, user_input, permission):
        if type(user_input) == int:
            user = User.objects.get(pk=user_input)
        elif type(user_input) == User:
            user = user_input
        else:
            raise TypeError("The user input for %s must be either an integer or userobject." % self.has_permission)
        if type(permission) not in [str, unicode]:
            raise TypeError("The permissions input for %s must be entered in a string." % self.check_permission)
        if permission not in ['read', 'Read',
                                'write', 'Write',
                                'delete', 'Delete',
                                u'read', u'Read',
                                u'write', u'Write',
                                u'delete', u'Delete']:
            return ValueError("The permission inout for %s must be read, write or delete" % self.check_permission)
        if permission in ['read', 'Read', u'read', u'Read']:
            perm_list = [1,3,5,7]
            perm_int = 1
        elif permission in ['write', 'Write', u'write', u'Write']:
            perm_list = [2,3,6,7]
            perm_int = 2
        else:
            perm_list = [4,5,6,7]
            perm_int = 4
        perm = PermissionModel.objects.filter(model=self, user=user)
        if not perm:
            new_perm = PermissionModel(model=self, user=user, permission=perm_int)
            new_perm.save()
            return 'New permission %(permission)s for user %(user)s on object %(model)s has been created' % {'permission': permission,
                                                                                                            'user': user,
                                                                                                            'model': self}
        else:
            perm = perm[0]
            if not perm.permission in perm_list:
                # To add a permission we just need to add the permission integer
                # to the integer permission value.
                perm.permission += perm_int
                perm.save()
                return 'Permission %(permission)s for user %(user)s on object %(model)s has been added' % {'permission': permission,
                                                                                                                'user': user,
                                                                                                                'model': self}
        return 'Permission %(permission)s for user %(user)s on object %(model)s already existed' % {'permission': permission,
                                                                                                    'user': user,
                                                                                                    'model': self}
    def del_permission(self, user_input, permission):
        if type(user_input) == int:
            user = User.objects.get(pk=user_input)
        elif type(user_input) == User:
            user = user_input
        else:
            raise TypeError("The user input for %s must be either an integer or userobject." % self.has_permission)
        if type(permission) not in [str, unicode]:
            raise TypeError("The permissions input for %s must be entered in a string." % self.check_permission)
        if permission not in ['read', 'Read',
                                'write', 'Write',
                                'delete', 'Delete',
                                u'read', u'Read',
                                u'write', u'Write',
                                u'delete', u'Delete']:
            return ValueError("The permission inout for %s must be read, write or delete" % self.check_permission)
        if permission in ['read', 'Read', u'read', u'Read']:
            perm_list = [1,3,5,7]
            perm_int = 1
        elif permission in ['write', 'Write', u'write', u'Write']:
            perm_list = [2,3,6,7]
            perm_int = 2
        else:
            perm_list = [4,5,6,7]
            perm_int = 4
        perm = PermissionModel.objects.filter(model=self, user=user)
        if not perm:
            # if no permission has been created for the user on the object, we
            # create a new permission with no access perm_int = 0
            new_perm = PermissionModel(model=self, user=user, permission=0)
            new_perm.save()
            return 'New permission for user %(user)s on object %(model)s with no access has been created' % {'user': user,
                                                                                                            'model': self}
        else:
            perm = perm[0]
            if perm.permission in perm_list:
                # To delete a perm, we can just substract the permission
                # integer.
                perm.permission -= perm_int
                perm.save()
                return 'Permission %(permission)s for user %(user)s on object %(model)s has been deleted' % {'permission': permission,
                                                                                                            'user': user,
                                                                                                            'model': self}
        return 'User %(user)s on object %(model)s did not have the permission %(permission)s' % {'permission': permission,
                                                                                                    'user': user,
                                                                                                    'model': self}
