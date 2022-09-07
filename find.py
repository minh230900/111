import  gzip
import mapbox_vector_tile
import  json
import pymbtiles
import math


def get_id_tile(lon, lat, z):
    latRad = (lat * math.pi) / 180
    n = 2**z
    xTile = n * ((lon + 180) / 360)
    yTile = 2**z -( n * (1 - (math.log(math.tan(latRad) + 1 / math.cos(latRad)) / math.pi)) / 2)
    out = [xTile, yTile]
    return out

def read(zoom_level,tile_column,tile_row):
    with pymbtiles.MBtiles('vn.mbtiles') as src:
        x = src.read_tile(zoom_level, tile_column, tile_row)
    x = mapbox_vector_tile.decode(gzip.decompress(x))
    return (x)

def find_tile(lon, lat, z):
    x=get_id_tile(lon, lat, z)
    x[0]=int(x[0])
    x[1]=int(x[1])
    return (read(z,x[0],x[1]))

x=find_tile(105, 20, 13)
print(x)
