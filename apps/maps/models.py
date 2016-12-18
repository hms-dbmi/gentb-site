"""
Provide a place for city and country geo data for showing on maps.
"""
import os

from django.db.models import *
from django.contrib.gis.db.models import *
from django.utils.encoding import python_2_unicode_compatible

# This is where we are currently looking for data, but it could change.
url_prefix = 'http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/'

# UN Regions and sub-regions
REGIONS = (
  (0, 'Other'),
  (1, 'World'),
  (2, 'Agrica'),
  (9, 'Oceania'),
  (19, 'Americas'),
  (21, 'North America'),
  (142, 'Asia'),
  (150, 'Europe'),
  (419, 'Latin America and the Caribbean'),
)
SUB_REGIONS = (
  (14, 'Eastern Africa'),
  (17, 'Middle Africa'),
  (15, 'Northern Africa'),
  (18, 'Southern Africa'),
  (11, 'Western Africa'),

  (29, 'Caribbean'),
  (13, 'Central America'),
  (5, 'South America'),

  (143, 'Central Asia'),
  (30, 'Eastern Asia'),
  (34, 'Southern Asia'),
  (35, 'South-Eastern Asia'),
  (145, 'Western Asia'),

  (151, 'Eastern Europe'),
  (154, 'Northern Europe'),
  (39, 'Southern Europe'),
  (155, 'Western Europe'),

  (53, 'Australia and New Zealand'),
  (54, 'Melanesia'),
  (57, 'Micronesia'),
  (61, 'Polynesia'),
)

@python_2_unicode_compatible
class Country(Model):
    """Provides a simple shape and a couple of useful fields to identify a country."""
    name = CharField(max_length=128, unique=True)

    iso2 = CharField(max_length=5, unique=True, db_index=True)
    iso3 = CharField(max_length=5, unique=True, db_index=True)

    region = IntegerField(choices=REGIONS, null=True, blank=True)
    subregion = IntegerField(choices=SUB_REGIONS, null=True, blank=True)

    geom = MultiPolygonField(srid=4326)
    objects = GeoManager()

    online_zip = 'http://thematicmapping.org/downloads/TM_WORLD_BORDERS_SIMPL-0.3.zip'
    mapping_id = 'iso2'
    mapping = { 
        'iso2': 'ISO2',
        'iso3': 'ISO3',
        'geom': 'POLYGON',
        'name': 'NAME',
        'region': 'REGION',
        'subregion': 'SUBREGION',
    }

    class Meta:
        verbose_name_plural = 'countries'
        ordering = ('name',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class CountryDetail(Model):
    """Provides a much more details country shape and more fields"""
    country = OneToOneField(Country, related_name='detail')

    name_short = CharField(max_length=36, null=True, blank=True)
    name_abbr = CharField(max_length=13, null=True, blank=True)

    continent = CharField(max_length=23, null=True, blank=True)

    pop = FloatField(null=True, blank=True)
    gdp = FloatField(null=True, blank=True)
    rank = FloatField(null=True, blank=True)
    mapcolor = FloatField(null=True, blank=True)

    geom = MultiPolygonField(srid=4326)

    online_zip = os.path.join(url_prefix, 'ne_10m_admin_0_countries.zip')
    mapping_id = 'country'
    mapping = {
        'country' : {'iso2': 'ISO_A2'},
        'rank' : 'scalerank',
        'name_short' : 'NAME',
        'name_abbr' : 'ABBREV',
        'mapcolor' : 'MAPCOLOR7',
        'gdp' : 'GDP_MD_EST',
        'continent' : 'CONTINENT',
        'geom' : 'MULTIPOLYGON',
    }
    
    class Meta:
        ordering = ('-pop',)

    def __str__(self):
        return self.name_short or self.name_abbr or self.country_id


@python_2_unicode_compatible
class Place(Model):
    """A populated place from the world map source"""
    name = CharField(max_length=128)
    country = ForeignKey(Country, related_name='places')

    latitude = FloatField()
    longitude = FloatField()

    pop = FloatField()
    rank = IntegerField()

    elevation = FloatField()
    timezone = CharField(max_length=254)
    geom = MultiPointField(srid=4326)
    objects = GeoManager()

    online_zip = os.path.join(url_prefix, 'ne_10m_populated_places.zip')
    mapping_id = ('name', 'country')
    mapping = { 
        'pop' : 'GN_POP',
        'rank' : 'SCALERANK',
        'name' : 'NAME',
        'country' : {'iso2': 'ISO_A2'},
        'latitude' : 'LATITUDE',
        'longitude' : 'LONGITUDE',
        'elevation' : 'ELEVATION',
        'timezone' : 'TIMEZONE',
        'geom' : 'MULTIPOINT',
    }   

    class Meta:
        ordering = ('-pop',)

    def __str__(self):
        return self.name

