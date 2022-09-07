import  gzip
import math
import mapbox_vector_tile
import transform_tiles
import pymbtiles

#đọc một tile dạng bit và chuyển về dict trong python
def read(zoom_level,tile_column,tile_row):
    with pymbtiles.MBtiles('vn.mbtiles') as src:
        x = src.read_tile(zoom_level, tile_column, tile_row)
    x = mapbox_vector_tile.decode(gzip.decompress(x))
    return (x)

#ghi một tile vào csdl
def write(zoom_level,tile_column,tile_row, tile):
    t=transform_tiles.get_full_class(tile)
    z = mapbox_vector_tile.encode(t)
    z = gzip.compress(z)
    with pymbtiles.MBtiles('vn1.mbtiles', mode='r+') as out:
        out.write_tile(zoom_level, tile_column, tile_row,z)


#tạo một tọa độ nguyên
def get_coordinates(tile_column, tile_row, bound_x, bound_y):
    x=round((tile_column % 1 )*4095) + bound_x*4095
    y=round(((tile_row )%1 )*4095) + bound_y*4095
    out=[x,y]
    return out

#tìm tile của một điểm trên một mức zoom
def get_id_tile(lon, lat, z):
    latRad = (lat * math.pi) / 180
    n = 2**z
    xTile = n * ((lon + 180) / 360)
    yTile = 2**z -( n * (1 - (math.log(math.tan(latRad) + 1 / math.cos(latRad)) / math.pi)) / 2)
    out = [xTile, yTile]
    return out

#tìm tile của danh sách các điểm trên một mức zoom
def find_tile(lon_lat, zoom):
    a=[]
    for x in lon_lat :
        a.append(get_id_tile(x[0], x[1], zoom))
    return a

# tìm tất cả tile của danh sách các điểm
def get_full_tile(lon_lat):
    x=[]
    a=[]
    for i in range(15):
       for lo_la in lon_lat:
           x.append(find_tile(lo_la, i))
       a.append(x)
       x=[]
    return a

#lấy dữ liệu từ file input
def read_input():
    f = open("input.txt", "r")
    x = []
    for i in f:
        x.append(i)
    return x

# lấy dữ liệu từ file input2
def read_input2():
    f2 = open("input2.txt", "r")
    x = []
    for i in f2:
        x.append(i)
    return x

#đọc coor dạng kinh độ, vĩ độ
def read_coordinate_lon_lat(x):
    a=x.rsplit(", ")
    n=len(a)
    for i in range(n):
        coor=a[i].rsplit(" ")
        a[i]=[float(coor[0]), float(coor[1])]
    return a

#tạo các tọa độ nguyên
def get_coor_tile(x):
    coor=[]
    a=[]
    for i in x:
        for j in i:
            a.append(get_coordinates(j[0],j[1],0,0))
        coor.append(a)
        a=[]
    return coor

# đọc id_feature
def get_id_featutes(x):
    a=x.rsplit(" ")
    x=[]
    for i in a:
        x.append(int(i))
    return x

#thay đổi hình học
def change_coor_map(z,tile_id, coor, layer_name, id):
    if(id==-1) :
        return 0
    tile_data=read(z,tile_id[0], tile_id[1])
    count=0
    for i in tile_data[layer_name]['features']:
        if i["id"]==id:
            if i['geometry']['type']=='Point':
                tile_data[layer_name]['features'][count]['geometry']['coordinates'] = coor[0][0]
            elif i['geometry']['type']=='Multi Point':
                tile_data[layer_name]['features'][count]['geometry']['coordinates'] = coor[0]
            elif i['geometry']['type']=='LineString':
                tile_data[layer_name]['features'][count]['geometry']['coordinates'] = coor[0]
            else:
                tile_data[layer_name]['features'][count]['geometry']['coordinates']=coor
            write(z, tile_id[0], tile_id[1],tile_data)
            return 1
        count=count+1
    return 0

#thay đổi thuộc tính
def change_pro_map(z,tile_id, layer_name, id, key, value):
    if(id==-1) :
        return 0
    tile_data=read(z,tile_id[0], tile_id[1])
    count=0
    for i in tile_data[layer_name]['features']:
        if i["id"]==id:
            tile_data[layer_name]['features'][count]['properties'][key]=value
            write(z, tile_id[0], tile_id[1],tile_data)
            return 1
        count=count+1
    return 0

# thay đổi hình học
data=read_input()
n=len(data)
for i in range(n):
    data[i]=data[i].replace('\n','')
n=len(data)
coordinates_lon_lat=[]
coordinate_tile=[]
for i in range(2,n):
    coordinates_lon_lat.append(read_coordinate_lon_lat(data[i]))
id_feature=get_id_featutes(data[1])
x=get_full_tile(coordinates_lon_lat)
for i in range(15):
    y = get_coor_tile(x[i])
    xTile=int(x[i][0][0][0])
    yTile=int(x[i][0][0][1])
    tileId = [xTile, yTile]
    layer_name = data[0]
    change_coor_map(i, tileId, y, layer_name, id_feature[i])

# thay đổi thuộc tính
# đọc dữ liệu đầu vào
data = read_input2()
n=len(data)
for i in range(n):
    data[i]=data[i].replace('\n','')
id_feature = data[1].rsplit(" ")
n=len(id_feature)
for i in range(n):
    id_feature[i]=int(id_feature[i])
lon_lat=data[2].rsplit(" ")
lon_lat[0]=int(lon_lat[0])
lon_lat[1]=int(lon_lat[1])
tile_id=[]
for i in range(15):
    tile_id.append(get_id_tile(lon_lat[0], lon_lat[1], i))
    tile_id[i][0]=int(tile_id[i][0])
    tile_id[i][1]=int(tile_id[i][1])
data[1]=data[1].rsplit(" ")
n=len(data[1])
for i in range(n):
    data[1][i]=int(data[1][i])
n=len(data)
for i in  range(3,n):
    data[i]=data[i].rsplit("-")
for i in range(15):
    for j in range(3,n):
       change_pro_map(i,tile_id[i],data[0],data[1][i],data[j][0],data[j][1])






