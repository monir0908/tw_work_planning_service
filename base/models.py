from django.db import models
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
from .enums import StatusTypes

class BaseModel(models.Model):
    
    status = models.IntegerField(
        choices=[(tag.value, _(tag.name)) for tag in StatusTypes],
        default=StatusTypes.ACTIVE.value,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'base'
        
class NameBaseModel(BaseModel):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    slug = AutoSlugField(
        populate_from='first_name',
        always_update=True,
        unique=True,
        allow_unicode=True
    )

    class Meta:
        abstract = True
