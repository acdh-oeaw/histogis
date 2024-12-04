from shapely.geometry import mapping, shape


def round_coords(geometry, precision=2):
    if geometry.is_empty:
        return geometry
    return shape(
        {
            **mapping(geometry),
            "coordinates": _round_coords_recursive(
                mapping(geometry)["coordinates"], precision
            ),
        }
    )


# Recursive function to handle nested coordinates
def _round_coords_recursive(coords, precision):
    if isinstance(
        coords[0], (list, tuple)
    ):  # Handle nested lists (e.g., multipolygons, polygons)
        return [_round_coords_recursive(c, precision) for c in coords]
    return [round(coord, precision) for coord in coords]
