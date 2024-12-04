import json
import geopandas as gpd
from django.http import JsonResponse
from shapely.wkt import loads

from shps.filters import TempSpatialListFilter
from shps.models import TempSpatial
from shps.utils import round_coords


def shapes_geojson(request):
    values_list = [
        "id",
        "name",
        "geom",
    ]
    qs = TempSpatialListFilter(request.GET, queryset=TempSpatial.objects.all()).qs
    items = list(qs.values_list(*values_list))
    converted_data = [(id, name, loads(geom.wkt)) for id, name, geom in items]
    gdf = gpd.GeoDataFrame(
        converted_data, columns=["id", "name", "geometry"], crs="EPSG:4326"
    )
    gdf["geometry"] = gdf["geometry"].apply(
        lambda geom: round_coords(geom, precision=2)
    )
    data = json.loads(gdf.to_json())
    data["metadata"] = {
        "number of objects": len(gdf)
    }
    return JsonResponse(data)
