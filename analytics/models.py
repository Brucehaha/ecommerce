from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.conf import settings
from .utils import get_client_ip
from .signals import  object_viewed_signal
from accounts.signals import user_logged_in


User = settings.AUTH_USER_MODEL



FORCE_SESSION_TO_ONE = getattr(settings,'FORCE_SESSION_TO_ONE', False)
FORCE_USER_INACTIVE_END_SESSION = getattr(settings,'FORCE_SESSION_TO_ONE', False)

class ObjectViewed(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    content_type    = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id       = models.PositiveIntegerField()
    ip_address      = models.CharField(max_length=120, blank=True, null=True)
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self, ):
        return "%s viewed: %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):

    c_type = ContentType.objects.get_for_model(sender)
    ip_address = None
    user = request.user
    if request.user.id == None:
        user = None
    try:
        ip_address = get_client_ip(request)
    except:
        pass
    new_view_instance = ObjectViewed.objects.create(
                user=user,
                content_type=c_type,
                object_id=instance.id,
                ip_address=ip_address
                )

object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ip_address      = models.CharField(max_length=120, blank=True, null=True)
    session_key     = models.CharField(max_length=100, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)
    ended          = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active=False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended


## auto logout after a new login from other browser
def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    ## manage logout from admin
    if not instance.active:
        instance.end_session()
if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)

##auto logout users afterh the user is not active
def post_save_session_user_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user=instance)
            for i in qs:
                i.end_session()

if FORCE_USER_INACTIVE_END_SESSION:
    post_save.connect(post_save_session_user_receiver, sender=User)





def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )
user_logged_in.connect(user_logged_in_receiver)
