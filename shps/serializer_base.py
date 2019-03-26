from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.conf import settings

try:
    if settings.BASE_URL.endswith('/'):
        base_url = settings.BASE_URL[:-1]
    else:
        base_url = settings.BASE_URL
except AttributeError:
    base_url = "http://PROVIDE-A-SERVER-BASE-URL"


class LinkedPastsSerializer(GeoFeatureModelSerializer):

    def to_representation(self, instance):
        feature = super(LinkedPastsSerializer, self).to_representation(instance)
        when = {
            "timespans": [
                {
                    "start": {
                        "in": instance.start_date
                    },
                    "end": {
                        "in": instance.end_date
                    }
                }
            ]
        }
        names = [
            {"toponym": instance.name}
        ]
        if len(instance.alt_name_list()) > 1:
            all_names = [names.append({"toponym": x} for x in instance.alt_name_list())]
        else:
            all_names = names
        types = [
            {
                "identifier": "{}{}".format(
                    base_url,
                    instance.administrative_unit.get_absolute_url()
                ),
                "label": instance.administrative_unit.pref_label
            }
        ]
        descriptions = [
            {
                "value": "{}".format(instance.source.description),
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
                    "identifier": instance.wikidata_id
                }
            ]
            feature["links"] = links
        feature["@id"] = "{}{}".format(base_url, instance.get_permalink_url())
        return feature
