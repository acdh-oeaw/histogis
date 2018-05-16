import lxml.etree as ET
import csv
from .models import SkosConcept, SkosConceptScheme, SkosLabel


class Csv2SkosReader(object):
    """
    extract SKOS-like objects from special structured CSV sheets
    and returns a list of dictionaries containing data needed to
    create vocabs-entries
    """

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = [x for x in csv.reader(self.csv_file)]
        self.headers = self.data[0]
        try:
            self.alt_lang = (self.headers[1])[(self.headers[1]).index('@')+1:]
        except:
            self.alt_lang = None
        self.schemes = set([x[0] for x in self.data[1:]])
        self.number_of_schemes = len(self.schemes)

    def get_concepts(self):
        concepts = []
        for x in self.data[1:]:
            first_order = x[1].split('|')
            if x[2] != '':
                second_order = x[2].split('|')
                concept = {
                    'scheme': x[0],
                    'concept': {
                        'pref_label': first_order[0],
                        'pref_label_lang': 'eng',
                        'alt_label': self.alt_lang,
                        'alt_label_lang': self.alt_lang,
                        'narrower': {
                            'scheme': x[0],
                            'concept': {
                                'pref_label': second_order[0],
                                'pref_label_lang': 'eng',
                                'alt_label': second_order[1],
                                'alt_label_lang': self.alt_lang,
                            }
                        }
                    }
                }
            else:
                concept = {
                    'scheme': x[0],
                    'concept': {
                        'pref_label': first_order[0],
                        'pref_label_lang': 'eng',
                        'alt_label': first_order[1],
                        'alt_label_lang': self.alt_lang,
                    }
                }
            concepts.append(concept)

        return concepts


class Csv2SkosImporter(Csv2SkosReader):
    """Takes a special formatted csv file, parses it and imports the derived data into vocabs"""

    def update_schemes(self):
        """import/updates all conceptSchemes found in csv"""
        report = {}
        report['before'] = len(SkosConceptScheme.objects.all())
        failed = []
        success = []
        for x in self.schemes:
            try:
                clean = x.split('|')[0].strip()
            except:
                clean = x.strip()
            try:
                temp_scheme, _ = SkosConceptScheme.objects.get_or_create(dc_title=clean)
                temp_scheme.save()
                success.append(x)
            except:
                failed.append(x)
        report['failed'] = failed
        report['success'] = success
        report['after'] = len(SkosConceptScheme.objects.all())
        return report

    def importConcepts(self):
        """import/updates all SkosConcepts found in csv"""
        report = {}
        report['before'] = len(SkosConcept.objects.all())
        report['schemes_before'] = len(SkosConceptScheme.objects.all())
        failed = []
        success = []
        for x in self.get_concepts():
            # get scheme
            try:
                clean = x['scheme'].split('|')[0].strip()
            except:
                clean = x['scheme'].strip()
            temp_scheme, _ = SkosConceptScheme.objects.get_or_create(dc_title=clean)
            # crete 1st order
            try:
                temp_label, _ = SkosLabel.objects.get_or_create(
                    label=x['concept']['alt_label'],
                    label_type='altLabel',
                    isoCode=x['concept']['alt_label_lang']
                )
                temp_first, _ = SkosConcept.objects.get_or_create(
                    pref_label=x['concept']['pref_label'],
                    pref_label_lang=x['concept']['pref_label_lang']
                )
                temp_first.label = [temp_label]
                temp_first.scheme = [temp_scheme]
                success.append(x['concept']['pref_label'])
            except:
                failed.append(x['concept']['pref_label'])
            try:
                second = x['concept']['narrower']['concept']
                # crete 2st order
                try:
                    temp_label, _ = SkosLabel.objects.get_or_create(
                        label=second['alt_label'],
                        label_type='altLabel',
                        isoCode=second['alt_label_lang']
                    )
                    temp_second, _ = SkosConcept.objects.get_or_create(
                        pref_label=second['pref_label'],
                        pref_label_lang=second['pref_label_lang']
                    )
                    temp_second.label = [temp_label]
                    temp_second.scheme = [temp_scheme]
                    temp_first.skos_narrower = [temp_second]
                    success.append(second['pref_label'])
                except:
                    failed.append(second['pref_label'])
            except:
                pass
        report['failed'] = failed
        report['success'] = success
        report['after'] = len(SkosConcept.objects.all())
        report['schemes_after'] = len(SkosConceptScheme.objects.all())
        return report

    def update_concepts(self):
        """import/updates all SkosConcepts found in csv"""
        report = {}
        report['before'] = len(SkosConcept.objects.all())
        failed = []
        success = []
        for x in self.get_concepts():
            # print(x['concept'])
            pass
        report['after'] = len(SkosConcept.objects.all())
        return report


