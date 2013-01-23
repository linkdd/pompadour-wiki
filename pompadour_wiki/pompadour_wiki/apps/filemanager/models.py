# -*- coding: utf-8 -*-

from django.db import models

from pompadour_wiki.apps.wiki.models import Wiki

class Attachment(models.Model):
    wiki = models.ForeignKey(Wiki)
    page = models.CharField(max_length=512)
    file = models.CharField(max_length=512)
    mimetype = models.CharField(max_length=100)

    def __unicode__(self):
        return u'{0} -> {1}'.format(self.file, self.page)