# this files contains basic metadata about the project. This data will be used
# (by default) in the base.html and index.html

PROJECT_METADATA = {
    'title': 'HistoGIS',
    'author': 'Peter Andorfer, Matthias Schlögl',
    'subtitle': 'A Geographical Information System, workbench and repository to retrieve,\
    collect, create, enrich and preserve historical temporalized spatial data sets',
    'description': """
    Information about historical political/administrative units is usually communicated through\
    maps. Our human perception allows us to extract diverse information by just looking at a map;\
    we can, for instance, at a glance identify border lines, streets and cities and answer\
    questions such as: 'Was city A part of country B in the year C or which countries shared a\
    border line between Year D and E'.
    A machine on the contrary is hardly capable of doing something similar.\
    The starting point to make a map machine readable is to have it digitized and georeferenced in\
    form of a so called raster image (geotiff), which is usually the standard outcome of projects\
    such as the 'Woldan goes digital Project' or 'Mapire'. To capture any further information\
    transported in historical (political) maps, those raster images need to be vectorized,\
    i.e. transformed into so called vector- or shapefiles, which can spatially describe points,\
    lines, and polygons, thus making it possible to represent border lines, rivers, or the location\
    and outline of cities.
    This is where 'HistoGIS' starts: HistoGIS is a platform to collect, create, curate and share\
    temporalized shapefiles and thereby make implicit information stored in maps explicit and\
    machine readable.
    HistoGIS wants to collect existing data, enrich it and give it back to the community.\
    But HistoGIS also wants to invite researchers from various disciplines in the humanities and\
    social sciences to embed HistoGIS into their research projects and workflow, be it as an\
    analytical tool, be it as an enrichment service, be it as a workbench for data creation\
    and curation or be it as a publishing platform and stable repository for data,\
    crafted in their own projects.
    """,
    'github': 'https://github.com/acdh-oeaw/histogis',
    'purpose_de': 'Ziel von HistoGIS ist die Publikation von Forschungsdaten.',
    'purpose_en': 'The purpose of HistoGIS is the publication of research data.',
    'version': '0.0.1',
    'matomo_id': 'provide some',
    'matomo_url': '//piwik.apollo.arz.oeaw.ac.at/'
}
