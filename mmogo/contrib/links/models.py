from django.db import models

class Link(models.Model):
    WEBSITE = 0
    FACEBOOK = 1
    TWITTER = 2
    INSTAGRAM = 3
    LINKEDIN = 4
    PINTEREST = 5

    LINK_TYPE_CHOICES = (
        (WEBSITE, 'Website'),
        (FACEBOOK, 'Facebook'),
        (TWITTER, 'Twitter'),
        (INSTAGRAM, 'Instagram'),
        (LINKEDIN, 'LinkedIn'),
        (PINTEREST, 'Pinterest'),
    )
    link = models.CharField(max_length=255)
    ordering = models.SmallIntegerField(default=0)
    link_type = models.SmallIntegerField(default=WEBSITE, choices=LINK_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'links'
        ordering = ('ordering',)
        verbose_name = 'Link'
        verbose_name_plural = 'Links'


    def __str__(self):
        return str(self.product)
    

    @property
    def type_display(self):
        return self.LINK_TYPE_CHOICES[self.link_type][1]