import pickle
import os
import re


from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist
from django.db.models.query import QuerySet

from rdflib import Graph, Namespace, URIRef, Literal, XSD
from rdflib.namespace import RDF, SKOS

from browsing.browsing_utils import model_to_dict
from webpage.metadata import PROJECT_METADATA

ARCHE_CONST_MAPPINGS = getattr(settings, 'ARCHE_CONST_MAPPINGS', False)

ARCHE_LANG = getattr(settings, 'ARCHE_LANG', 'en')
ARCHE_BASE_URL = getattr(settings, 'ARCHE_BASE_URL', 'https://id.acdh.oeaw.ac.at/MYPROJECT')

ARCHE_DEFAULT_EXTENSION = getattr(settings, 'ARCHE_DEFAULT_EXTENSION', 'geojson')
ARCHE_PAYLOAD_MIMETYPE = getattr(settings, 'ARCHE_PAYLOAD_MIMETYPE', 'application/geo+json')


repo_schema = "https://raw.githubusercontent.com/acdh-oeaw/repo-schema/master/acdh-schema.owl"
acdh_ns = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")
owl_ns = Namespace("http://www.w3.org/2002/07/owl#")
rdfs_ns = Namespace("http://www.w3.org/2000/01/rdf-schema#")

pandorfer = URIRef("https://d-nb.info/gnd/1043833846")
mschloegl = URIRef("https://d-nb.info/gnd/1154715620")
apiechl = URIRef("https://orcid.org/0000-0002-9239-5577")
adueck = URIRef("https://orcid.org/0000-0003-3392-2610")
pmarck = URIRef("https://orcid.org/0000-0003-1816-4823")


def get_prop_types(repo_schema_url=repo_schema):
    g = Graph()
    g.parse(repo_schema, format='xml')
    prop_types = {}
    for s in g.subjects(RDF.type, None):
        if s.startswith('https://vocabs.acdh'):
            prop_name = s.split('#')[-1]
            for range_prop in g.objects(s, rdfs_ns.range):
                prop_types[prop_name] = range_prop.split('#')[-1]
    return prop_types


ARCHE_PROPS_LOOKUP = get_prop_types()


