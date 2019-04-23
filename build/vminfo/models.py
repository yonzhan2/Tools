from django.db import models


# Create your models here.
class VCInfo(models.Model):
    vcdns = models.CharField(max_length=32, primary_key=True)
    vcname = models.CharField(max_length=32)

    def __str__(self):
        return self.vcname


class VMList(models.Model):
    vcname = models.CharField(max_length=32)
    dcname = models.CharField(max_length=32)
    cluster = models.CharField(max_length=32)
    hostip = models.CharField(max_length=32)
    vmname = models.CharField(max_length=100)
    vmip = models.CharField(max_length=16, default='N/A')
    vmmacc = models.CharField(max_length=100)
    status = models.CharField(max_length=16)
    vmpath = models.CharField(max_length=200)

    class Meta:
        unique_together = ('vmname', 'vmmacc')

    def __str__(self):
        return self.vmname
