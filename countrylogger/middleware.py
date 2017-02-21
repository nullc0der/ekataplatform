from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.auth.models import User

from hashtag.views import get_client_ip
from countrylogger.models import UserCountry


class CountryMiddleWare(object):
    def process_request(self, request):
        try:
            g = GeoIP2()
            country = g.country(get_client_ip(request))
            usercountry, created = UserCountry.objects.get_or_create(
                name=country['country_name']
            )
            usercountry.users.add(request.user)
        except:
            pass
