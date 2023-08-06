"""
Small function to perform a conversion between texture name and clay sand fractions.
"""

_tex_name = {  # name: (clay, sand)
    'clay': (65, 17.5),
    'silty clay': (47.5, 7.5),
    'sandy clay': (42.5, 52.5),
    'clay loam': (32.5, 32.5),
    'silty clay loam': (32.5, 10),
    'sandy clay loam': (27.5, 60),
    'loam': (17.5, 42.5),
    'sand': (2.5, 92.5),
    'loamy sand': (5, 82.5),
    'sandy loam': (10, 65),
    'silt loam': (15, 20),
    'silt': (5, 7.5)
}

usda_names = sorted(_tex_name.keys())

# algo to find if point is inside polygon does not work if point exactly on border
th = 1e-4

_tex_poly = {  # name: polygon of [(clay, sand), ...]
    'clay': [(100 + th, 0 - th), (55, 45 + th), (40, 45), (40, 20), (60, 0 - th)],
    'silty clay': [(60, 0 - th), (40, 20), (40, 0 - th)],
    'sandy clay': [(55, 45 + th), (35, 65 + th), (35, 45), (40, 45)],
    'clay loam': [(40, 45), (35, 45), (27.5, 45), (27.5, 22.5), (27.5, 20), (40, 20)],
    'silty clay loam': [(40, 20), (27.5, 20), (27.5, 0 - th), (40, 0 - th)],
    'sandy clay loam': [(35, 65 + th), (20, 80 + th), (20, 52.5), (27.5, 45), (35, 45)],
    'loam': [(27.5, 45), (20, 52.5), (7.5, 52.5), (7.5, 42.5), (27.5, 22.5)],
    'sand': [(0 - th, 100 + th), (0 - th, 85), (10, 90 + th)],
    'loamy sand': [(10, 90 + th), (0 - th, 85), (0 - th, 70), (15, 85 + th)],
    'sandy loam': [(20, 80 + th), (15, 85 + th), (0 - th, 70), (0 - th, 50), (7.5, 42.5), (7.5, 52.5), (20, 52.5)],
    'silt loam': [(27.5, 20), (27.5, 22.5), (7.5, 42.5), (0 - th, 50), (0 - th, 20), (12.5, 7.5), (12.5, 0 - th),
                  (27.5, 0 - th)],
    'silt': [(0 - th, 20), (0 - th, 0 - th), (12.5, 0 - th), (12.5, 7.5)]
}


def _ray_tracing_method(x, y, poly):
    n = len(poly)
    inside = False
    xints = 0.0

    for i in range(n):
        p1x, p1y = poly[i]
        p2x, p2y = poly[(i + 1) % n]

        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside

    return inside


def texture_name(clay, sand):
    """Texture denomination

    References:
        https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/ref/?cid=nrcs142p2_054253

    Args:
        clay (float): [-] clay fraction between 0 and 1
        sand (float): [-] sand fraction between 0 and 1

    Returns:
        (str): 'official' name of texture
    """
    clay *= 100  # stored as %
    sand *= 100  # stored as %

    for name, poly in _tex_poly.items():
        if _ray_tracing_method(clay, sand, poly):
            return name

    raise UserWarning(f"texture not defined for clay '{clay:.2f}' and sand '{sand:.2f}'")


def texture(name):
    """Fraction of clay and sand elements

    References:
        https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/ref/?cid=nrcs142p2_054253

    Args:
        name (str): 'official' name of texture

    Returns:
        (float, float): [-] fraction of clay, sand between 0 and 1
    """
    return (v / 100 for v in _tex_name[name])
