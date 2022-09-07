import json
import geodaisy.converters as convert

# đọc layer_name
def get_name(tile_data) :
    z=list(tile_data.keys())
    return (z)

#đọc geometry
def get_geos(tile_data, name) :
    geos=[]
    n=len(tile_data[name]['features'])
    for i in range(n) :
        geo={}
        geo['type']=tile_data[name]['features'][i]['geometry']['type']
        geo['coordinates']=tile_data[name]['features'][i]['geometry']['coordinates']
        geos.append(geo)
    return geos

# đọc properties
def get_full_properties(tile_data, name):
    propertiles=[]
    n=len(tile_data[name]['features'])
    for i in range(n) :
        propertiles.append(tile_data[name]['features'][i]['properties'])
    return propertiles

# tạo layer hợp lệ
def get_class(tile_data, name):
    class_tile={}
    class_tile['name']=name
    class_tile['version'] = 2
    features_list=[]
    g=get_geos(tile_data, name)
    pro=get_full_properties(tile_data,name)
    n=len(g)
    for i in range(n) :
        feature = {}
        g[i]=json.dumps(g[i])
        feature['geometry'] = convert.geojson_to_wkt(g[i])
        feature['properties'] = pro[i]
        feature['id']=tile_data[name]['features'][i]['id']
        features_list.append(feature)
    class_tile['features'] = features_list
    return class_tile

#tạo một vector tile hợp lệ
def get_full_class(tile_data) :
   tile=[]
   name=get_name(tile_data)
   for x in name :
       tile.append(get_class(tile_data,x))
   return tile