class SkosReader(object):

    """
    reads a skos file (RDF/XML) and returns a list of dictionaries
    containing rdf:Description properties
    concept-id: (URL)
    notation: (derived from concept-id)
    pref_labels: (list of labels)
    skos:broader: (list of broader elements)
    skos:narrower: ...
    skos:closeMatch ...
    skos:inScheme: (list of all conceptSchemes a concept is related to
    """

    def __init__(self, skosfile):
        self.ns_skos = "http://www.w3.org/2004/02/skos/core#"
        self.ns_rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        self.skosfile = skosfile

        try:
            self.tree = ET.parse(skosfile)
            self.parsed_file = ET.tostring(self.tree, encoding="utf-8")
        except:
            self.parsed_file = "parsing didn't work"

        try:
            self.extractedDescriptions = self.tree.findall(
                'rdf:Description', namespaces={"rdf": self.ns_rdf})
            self.numberOfextractedDescriptions = len(self.extractedDescriptions)
        except:
            self.extractedDescriptions = "rdf:Descriptions could not be extracted."
            self.numberOfextractedDescriptions = 0

    def returnDescriptions(self):
        descriptions = []
        for x in self.extractedDescriptions:
            description = {}
            temp_type = x.find('rdf:type', namespaces={"rdf": self.ns_rdf})
            if temp_type is not None:
                description["type"] = temp_type.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
            else:
                description["type"] = "no type"
            description["id"] = x.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']
            description["notation"] = x.find('skos:notation', namespaces={"skos": self.ns_skos})

            skos_pref_labels = []
            for y in x.findall('skos:prefLabel', namespaces={"skos": self.ns_skos}):
                skos_label = {}
                skos_label['text'] = y.text
                skos_label['lang'] = y.attrib['{http://www.w3.org/XML/1998/namespace}lang']
                skos_pref_labels.append(skos_label)
            description["pref_labels"] = skos_pref_labels
            skos_definitions = []
            for y in x.findall('skos:definition', namespaces={"skos": self.ns_skos}):
                skos_definitions.append(y.text)
            description["definitions"] = skos_definitions

            skos_alt_labels = []
            for y in x.findall('skos:altLabel', namespaces={"skos": self.ns_skos}):
                skos_label = {}
                skos_label['text'] = y.text
                skos_label['lang'] = y.attrib['{http://www.w3.org/XML/1998/namespace}lang']
                skos_alt_labels.append(skos_label)
            description["alt_labels"] = skos_alt_labels

            skos_broader = []
            for y in x.findall('skos:broader', namespaces={"skos": self.ns_skos}):
                broader = {}
                broader['uri'] = y.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
                broader['notation'] = broader['uri'].split('/')[-1]
                skos_broader.append(broader)
            description['broader'] = skos_broader

            skos_narrower = []
            for y in x.findall('skos:narrower', namespaces={"skos": self.ns_skos}):
                narrower = {}
                narrower['uri'] = y.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
                narrower['notation'] = narrower['uri'].split('/')[-1]
                skos_narrower.append(narrower)
            description['narrower'] = skos_narrower

            skos_closeMatch = []
            for y in x.findall('skos:closeMatch', namespaces={"skos": self.ns_skos}):
                closeMatch = {}
                closeMatch['uri'] = y.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
                closeMatch['notation'] = closeMatch['uri'].split('/')[-1]
                skos_closeMatch.append(closeMatch)
            description['closeMatch'] = skos_closeMatch

            skos_schemes = []
            for y in x.findall('skos:inScheme', namespaces={"skos": self.ns_skos}):
                skos_schemes.append(
                    y.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'])
            description["schemes"] = skos_schemes
            descriptions.append(description)
        return descriptions

    def countConcepts(self):
        return len(self.returnDescriptions())


class SkosImporter(SkosReader):

    """Imports concepts and concept schemes to django application/database"""

    def importConcepts(self):
        concepts_before = len(SkosConcept.objects.all())
        num_description_type_concept = 0
        num_description_type_concept_scheme = 0
        for x in self.returnDescriptions():
            if x["type"] == "http://www.w3.org/2004/02/skos/core#ConceptScheme":
                temp_concept_scheme, _ = SkosConceptScheme.objects.get_or_create(legacy_id=x["id"])
                temp_concept_scheme.save()
                num_description_type_concept_scheme += 1

            else:
                temp_uri = x['id']
                temp_notation = temp_uri.split('/')[-1]
                temp_concept, _ = SkosConcept.objects.get_or_create(
                    legacy_id=temp_uri, notation=temp_notation)
                try:
                    temp_concept.pref_label = x['pref_labels'][0]["text"]
                    temp_concept.pref_label_lang = x['pref_labels']["lang"]
                except:
                    pass
                try:
                    temp_concept.definition = x['definitions'][0]
                    temp_concept.definition_lang = "eng"
                except:
                    pass
                temp_concept.save()

                for y in x['pref_labels'][1:]:
                    temp_label, _ = SkosLabel.objects.get_or_create(
                        label=y["text"],
                        isoCode=y["lang"],
                        label_type="prefLabel"
                    )
                    temp_concept.label = [temp_label]
                    temp_concept.save()

                for y in x['alt_labels'][1:]:
                    temp_label, _ = SkosLabel.objects.get_or_create(
                        label=y["text"],
                        isoCode=y["lang"],
                        label_type="altLabel"
                    )
                    temp_concept.label = [temp_label]
                    temp_concept.save()

                for z in x['schemes']:
                    temp_scheme, _ = SkosConceptScheme.objects.get_or_create(
                        legacy_id=z
                    )
                    scheme_dctitle = z.split('/')[-1]
                    temp_scheme.dc_title = scheme_dctitle
                    temp_scheme.save()
                    temp_concept.scheme = [temp_scheme]
                    temp_concept.save()

                for y in x['broader']:
                    temp_broader, _ = SkosConcept.objects.get_or_create(
                        legacy_id=y["uri"], notation=y["notation"])
                    temp_broader.save()
                    temp_concept.skos_broader = [temp_broader]
                    temp_concept.save()

                for y in x['narrower']:
                    temp_narrower, _ = SkosConcept.objects.get_or_create(
                        legacy_id=y["uri"], notation=y["notation"])
                    temp_narrower.save()
                    temp_concept.skos_narrower = [temp_narrower]
                    temp_concept.save()

                for y in x['closeMatch']:
                    temp_closeMatch, _ = SkosConcept.objects.get_or_create(
                        legacy_id=y["uri"], notation=y["notation"])
                    temp_closeMatch.save()
                    temp_concept.skos_closematch = [temp_closeMatch]
                    temp_concept.save()

                num_description_type_concept += 1
        concepts_after = len(SkosConcept.objects.all())
        summary = "#descr. type 'concept': {} |  #descr. type 'conceptSchemes': {}".format(
            num_description_type_concept, num_description_type_concept_scheme
        )

        report = {'summary': summary, 'before': concepts_before, 'after': concepts_after}
        return report

    def test_if_class_works(self):
        check = "Works!"
        return check
