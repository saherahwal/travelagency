from django.db import models
from common.models import TimeStampedModel
from django.contrib.auth.models import User

TAG_MAX_SZ = 200
BLOG_NAME_MAX_SZ = 200
SHORT_DESC_SZ = 600
VIDEO_URL_SZ = 700

UPLOAD_TO_IMG = 'blogs/images/'
UPLOAD_TO_VIDEO = 'blogs/videos/'

class Tag(TimeStampedModel):
    """
        Tag / Category for blob entry
    """
    title = models.CharField(max_length=TAG_MAX_SZ, unique=True)
    slug = models.SlugField(max_length=TAG_MAX_SZ, unique=True)

    def __unicode__(self):
        return '%s' % self.title


class Blog(TimeStampedModel):
    """
        Blog model
    """
    # title
    title = models.CharField( max_length=BLOG_NAME_MAX_SZ, unique=True )

    # slug
    slug = models.SlugField(max_length=BLOG_NAME_MAX_SZ, unique=True)

    # user who posted blog entry
    blog_by = models.ForeignKey( User, related_name='blog_by_user')

    # body
    blog_body = models.TextField()

    # short description (part of body)
    short_desc = models.CharField( max_length = SHORT_DESC_SZ )

    # tags
    tags = models.ManyToManyField( Tag )

    # main img for blog title / entry
    img = models.ImageField( upload_to = UPLOAD_TO_IMG, blank=True )

    # video file for blog entry
    video_file = models.FileField( upload_to = UPLOAD_TO_VIDEO,  blank=True )

    # video youtube link - embed (includes iframe)
    embed_video_url = models.CharField( max_length = VIDEO_URL_SZ,  blank=True )

    # visibility to admin only
    admin_visible_only = models.BooleanField()

    def __unicode__(self):
        return '%s' % self.title

# TODO: add class Comment - allow users to comment on blog straight on the site
# for v1 - facebook page / twitter account will be sufficient - way to control comments straight on
# site
