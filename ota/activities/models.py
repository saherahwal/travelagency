from django.db import models
from common.models import *


class GeneralInterest(TimeStampedModel):
    """
    Describes general interests of activities displayed to the user
    e.g ( Adventure, Family, Beach, Shopping, Romance, Night-life )
    """
    name = models.CharField(max_length=100)


class Activity(TimeStampedModel):
    """
    Describes activities (sub-set of General Interests)
    e.g ( Rafting, Skiing, Swimming, Snorekling, Snowboarding)
    """
    name = models.CharField(max_length=100)
    
