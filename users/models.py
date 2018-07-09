from django.db import models
from dateutil.relativedelta import relativedelta
import datetime

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils.translation import ugettext_lazy as _



class UserManager(BaseUserManager):
    
    use_in_migrations = True

    def create_user(self, email, name, college, date_of_birth, is_participant, is_mentor, is_sponsor, is_end_user , mentored_challenges, mentored_won_challenges, sponsored_challenges, contested_challenges, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        print("naam" + name)
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            college=college,
            name=name,
            is_participant = is_participant,
            is_mentor = is_mentor,
            is_sponsor = is_sponsor,
            is_end_user = is_end_user,
            mentored_challenges = mentored_challenges,
            mentored_won_challenges = mentored_won_challenges,
            sponsored_challenges = sponsored_challenges,
            contested_challenges = contested_challenges,
        )

        print(user)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, college, date_of_birth, password , is_participant, is_mentor, is_sponsor, is_end_user , mentored_challenges, mentored_won_challenges, sponsored_challenges, contested_challenges):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            college=college,
            name=name,
            is_participant = is_participant,
            is_mentor = is_mentor,
            is_sponsor = is_sponsor,
            is_end_user = is_end_user,
            mentored_challenges = mentored_challenges,
            mentored_won_challenges = mentored_won_challenges,
            sponsored_challenges = sponsored_challenges,
            contested_challenges = contested_challenges,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, college, date_of_birth, password, is_participant, is_mentor, is_sponsor, is_end_user):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            college= "True",
            name= "True",
            is_participant =  True,
            is_mentor =  True,
            is_sponsor =  True,
            is_end_user =  True,
            mentored_challenges =  0,
            mentored_won_challenges = 1,
            sponsored_challenges =  1,
            contested_challenges =  1,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    username = None
    email = models.EmailField(_('email address'), unique=True)


    name = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    date_of_birth = models.DateField(default=datetime.date.today)

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    is_participant = models.BooleanField(default=True)
    is_mentor = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=False)
    is_end_user = models.BooleanField(default=False)
    
    contested_challenges = models.IntegerField(default=0) 
    mentored_challenges = models.IntegerField(default=1)
    mentored_won_challenges = models.IntegerField(default=0)
    sponsored_challenges = models.IntegerField(default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'date_of_birth','name','college', 'is_participant', 'is_mentor','is_sponsor','is_end_user']

    objects = UserManager()

    def sponsor_challenge(self):        
        new_sponsor_count = self.sponsored_challenges + 1
        self.sponsored_challenges = new_sponsor_count
        self.save(update_fields = ["sponsored_challenges"] )

    def mentor_challenge(self):
        new_mentor_count = self.mentored_challenges + 1
        self.mentored_challenges = new_mentor_count
        print(new_mentor_count)
        print(self.mentored_challenges)
        self.save(update_fields = ["mentored_challenges"] )
    
    def contest_challenge(self):
        new_contest_count = self.contested_challenges + 1
        setattr(self, 'contested_challenges', new_contest_count)

        self.save(update_fields = ["contested_challenges"] )
    
    def mentor_won_challenge(self):
        new_mentor_won_count = self.mentored_won_challenges + 1
        setattr(self, 'mentored_won_challenges', new_mentor_won_count)

        self.save(update_fields = ["mentored_won_challenges"] )

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

# class MyUser(AbstractBaseUser):
#     emailaddress = models.CharField(max_length=40, unique=True)
#     password = models.CharField(max_length=30)
#     name = models.CharField(max_length=100)
#     college = models.CharField(max_length=100)
#     date_of_birth = models.DateField()
#     is_active = models.BooleanField(default=False) # default=False when you are going to implement Activation Mail


#     USERNAME_FIELD = 'emailaddress'
    # REQUIRED_FIELDS = ['password','name','college','date_of_birth']
# # Create your models here.
# class UserAccountManager(BaseUserManager):

#     def create_user(self, email, name, college, dob, age, username, password=None):
#         if not email:
#             raise ValueError('Email must be set!')
#         user = self.model(email=email, name=name, college=college, dob=dob, age=age, username=username)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, first_name, last_name, password):
#         user = self.create_user(email, first_name, last_name, password)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

# class User(AbstractBaseUser):

#     REQUIRED_FIELDS = ('name','college','dob','password')

#     pub_date = models.DateTimeField(auto_now_add=True, blank=True)
#     USERNAME_FIELD = 'email'

#     password = models.CharField(max_length=30)
#     email = models.EmailField(max_length=70, unique=True)
#     name = models.CharField(max_length=100)
#     college = models.CharField(max_length=100)
#     username = models.CharField(max_length=100)
#     dob = models.DateField(max_length=8, default="1998-01-01")
#     age = models.IntegerField(default=0,editable=False) 

#     is_active = models.BooleanField(default=False) # default=False when you are going to implement Activation Mail
#     is_admin = models.BooleanField(default=False)

#     objects = UserAccountManager()

#     def __str__(self):
#         today = datetime.date.today()
#         delta = relativedelta(today, self.dob)
#         self.age = delta.years
#         return self.email

#     class Meta:
#         ordering = ('pub_date',)

# class User(AbstractBaseUser, PermissionsMixin):

#   is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
#   is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
#   date_joined = models.DateTimeField(_('date joined'), default=datetime.date.now())

#   USER_TYPES = (
#     ('Farmer', 'Farmer'),
#     ('Windmill owner', 'Windmill owner'),
#     ('Solar panel owner', 'Solar panel owner'),)
#   user_type = models.CharField(_('user type'), choices=USER_TYPES, max_length=30, blank=True, null=True)

#   USERNAME_FIELD = 'username'
#   REQUIRED_FIELDS = ['email',]

#   objects = UserManager()

#   class Meta:
#     verbose_name = _('user')
#     verbose_name_plural = _('users')

#   def get_full_name(self):
#     full_name = '%s %s' % (self.first_name, self.last_name)
#     return full_name.strip()

#   def get_short_name(self):
#     return self.first_name

#   def email_user(self, subject, message, from_email=None):
#     send_mail(subject, message, from_email, [self.email]) 
