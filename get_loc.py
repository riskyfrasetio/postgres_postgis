import psycopg2 as pg
import pandas as pd
#import os
#from subprocess import Popen, PIPE
import flask
from flask import request, jsonify, Response
import numpy
#import re

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/geotargeting', methods=['GET'])
def api_filter():
	conn=pg.connect(host="ec2-54-80-184-43.compute-1.amazonaws.com",database="d4bkoe4dm09aui", user="qgavnbqrmljnqn", password="ffb43fefa1b21a800addeff21cfca93ca661ae9d1c31924250b25fc75c43f693")
	cursor=conn.cursor()
	query_parameters = request.args
	df= query_parameters.get('data_frame')
	#df='dki_kecamatan'
	#data_frame=str(data_frame)
	long = query_parameters.get('long')
	lat = query_parameters.get('lat')
	com= "select b.srid,b.proj4text from srid_table a left join spatial_ref_sys b on b.srid=cast(a.srid as int) where a.name_table='"+df+"'"
	quer=pd.read_sql_query(com,conn)
	srid=quer['srid'].to_numpy().tolist()
	sr=str(srid[0])
	type=quer['proj4text'].to_numpy().tolist()
	if 'utm' in type[0][:15]: 
		command="select * from public." + df + " WHERE ST_CONTAINS(ST_Transform(geom,4326),ST_GeomFromText('POINT("+long +" "+ lat+")',4326))"
		dat=pd.read_sql_query(command,conn)
		dat=dat.drop(['geom'],axis=1)
		return Response(dat.to_json(orient="records"), mimetype='application/json')
	elif 'longlat' in type[0][:15]:
		command="select * from public." + df + " WHERE ST_CONTAINS(geom,ST_GeomFromText('POINT("+long +" "+ lat+")',"+sr+"))"
		dat=pd.read_sql_query(command,conn)
		dat=dat.drop(['geom'],axis=1)
		return Response(dat.to_json(orient="records"), mimetype='application/json')
	cursor.close()
	conn.close()
	#else return Response("not supported".to_json(orient="records"), mimetype='application/json')
app.run()


