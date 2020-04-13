this is python flask app practice example for exploring spatial data using postgreSQL with postgis. The flask app is deployed in heroku dev server. 

Example request:

Lat=-6.178891

Long=106.812230

data=dki_kecamatan

https://shrouded-ocean-86248.herokuapp.com/geotargeting?long=106.812230&lat=-6.178891&data_frame=dki_kecamatan

we will get a json distric name at that point. 

{"gid":9,"kecamatan":"GAMBIR"}
