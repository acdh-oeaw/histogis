from django.conf import settings
from rest_framework_gis.serializers import GeoFeatureModelSerializer

try:
    if settings.BASE_URL.endswith("/"):
        base_url = settings.BASE_URL[:-1]
    else:
        base_url = settings.BASE_URL
except AttributeError:
    base_url = "http://PROVIDE-A-SERVER-BASE-URL"


class LinkedPastsSerializer(GeoFeatureModelSerializer):
    def to_representation(self, instance):
        feature = super().to_representation(instance)
        when = {
            "timespans": [
                {"start": {"in": instance.start_date}, "end": {"in": instance.end_date}}
            ]
        }
        names = [{"toponym": instance.name}]
        if len(instance.alt_name_list()) > 0:
            all_names = [{"toponym": x} for x in instance.alt_name_list()]
            all_names = names + all_names
        else:
            all_names = names
        types = [
            {
                "identifier": f"{base_url}{instance.administrative_unit.get_absolute_url()}",
                "label": instance.administrative_unit.pref_label,
            }
        ]
        descriptions = [
            {
                "value": f"{instance.source.description}",
                "lang": "en",
            }
        ]
        feature["when"] = when
        feature["names"] = all_names
        feature["types"] = types
        feature["descriptions"] = descriptions
        if instance.wikidata_id == "":
            pass
        else:
            links = [
                {
                    "type": "skos:closeMatch",
                    "identifier": f"http://www.wikidata.org/entity/{instance.wikidata_id}",
                }
            ]
            feature["links"] = links
        feature["@id"] = f"{base_url}{instance.get_permalink_url()}"
        return feature
