from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import pre_save


class Candidate(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    known_for = models.CharField(null=True, blank=True, max_length=255)
    image = models.ImageField(upload_to="candidate_pic", null=True, blank=True)
    hometown = models.CharField(null=True, blank=True, max_length=255)
    background = models.TextField(null=True, blank=True)

    political_party = models.ForeignKey('PoliticalParty', null=True, blank=True)
    race = models.ForeignKey('Race', null=True, blank=True)
    

    up_users = models.ManyToManyField('CustomUser', blank=True, related_name='up_voted_candidates')
    down_users = models.ManyToManyField('CustomUser', blank=True, related_name='down_voted_candidates')
    up_vote_count = models.IntegerField(null=True, blank=True)
    down_vote_count = models.IntegerField(null=True, blank=True)
    
    # INSERT STANCE OBJECTS HERE LATER

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"

    def __unicode__(self):
        return self.name

    def raw_vote_count(self):
        return self.up_vote_count - self.down_vote_count


def update_vote_count(sender, instance, **kwargs):
    if instance.political_party is not None:
        instance.up_vote_count = len(instance.up_users.all())
        instance.down_vote_count = len(instance.down_users.all())


pre_save.connect(update_vote_count, sender=Candidate)


class Comment(models.Model):
    body = models.TextField("comment body", null=True, blank=True)
    author = models.ForeignKey('CustomUser', null=True, blank=True)
    candidate = models.ForeignKey('Candidate', null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __unicode__(self):
            return self.author.email + ": " + self.body[:15]


class PoliticalParty(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    initials = models.CharField(null=True, blank=True, max_length=255)
    animal_image = models.ImageField(upload_to="party_animal_image", null=True, blank=True)
    description = models.TextField(null=True, blank=True)


    class Meta:
        verbose_name = "Political party"
        verbose_name_plural = "Political parties"

    def __unicode__(self):
            return self.name
   

class Race(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    state_abbrev = models.CharField(null=True, blank=True, max_length=10)
    race_type = models.CharField(max_length=1)
    district = models.CharField(null=True, blank=True, max_length=255)
    class Meta:
        verbose_name = "Race"
        verbose_name_plural = "Races"
        ordering = ['name']

    def __unicode__(self):
            return self.name



class CustomUserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()

        if not email:
            email = username
        email = self.normalize_email(email)
        user = self.model(email=email,
                              is_staff=is_staff,
                              is_active=True,
                              is_superuser=is_superuser,
                              last_login=now,
                              date_joined=now,
                              **extra_fields
                              )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user("", email, password, False, False, **extra_fields)     


    def create_superuser(self, email, password, **extra_fields):
        return self._create_user("", email, password, True, True, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', max_length=255, unique=True)
    first_name = models.CharField('first name', max_length=255, blank=True, null=True)
    last_name = models.CharField('last name', max_length=255, blank=True, null=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name ='user'
        verbose_name_plural = 'users'

    def __unicode__(self):
        return self.email.partition('@')[0]

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