def serialize_project():
    g = Graph()
    sub = URIRef(f"{ARCHE_BASE_URL}")
    proj_sub = URIRef(f"{ARCHE_BASE_URL}/project")
    # HistoGIS Project
    proj_g = Graph()
    proj_g.add(
        (proj_sub, RDF.type, acdh_ns.Project)
    )
    proj_g.add(
        (proj_sub, acdh_ns.hasTitle, Literal(f"HistoGIS (Project)", lang=ARCHE_LANG))
    )
    proj_g.add(
        (proj_sub, acdh_ns.hasStartDate, Literal(f"2018-03-01", datatype=XSD.date))
    )
    proj_g.add(
        (proj_sub, acdh_ns.hasEndDate, Literal(f"2020-11-30", datatype=XSD.date))
    )
    proj_g.add(
        (proj_sub, acdh_ns.hasFunder, URIRef("https://id.acdh.oeaw.ac.at/oeaw"))
    )
    for x in [adueck, apiechl, pmarck]:
        proj_g.add(
            (proj_sub, acdh_ns.hasContributor, x)
        )
    proj_g.add(
        (proj_sub, acdh_ns.hasPrincipalInvestigator, pandorfer)
    )
    proj_g.add(
        (proj_sub, acdh_ns.hasPrincipalInvestigator, mschloegl)
    )
    proj_g.add(
        (proj_sub, acdh_ns.hasRelatedCollection, sub)
    )
    proj_g.add(
        (
            proj_sub,
            acdh_ns.hasDescription,
            Literal(f"{PROJECT_METADATA['description']}", lang=ARCHE_LANG))
    )
    for const in ARCHE_CONST_MAPPINGS:
        arche_prop_domain = ARCHE_PROPS_LOOKUP.get(const[0], 'No Match')
        if arche_prop_domain == 'date':
            proj_g.add((proj_sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
        if arche_prop_domain == 'string':
            proj_g.add((proj_sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
        else:
            proj_g.add((proj_sub, acdh_ns[const[0]], URIRef(const[1])))
    # HistoGIS Root Collection
    g.add((sub, RDF.type, acdh_ns.Collection))
    g.add(
        (
            sub,
            acdh_ns.hasPid,
            Literal(
                'http://hdl.handle.net/21.11115/0000-000C-E12A-7', datatype=XSD.anyURI
            )
        )
    )
    g.add(
        (sub, acdh_ns.hasCoverageStartDate, Literal('1890-01-01', datatype=XSD.date))
    )
    g.add(
        (sub, acdh_ns.hasCoverageEndDate, Literal('1920-12-31', datatype=XSD.date))
    )
    g.add(
        (sub, acdh_ns.hasTitle, Literal(f"{PROJECT_METADATA['title']}", lang=ARCHE_LANG))
    )
    g.add(
        (sub, acdh_ns.hasOaiSet, Literal(f"kulturpool"))
    )
    g.add(
        (sub, acdh_ns.hasRelatedProject, proj_sub)
    )
    g = g + proj_g
    # define persons
    g.add((pandorfer, RDF.type, acdh_ns.Person))
    g.add((pandorfer, acdh_ns.hasTitle, Literal('Peter Andorfer', lang="de")))

    g.add((mschloegl, RDF.type, acdh_ns.Person))
    g.add((mschloegl, acdh_ns.hasTitle, Literal('Matthias Schlögl', lang="de")))
    g.add((mschloegl, acdh_ns.hasFirstName, Literal('Matthias', lang="de")))
    g.add((mschloegl, acdh_ns.hasLastName, Literal('Schlögl', lang="de")))

    g.add((apiechl, RDF.type, acdh_ns.Person))
    g.add((apiechl, acdh_ns.hasTitle, Literal('Anna Piechl', lang="de")))
    g.add((apiechl, acdh_ns.hasFirstName, Literal('Piechl', lang="de")))
    g.add((apiechl, acdh_ns.hasLastName, Literal('Anna', lang="de")))
    g.add((sub, acdh_ns.hasCreator, apiechl))

    g.add((adueck, RDF.type, acdh_ns.Person))
    g.add((adueck, acdh_ns.hasTitle, Literal('Antonia Dückelmann', lang="de")))
    g.add((adueck, acdh_ns.hasFirstName, Literal('Dückelmann', lang="de")))
    g.add((adueck, acdh_ns.hasLastName, Literal('Antonia', lang="de")))
    g.add((sub, acdh_ns.hasCreator, adueck))

    g.add((pmarck, acdh_ns.type, acdh_ns.Person))
    g.add((pmarck, acdh_ns.hasTitle, Literal('Peter Paul Marckhgott-Sanabria', lang="de")))
    g.add((pmarck, acdh_ns.hasFirstName, Literal('Marckhgott-Sanabria', lang="de")))
    g.add((pmarck, acdh_ns.hasLastName, Literal('Peter Paul', lang="de")))
    g.add((sub, acdh_ns.hasCreator, pmarck))
    g.add(
        (
            sub,
            acdh_ns.hasDescription,
            Literal(f"{PROJECT_METADATA['description']}", lang=ARCHE_LANG))
    )
    for const in ARCHE_CONST_MAPPINGS:
        arche_prop_domain = ARCHE_PROPS_LOOKUP.get(const[0], 'No Match')
        if arche_prop_domain == 'date':
            col.add()
            g.add((sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
        if arche_prop_domain == 'string':
            g.add((sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
        else:
            g.add((sub, acdh_ns[const[0]], URIRef(const[1])))
    return g


def get_arche_id(res, id_prop="pk", arche_uri=ARCHE_BASE_URL):
    """ function to generate generic ARCHE-IDs
        :param res: A model object
        :param id_prop: The object's primary key property
        :param arche_uri: A base url; should be configued in the subs settings file
        :return: An ARCHE-ID (URI)
    """
    if isinstance(res, str):
        return res
    else:
        app_name = res.__class__._meta.app_label.lower()
        class_name = res.__class__.__name__.lower()
        return "/".join(
            [arche_uri, app_name, class_name, f"{getattr(res, id_prop)}"]
        )


def as_arche_graph(res):
    g = Graph()
    sub = URIRef(f"{ARCHE_BASE_URL}/{res.source.slug_name()}/{res.slug_name()}")
    g.add(
        (
            sub, acdh_ns.hasTitle,
            Literal(f"{res}", lang=ARCHE_LANG)
        )
    )
    g.add(
        (sub, acdh_ns.hasOaiSet, Literal(f"kulturpool"))
    )
    alt_names = res.alt_name.replace(',', ';')
    for x in alt_names.split(';'):
        if x is not "":
            g.add(
                (
                    sub, acdh_ns.hasAlternativeTitle,
                    Literal(
                        f"{x.strip()}",
                        lang=ARCHE_LANG
                    )
                )
            )
    if res.administrative_unit.pref_label is not None or '':
        g.add(
            (
                sub,
                acdh_ns.hasSubject,
                Literal(
                    f"{res.administrative_unit.pref_label}",
                    lang=f"{res.administrative_unit.pref_label_lang[:1]}"
                )
            )
        )
    # g.add(
    #     (
    #         sub, acdh_ns.hasDescription,
    #         Literal(
    #             f"{res} is part of {res.source}: {res.source.description}",
    #             lang=ARCHE_LANG
    #         )
    #     )
    # )
    quote = res.source.quote
    g.add(
        (
            sub, acdh_ns.hasDescription,
            Literal(
                f"{res} in: {quote}",
                lang=ARCHE_LANG,
            )
        )
    )
    g.add(
        (
            sub, acdh_ns.hasDescription,
            Literal(
                f"",
                lang=ARCHE_LANG
            )
        )
    )
    if 'Marckhgott' in quote:
        g.add((sub, acdh_ns.hasCreator, pmarck))
    if 'Piechl' in quote:
        g.add((sub, acdh_ns.hasCreator, apiechl))
    if 'Dückelmann' in quote:
        g.add((sub, acdh_ns.hasCreator, adueck))
    g.add((sub, RDF.type, acdh_ns.Resource))
    g.add(
        (
            sub,
            acdh_ns.hasNonLinkedIdentifier,
            Literal(
                f"HistoGIS DB-ID {res.id}",
                lang=ARCHE_LANG)
            )
    )
    g.add(
        (
            sub,
            acdh_ns.hasNonLinkedIdentifier,
            Literal(
                f"Wikidata ID: {res.wikidata_id}")
            )
    )
    col = Graph()
    col_sub = URIRef(f"{ARCHE_BASE_URL}/{res.source.slug_name()}")
    g.add((col_sub, RDF.type, acdh_ns.Collection))
    g.add((col_sub, acdh_ns.hasDescription, Literal("", lang=ARCHE_LANG)))
    # g.add((col_sub, acdh_ns.hasDescription, Literal(res.source.description, lang=ARCHE_LANG)))
    col.add(
        (col_sub, acdh_ns.isPartOf, URIRef(f"{ARCHE_BASE_URL}"))
    )
    col.add(
        (col_sub, acdh_ns.hasOaiSet, Literal(f"kulturpool"))
    )
    col.add(
        (
            col_sub,
            acdh_ns.hasTitle,
            Literal(
                f"{res.source}",
                lang=ARCHE_LANG)
            )
    )
    g.add(
        (sub, acdh_ns.isPartOf, col_sub)
    )
    g.add(
        (sub, SKOS.narrowMatch, Literal(res.sanitize_wikidataid(), datatype=XSD.anyURI))
    )
    if res.start_date is not None:
        g.add(
            (
                sub,
                acdh_ns.hasCoverageStartDate,
                Literal(res.start_date, datatype=XSD.date)
            )
        )
    if res.end_date is not None:
        g.add(
            (
                sub,
                acdh_ns.hasCoverageEndDate,
                Literal(res.end_date, datatype=XSD.date)
            )
        )
    g.add(
        (
            sub,
            acdh_ns.hasCategory,
            URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/dataset/geojson"))
    )
    for const in ARCHE_CONST_MAPPINGS:
        arche_prop_domain = ARCHE_PROPS_LOOKUP.get(const[0], 'No Match')
        if arche_prop_domain == 'date':
            col.add()
            g.add((sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
            col.add((col_sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
        if arche_prop_domain == 'string':
            g.add((sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
            col.add((col_sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
        else:
            g.add((sub, acdh_ns[const[0]], URIRef(const[1])))
            col.add((col_sub, acdh_ns[const[0]], URIRef(const[1])))
    g = g + col
    return g
