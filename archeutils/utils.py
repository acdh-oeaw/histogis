from django.conf import settings
from rdflib import Graph, Namespace, URIRef, Literal, XSD
from rdflib.namespace import RDF

from webpage.metadata import PROJECT_METADATA

ARCHE_CONST_MAPPINGS = getattr(settings, "ARCHE_CONST_MAPPINGS", False)
ARCHE_CONST_MAPPINGS_SIMPLE = getattr(settings, "ARCHE_CONST_MAPPINGS_SIMPLE", False)

ARCHE_LANG = getattr(settings, "ARCHE_LANG", "en")
ARCHE_BASE_URL = getattr(
    settings, "ARCHE_BASE_URL", "https://id.acdh.oeaw.ac.at/MYPROJECT"
)

ARCHE_DEFAULT_EXTENSION = getattr(settings, "ARCHE_DEFAULT_EXTENSION", "geojson")
ARCHE_PAYLOAD_MIMETYPE = getattr(
    settings, "ARCHE_PAYLOAD_MIMETYPE", "application/geo+json"
)

TOP_COL_DESC = """A geodata collection on historical political/administrative units created and collected for the HistoGIS Project.
The region covered is Europe with a special focus on Central Europe / Austria(-Hungary) and German States,  the temporal extent is from c. 1815 to c. 1919. National borders are available for the whole temporal extent and all of Europe, while lower level administrative borders (provinces, counties, etc.) are available for the focus areas.
Data is provided in GeoJSON format following the “The Linked Places format (LPF)” recommendations. The files contain geometries, timespans as well as additional attribute data. The data is structured along three axes: Geographical / political region, contemporary administrative level and time."""

PROJECT_DESC = """The HistoGIS project creates and publishes machine readable data about historical administrative units. Maps, either historic ones or maps displaying past (political) border lines, has been georeferenced and the actual information about the former borderlines was captured as GeoJSON together with necessary metadata like the name of the temporal spatial entity, its start and end dates, alternative names as well as potential matching Wikidata IDs.
The project was funded by the Austrian Academy of Sciences (Innovationsfonds), run from March 2018 until October 2020 and was led by Peter Andorfer and Matthias Schlögl. The actual work on the data was done by Antonia Dückelmann, Anna Piechl and Peter Paul Marckhgott-Sanabria with support from the interns Laura Elmer and Liam Downs-Tepper.
Besides the data the project HistoGIS comprises a web service to query the data (https://histogis.acdh.oeaw.ac.at)"""


repo_schema = (
    "https://raw.githubusercontent.com/acdh-oeaw/repo-schema/master/acdh-schema.owl"
)
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
    g.parse(repo_schema, format="xml")
    prop_types = {}
    for s in g.subjects(RDF.type, None):
        if s.startswith("https://vocabs.acdh"):
            prop_name = s.split("#")[-1]
            for range_prop in g.objects(s, rdfs_ns.range):
                prop_types[prop_name] = range_prop.split("#")[-1]
    return prop_types


