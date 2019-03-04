import geopandas as gpd
import pickle

def getPolyCoords(row, geom, coord_type, boundaries):
    """Returns the coordinates ('x' or 'y') of edges of a Polygon exterior and checks that it is in boundary"""
    if row[geom]:
        # Parse the exterior of the coordinate
        if row[geom].type == 'Polygon':
            exterior = row[geom].exterior
        elif row[geom].type == 'MultiPolygon':
            exterior = row[geom][0].exterior

        x_range = exterior.coords.xy[0]
        y_range = exterior.coords.xy[1]

        if coord_type == 'x':
            if max(x_range) > boundaries[2] or min(x_range) < boundaries[3]:
                return 0
            else:
                # Return 1 if in range
                return 1
        elif coord_type == 'y':
            if max(y_range) > boundaries[0] or min(y_range) < boundaries[1]:
                return 0
            else:
                # Return 1 if in range
                return 1

state = 'vic'
shp = 'SSC_2016_AUST.shp'

# Defining boundary: http://boundingbox.klokantech.com
if state == 'vic':
    # boundary = [-37.54, -38.27, 145.37, 144.63]
    boundary = [-37.24, -38.71, 146.72, 143.63]
elif state == 'nsw':
    boundary = [-33.663, -34.006, 151.342, 150.785]
elif state == 'sa':
    boundary = [-34.470, -35.056, 139.019, 138.236]
else:
    raise NameError('Boundary Conditions not defined for state ' + state)


out = state + ' filtered.p'

try:
    g_df = pickle.load(open(out, "rb"))
except Exception:
    # Read files
    grid = gpd.read_file(shp)

    # Get the Polygon x and y coordinates
    grid['x'] = grid.apply(getPolyCoords, geom='geometry', coord_type='x', boundaries=boundary, axis=1)
    grid['y'] = grid.apply(getPolyCoords, geom='geometry', coord_type='y', boundaries=boundary, axis=1)

    grid['val'] = grid.x * grid.y
    filtered_df = grid.loc[grid.val == 1]
    pickle.dump(filtered_df, open(out, 'wb'))
    
