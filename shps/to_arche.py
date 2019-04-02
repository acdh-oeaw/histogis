import rdflib
from datetime import datetime
from django.conf import settings
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS, ConjunctiveGraph
from rdflib.namespace import DC, FOAF, RDFS, XSD
from rdflib.namespace import SKOS
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from . models import TempSpatial

from webpage.metadata import PROJECT_METADATA

ARCHE = Namespace('https://vocabs.acdh.oeaw.ac.at/schema#')
ACDH = Namespace('https://id.acdh.oeaw.ac.at/')
curent_date = datetime.now().strftime('%Y-%m-%d')


def project_to_arche():
    g = rdflib.Graph()

    # top-collection
    topcol = URIRef('https://id.acdh.oeaw.ac.at/histogis')
    g.add((topcol, RDF.type, ARCHE.Collection))
    g.add((topcol, ARCHE.hasTitle, Literal('HistoGIS Data')))
    g.add((topcol, ARCHE.hasAvailableDate, Literal(curent_date, datatype=XSD.date)))

    # project
    project = URIRef('https://id.acdh.oeaw.ac.at/histogis/project')
    g.add((project, RDF.type, ARCHE.Project))
    g.add((project, ARCHE.hasTitle, Literal('HistoGIS Project')))
    g.add((project, ARCHE.hasDescription, Literal(PROJECT_METADATA['description'])))
    g.add((project, ARCHE.hasStartDate, Literal('2018-04-01', datatype=XSD.date)))
    g.add((project, ARCHE.hasEndDate, Literal('2020-03-31', datatype=XSD.date)))
    g.add((project, ARCHE.language, Literal('eng')))
    g.add((topcol, ARCHE.hasAvailableDate, Literal(curent_date, datatype=XSD.date)))

    # persons
    pandorfer = URIRef("http://d-nb.info/gnd/1043833846")
    g.add((pandorfer, ARCHE.hasFirstName, Literal('Peter')))
    g.add((pandorfer, ARCHE.hasLastName, Literal('Andorfer')))
    g.add((project, ARCHE.hasPrincipalInvestigator, pandorfer))
    g.add((project, ARCHE.hasContact, pandorfer))

    mschloegl = URIRef("http://d-nb.info/gnd/1154715620")
    g.add((mschloegl, ARCHE.hasFirstName, Literal('Matthias')))
    g.add((mschloegl, ARCHE.hasLastName, Literal('Schlögl')))
    g.add((project, ARCHE.hasContact, mschloegl))

    apiechl = URIRef("https://orcid.org/0000-0002-9239-5577")
    g.add((apiechl, ARCHE.hasFirstName, Literal('Piechl')))
    g.add((apiechl, ARCHE.hasLastName, Literal('Anna')))
    g.add((project, ARCHE.hasCreator, apiechl))

    adueck = URIRef("https://orcid.org/non-provided-yet")
    g.add((adueck, ARCHE.hasFirstName, Literal('Dückelmann')))
    g.add((adueck, ARCHE.hasLastName, Literal('Antonia')))
    g.add((project, ARCHE.hasCreator, adueck))

    pmarck = URIRef("https://orcid.org/0000-0003-1816-4823")
    g.add((pmarck, ARCHE.hasFirstName, Literal('Marckghott-Sanabria')))
    g.add((pmarck, ARCHE.hasLastName, Literal('Peter Paul')))
    g.add((project, ARCHE.hasCreator, pmarck))

    # top-collection more
    g.add((project, ARCHE.hasRelatedCollection, topcol))
    g.add((topcol, ARCHE.hasRelatedProject, project))
    g.add((topcol, ARCHE.hasLicense, URIRef("https://creativecommons.org/licenses/by/4.0/")))
    g.add((topcol, ARCHE.hasContact, mschloegl))
    g.add((topcol, ARCHE.hasContact, pandorfer))
    g.add((topcol, ARCHE.hasContributor, pandorfer))
    g.add((topcol, ARCHE.hasContributor, mschloegl))
    g.add((topcol, ARCHE.hasCreator, pmarck))
    g.add((topcol, ARCHE.hasCreator, apiechl))
    g.add((topcol, ARCHE.hasCreator, adueck))
    g.add((topcol, ARCHE.hasDescription, Literal(PROJECT_METADATA['description'])))
    g.add((topcol, ARCHE.hasCoverageStartDate, Literal('1815-01-01', datatype=XSD.date)))
    g.add((topcol, ARCHE.hasCoverageEndDate, Literal('1919-01-01', datatype=XSD.date)))

    # vector-collection
    vecol = URIRef('https://id.acdh.oeaw.ac.at/histogis/vectordata')
    g.add((vecol, RDF.type, ARCHE.Collection))
    g.add((vecol, ARCHE.hasAvailableDate, Literal(curent_date, datatype=XSD.date)))
    g.add((vecol, ARCHE.hasTitle, Literal('HistoGIS Vector Data')))
    g.add((vecol, ARCHE.isPartOf, topcol))
    g.add((vecol, ARCHE.hasLicense, URIRef("https://creativecommons.org/licenses/by/4.0/")))
    g.add((vecol, ARCHE.hasContact, mschloegl))
    g.add((vecol, ARCHE.hasContact, pandorfer))
    g.add((vecol, ARCHE.hasContributor, pandorfer))
    g.add((vecol, ARCHE.hasContributor, mschloegl))
    g.add((vecol, ARCHE.hasCreator, pmarck))
    g.add((vecol, ARCHE.hasCreator, apiechl))
    g.add((vecol, ARCHE.hasCreator, adueck))
    g.add((vecol, ARCHE.hasDescription, Literal("This collections provides vectordata (GeoJson)")))
    g.add((vecol, ARCHE.hasCoverageStartDate, Literal('1815-01-01', datatype=XSD.date)))
    g.add((vecol, ARCHE.hasCoverageEndDate, Literal('1919-01-01', datatype=XSD.date)))

    for x in TempSpatial.objects.all()[:3]:
        res = x.as_arche_res()
        g.add((vecol, ARCHE.hasContributor, pandorfer))
        g.add((vecol, ARCHE.hasContributor, mschloegl))
        g.add((vecol, ARCHE.hasCreator, pmarck))
        g.add((vecol, ARCHE.hasCreator, apiechl))
        g.add((vecol, ARCHE.hasCreator, adueck))
        g = g + x.as_arche_res()

    return g