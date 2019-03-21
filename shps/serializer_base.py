from rest_framework_gis.serializers import GeoFeatureModelSerializer


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
                "identifier": "histogisadm:{}".format(
                    instance.administrative_unit.id
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
                    "type": "seeAlso",
                    "identifier": instance.wikidata_id
                }
            ]
            feature["links"] = links
        return feature
