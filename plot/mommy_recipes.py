# coding=utf-8

from geopy import Point
from random import random
from faker import Faker
from faker.providers import BaseProvider
from model_mommy.recipe import Recipe

from edc_base.test_mixins.reference_date_mixin import ReferenceDateMixin

from .constants import RESIDENTIAL_HABITABLE, TWENTY_PERCENT
from .models import Plot, PlotLogEntry, PlotLog


class ReferenceDate(ReferenceDateMixin):
    consent_model = 'edc_example.subjectconsent'


def get_utcnow():
    return ReferenceDate().get_utcnow()


class GpsProvider(BaseProvider):

    target_point = Point(-25.330451, 25.556502)

    def target_latitude(self):
        return self.target_point.latitude - random() / 10000000

    def target_longitude(self):
        return self.target_point.longitude - random() / 10000000

    def confirmed_latitude(self):
        return self.target_point.latitude - random() / 10000000

    def confirmed_longitude(self):
        return self.target_point.longitude - random() / 10000000

fake = Faker()
fake.add_provider(GpsProvider)

plot = Recipe(
    Plot,
    report_datetime=get_utcnow,
    map_area='test_community',
    household_count=1,
    status=RESIDENTIAL_HABITABLE,
    eligible_members=5,
    selected=TWENTY_PERCENT,
    gps_target_lat=fake.target_latitude,
    gps_target_lon=fake.target_longitude,
)

plotlog = Recipe(
    PlotLog,
    # report_datetime=get_utcnow,
)

plotlogentry = Recipe(
    PlotLogEntry,
    report_datetime=get_utcnow,
)