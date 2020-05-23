from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class TicketUser(AbstractUser):
    name = models.CharField(max_length=50)


class TicketItem(models.Model):
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'
    INVALID = 'INVALID'
    CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
        (INVALID, 'Invalid')
    ]
    title = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    time = models.CharField(max_length=30, default='')
    description = models.TextField()
    filed_user = models.ForeignKey(TicketUser, related_name='filed_user', null=True, blank=True, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(TicketUser, related_name='assigned_user', null=True, blank=True, on_delete=models.CASCADE)
    completed_user = models.ForeignKey(TicketUser, related_name='completed_user', null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(choices=CHOICES, default=NEW, max_length=30)

    def __str__(self):
        return self.title
