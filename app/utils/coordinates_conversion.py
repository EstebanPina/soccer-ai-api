def conversion(str):
  direction = {'N':1, 'S':-1, 'E': 1, 'W':-1}
  new = str.replace(u'°',' ').replace('″',' ').replace('′',' ')
  new = new.split()
  new_dir = new.pop()
  new.extend([0,0,0])
  if "." in new[0]:
    return new[0]
  return (int(new[0])+int(new[1])/60.0+int(new[2])/3600.0) * direction[new_dir]

def get_converted_lat_lon(str_coord):
  try:
    if str_coord == None:
      return "0","0"
    lat, lon = str_coord.split(' ')
    return str(conversion(lat)), str(conversion(lon))
  except:
    return "0","0"