def serialize_project():
    g = Graph()
    sub = URIRef(f"{ARCHE_BASE_URL}")
    proj_sub = URIRef(f"{ARCHE_BASE_URL}/project")
    # HistoGIS Project
    proj_g = Graph()
    proj_g.add((proj_sub, RDF.type, acdh_ns.Project))
    proj_g.add(
        (proj_sub, acdh_ns.hasTitle, Literal("HistoGIS (Project)", lang=ARCHE_LANG))
    )
    proj_g.add(
        (proj_sub, acdh_ns.hasStartDate, Literal("2018-03-01", datatype=XSD.date))
    )
    proj_g.add((proj_sub, acdh_ns.hasEndDate, Literal("2020-11-30", datatype=XSD.date)))
    proj_g.add((proj_sub, acdh_ns.hasFunder, URIRef("https://id.acdh.oeaw.ac.at/oeaw")))
    for x in [adueck, apiechl, pmarck]:
        proj_g.add((proj_sub, acdh_ns.hasContributor, x))
    proj_g.add((proj_sub, acdh_ns.hasPrincipalInvestigator, pandorfer))
    proj_g.add((proj_sub, acdh_ns.hasPrincipalInvestigator, mschloegl))
    proj_g.add((proj_sub, acdh_ns.hasRelatedCollection, sub))
    proj_g.add(
        (proj_sub, acdh_ns.hasDescription, Literal(f"{PROJECT_DESC}", lang=ARCHE_LANG))
    )
    for const in ARCHE_CONST_MAPPINGS:
        arche_prop_domain = get_prop_types().get(const[0], "No Match")
        if arche_prop_domain == "date":
            proj_g.add(
                (proj_sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date))
            )
        if arche_prop_domain == "string":
            proj_g.add(
                (proj_sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG))
            )
        else:
            proj_g.add((proj_sub, acdh_ns[const[0]], URIRef(const[1])))
    # HistoGIS Root Collection
    g.add((sub, RDF.type, acdh_ns.TopCollection))
    g.add(
        (
            sub,
            acdh_ns.hasPid,
            Literal(
                "http://hdl.handle.net/21.11115/0000-000C-E12A-7", datatype=XSD.anyURI
            ),
        )
    )
    g.add((sub, acdh_ns.hasCoverageStartDate, Literal("1512-01-01", datatype=XSD.date)))
    g.add((sub, acdh_ns.hasCoverageEndDate, Literal("1989-12-31", datatype=XSD.date)))
    g.add(
        (
            sub,
            acdh_ns.hasTitle,
            Literal(f"{PROJECT_METADATA['title']}", lang=ARCHE_LANG),
        )
    )
    g.add(
        (
            sub,
            acdh_ns.hasOaiSet,
            URIRef("https://vocabs.acdh.oeaw.ac.at/archeoaisets/kulturpool"),
        )
    )
    g.add((sub, acdh_ns.hasRelatedProject, proj_sub))
    g.add((sub, acdh_ns.hasOwner, URIRef("https://id.acdh.oeaw.ac.at/acdh")))
    g = g + proj_g
    # define persons
    g.add((pandorfer, RDF.type, acdh_ns.Person))
    g.add((pandorfer, acdh_ns.hasTitle, Literal("Peter Andorfer", lang="de")))

    g.add((mschloegl, RDF.type, acdh_ns.Person))
    g.add(
        (
            mschloegl,
            acdh_ns.hasIdentifier,
            URIRef("https://id.acdh.oeaw.ac.at/mschloegl"),
        )
    )
    g.add((mschloegl, acdh_ns.isMemberOf, URIRef("https://id.acdh.oeaw.ac.at/acdh")))
    g.add((mschloegl, acdh_ns.hasTitle, Literal("Matthias Schlögl", lang="und")))
    g.add((mschloegl, acdh_ns.hasFirstName, Literal("Matthias", lang="und")))
    g.add((mschloegl, acdh_ns.hasLastName, Literal("Schlögl", lang="und")))

    g.add((apiechl, RDF.type, acdh_ns.Person))
    g.add(
        (apiechl, acdh_ns.hasIdentifier, URIRef("https://id.acdh.oeaw.ac.at/apiechl"))
    )
    g.add((apiechl, acdh_ns.hasTitle, Literal("Anna Piechl", lang="und")))
    g.add((apiechl, acdh_ns.hasLastName, Literal("Piechl", lang="und")))
    g.add((apiechl, acdh_ns.hasFirstName, Literal("Anna", lang="und")))
    g.add((sub, acdh_ns.hasCreator, apiechl))
    g.add((sub, acdh_ns.hasCurator, pandorfer))

    g.add((adueck, RDF.type, acdh_ns.Person))
    g.add(
        (
            adueck,
            acdh_ns.hasIdentifier,
            URIRef("https://id.acdh.oeaw.ac.at/adueckelmann"),
        )
    )
    g.add((adueck, acdh_ns.hasTitle, Literal("Antonia Dückelmann", lang="und")))
    g.add((adueck, acdh_ns.hasLastName, Literal("Dückelmann", lang="und")))
    g.add((adueck, acdh_ns.hasFirstName, Literal("Antonia", lang="und")))
    g.add((sub, acdh_ns.hasCreator, adueck))

    g.add((URIRef("https://orcid.org/0000-0003-4135-713X"), RDF.type, acdh_ns.Person))
    g.add(
        (
            URIRef("https://orcid.org/0000-0003-4135-713X"),
            acdh_ns.hasIdentifier,
            URIRef("https://id.acdh.oeaw.ac.at/lelmer"),
        )
    )
    g.add(
        (
            URIRef("https://orcid.org/0000-0003-4135-713X"),
            acdh_ns.hasTitle,
            Literal("Laura Elmer", lang="und"),
        )
    )
    g.add(
        (
            URIRef("https://orcid.org/0000-0003-4135-713X"),
            acdh_ns.hasLastName,
            Literal("Elmer", lang="und"),
        )
    )
    g.add(
        (
            URIRef("https://orcid.org/0000-0003-4135-713X"),
            acdh_ns.hasFirstName,
            Literal("Laura", lang="und"),
        )
    )
    g.add(
        (sub, acdh_ns.hasContributor, URIRef("https://orcid.org/0000-0003-4135-713X"))
    )

    g.add((URIRef("https://orcid.org/0000-0003-2271-8948"), RDF.type, acdh_ns.Person))
    g.add(
        (
            URIRef("https://orcid.org/0000-0003-2271-8948"),
            acdh_ns.hasIdentifier,
            URIRef("https://id.acdh.oeaw.ac.at/ldownstepper"),
        )
    )
    g.add(
        (
            URIRef("https://orcid.org/0000-0003-2271-8948"),
            acdh_ns.hasTitle,
            Literal("Liam Downs-Tepper", lang="und"),
        )
    )
    g.add(
        (
            URIRef("https://orcid.org/0000-0003-2271-8948"),
            acdh_ns.hasFirstName,
            Literal("Liam", lang="und"),
        )
    )
    g.add(
        (
            URIRef("https://orcid.org/0000-0003-2271-8948"),
            acdh_ns.hasLastName,
            Literal("Downs-Tepper", lang="und"),
        )
    )
    g.add(
        (sub, acdh_ns.hasContributor, URIRef("https://orcid.org/0000-0003-2271-8948"))
    )

    g.add((pmarck, RDF.type, acdh_ns.Person))
    g.add(
        (
            pmarck,
            acdh_ns.hasTitle,
            Literal("Peter Paul Marckhgott-Sanabria", lang="und"),
        )
    )
    g.add((pmarck, acdh_ns.hasLastName, Literal("Marckhgott-Sanabria", lang="und")))
    g.add((pmarck, acdh_ns.hasFirstName, Literal("Peter Paul", lang="und")))
    g.add((sub, acdh_ns.hasCreator, pmarck))
    g.add((sub, acdh_ns.hasDescription, Literal(f"{TOP_COL_DESC}", lang=ARCHE_LANG)))
    for const in ARCHE_CONST_MAPPINGS_SIMPLE:
        arche_prop_domain = get_prop_types().get(const[0], "No Match")
        if arche_prop_domain == "date":
            g.add((sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
        if arche_prop_domain == "string":
            g.add((sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
        else:
            g.add((sub, acdh_ns[const[0]], URIRef(const[1])))
    return g


def get_arche_id(res, id_prop="pk", arche_uri=ARCHE_BASE_URL):
    """function to generate generic ARCHE-IDs
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
        return "/".join([arche_uri, app_name, class_name, f"{getattr(res, id_prop)}"])


def as_arche_graph(res):
    g = Graph()
    sub = URIRef(f"{ARCHE_BASE_URL}/{res.source.slug_name()}/{res.slug_name()}")
    g.add(
        (
            sub,
            acdh_ns.hasOaiSet,
            URIRef("https://vocabs.acdh.oeaw.ac.at/archeoaisets/kulturpool"),
        )
    )
    g.add((sub, acdh_ns.hasTitle, Literal(f"{res}", lang="und")))
    alt_names = res.alt_name.replace(",", ";")
    for x in alt_names.split(";"):
        if x != "":
            g.add(
                (
                    sub,
                    acdh_ns.hasAlternativeTitle,
                    Literal(f"{x.strip()}", lang=ARCHE_LANG),
                )
            )
    if res.administrative_unit.pref_label is not None or "":
        g.add(
            (
                sub,
                acdh_ns.hasSubject,
                Literal(
                    f"{res.administrative_unit.pref_label}",
                    lang=f"{res.administrative_unit.pref_label_lang[:1]}",
                ),
            )
        )
    quote = res.source.quote
    g.add(
        (
            sub,
            acdh_ns.hasDescription,
            Literal(
                f"{res} in: {quote}",
                lang=ARCHE_LANG,
            ),
        )
    )
    # create place
    pl = Graph()
    sub_pl = URIRef(
        f"{ARCHE_BASE_URL}/{res.source.slug_name()}/{res.slug_name()}/place"
    )
    pl.add((sub_pl, RDF.type, acdh_ns.Place))
    pl.add((sub_pl, acdh_ns.hasTitle, Literal(f"Place for {res}", lang="und")))
    pl.add((sub_pl, acdh_ns.hasWkt, Literal(f"{res.geom.wkt}")))
    g.add((sub, acdh_ns.hasSpatialCoverage, sub_pl))
    g = g + pl
    # if res.wikidata_id:
    #     g.add(
    #         (
    #             sub,
    #             SKOS.broadMatch,
    #             Literal(f"https://www.wikidata.org/entity/{res.wikidata_id}")
    #         )
    #     )
    # g.add(
    #     (
    #         sub, acdh_ns.hasDescription,
    #         Literal(
    #             f"",
    #             lang=ARCHE_LANG
    #         )
    #     )
    # )
    if "Marckhgott" in quote:
        g.add((sub, acdh_ns.hasCreator, pmarck))
    if "Piechl" in quote:
        g.add((sub, acdh_ns.hasCreator, apiechl))
    if "Dückelmann" in quote:
        g.add((sub, acdh_ns.hasCreator, adueck))
    g.add((sub, RDF.type, acdh_ns.Resource))
    g.add(
        (
            sub,
            acdh_ns.hasNonLinkedIdentifier,
            Literal(f"HistoGIS DB-ID {res.id}", lang=ARCHE_LANG),
        )
    )
    g.add(
        (
            sub,
            acdh_ns.hasNonLinkedIdentifier,
            Literal(f"Wikidata ID: {res.wikidata_id}"),
        )
    )
    col = Graph()
    col_sub = URIRef(f"{ARCHE_BASE_URL}/{res.source.slug_name()}")
    g.add((col_sub, RDF.type, acdh_ns.Collection))
    g.add(
        (
            col_sub,
            acdh_ns.hasDescription,
            Literal(res.source.description, lang=ARCHE_LANG),
        )
    )
    col.add((col_sub, acdh_ns.isPartOf, URIRef(f"{ARCHE_BASE_URL}")))
    col.add(
        (
            col_sub,
            acdh_ns.hasOaiSet,
            URIRef("https://vocabs.acdh.oeaw.ac.at/archeoaisets/kulturpool"),
        )
    )
    if res.source.end_date is not None:
        col.add(
            (
                col_sub,
                acdh_ns.hasCoverageEndDate,
                Literal(res.source.end_date, datatype=XSD.date),
            )
        )
    if res.source.start_date is not None:
        col.add(
            (
                col_sub,
                acdh_ns.hasCoverageStartDate,
                Literal(res.source.start_date, datatype=XSD.date),
            )
        )
    col.add((col_sub, acdh_ns.hasTitle, Literal(f"{res.source}", lang=ARCHE_LANG)))
    g.add((sub, acdh_ns.isPartOf, col_sub))
    if res.start_date is not None:
        g.add(
            (
                sub,
                acdh_ns.hasCoverageStartDate,
                Literal(res.start_date, datatype=XSD.date),
            )
        )
    if res.end_date is not None:
        g.add(
            (sub, acdh_ns.hasCoverageEndDate, Literal(res.end_date, datatype=XSD.date))
        )
    g.add(
        (
            sub,
            acdh_ns.hasCategory,
            URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/dataset"),
        )
    )
    for const in ARCHE_CONST_MAPPINGS_SIMPLE:
        arche_prop_domain = get_prop_types().get(const[0], "No Match")
        if arche_prop_domain == "date":
            col.add()
            g.add((sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
            col.add((col_sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
        if arche_prop_domain == "string":
            g.add((sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
            col.add((col_sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
        else:
            g.add((sub, acdh_ns[const[0]], URIRef(const[1])))
            col.add((col_sub, acdh_ns[const[0]], URIRef(const[1])))
    g = g + col
    return g


def title_img():
    g = Graph()
    sub = URIRef(f"{ARCHE_BASE_URL}/histogis_projektlogo_black.png")
    sandra = URIRef("https://id.acdh.oeaw.ac.at/slehecka")
    sandra_g = Graph()
    sandra_g.add((sandra, RDF.type, acdh_ns.Person))
    sandra_g.add((sandra, acdh_ns.hasTitle, Literal("Sandra Lehecka", lang="und")))
    sandra_g.add((sandra, acdh_ns.hasFirstName, Literal("Sandra", lang="und")))
    sandra_g.add(
        (sandra, acdh_ns.isMemberOf, URIRef("https://id.acdh.oeaw.ac.at/acdh"))
    )

    sandra_g.add((sandra, acdh_ns.hasLastName, Literal("Lehecka", lang="und")))
    g.add((sub, RDF.type, acdh_ns.Resource))
    g = g + sandra_g
    g.add((sub, acdh_ns.hasCreator, sandra))
    g.add((sub, acdh_ns.hasTitle, Literal("HistoGIS Title Logo", lang=ARCHE_LANG)))
    g.add((sub, acdh_ns.isPartOf, URIRef(f"{ARCHE_BASE_URL}")))
    g.add(
        (
            sub,
            acdh_ns.hasCategory,
            URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/image"),
        )
    )
    g.add((sub, acdh_ns.isTitleImageOf, URIRef(f"{ARCHE_BASE_URL}")))
    for const in ARCHE_CONST_MAPPINGS_SIMPLE:
        arche_prop_domain = get_prop_types().get(const[0], "No Match")
        if arche_prop_domain == "date":
            g.add((sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
        if arche_prop_domain == "string":
            g.add((sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
        else:
            g.add((sub, acdh_ns[const[0]], URIRef(const[1])))

    return g
