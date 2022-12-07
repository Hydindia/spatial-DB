#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 19:10:01 2022

@author: shyam
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, sessionmaker
import pandas as pd
from fastapi import Depends, FastAPI
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import text
import sys
import requests
import json
import numpy as np
import random
from shapely.geometry import Polygon, Point
import typing
import psycopg2
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import json
from cmath import pi
from math import radians, cos, sin, sqrt, degrees, asin, atan2, acos
import numpy
import math
import time
from math import sin, cos, sqrt, atan2
import geopy.distance
import psycopg2
import pandas as pds
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import geopy.distance
from scipy import spatial

alchemyEngine   = create_engine('postgresql://postgres:Gangster30@127.0.0.1/Datamodel', pool_recycle=3600);


# Connect to PostgreSQL server

dbConnection    = alchemyEngine.connect();
conn_string = "host='localhost' dbname='Datamodel' user='postgres' password='Gangster30'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()


def Request_team_id():
    get_teamID_url= f"http://missilecommand.live:8080/START/2"
    teamID = requests.get(get_teamID_url)
    if teamID.status_code == 200:
        teamID_info=(json.loads(teamID.content.decode('utf-8')))
    return(teamID_info)


def Request_registeruser():
    get_regions=f"http://missilecommand.live:8080/REGISTER"
    register = requests.get(get_regions)
    if register.status_code == 200:
        register_info=(json.loads(register.content.decode('utf-8')))
    else:
        register_info='No data found'            
    return(register_info)



def Request_radar():
    get_radarsweep=f"http://missilecommand.live:8080/RADAR_SWEEP"
    radar = requests.get(get_radarsweep)
    if radar.status_code == 200:
        radar_info=(json.loads(radar.content.decode('utf-8')))
    else:
        radar_info="No data found"
    return(radar_info)



def Request_time():
    get_clock=f"http://missilecommand.live:8080/GET_CLOCK"
    current_time = requests.get(get_clock)
    if current_time.status_code == 200:
        current_time=(json.loads(current_time.content.decode('utf-8')))
    return(current_time)


def dict_get(x,key,here=None):
    x = x
    if here is None: here = []
    if x.get(key):  
        here.append(x.get(key))
        x.pop(key)
    else:
        for i,j in x.items():
          if  isinstance(x[i],list): dict_get(x[i][0],key,here)
          if  isinstance(x[i],dict): dict_get(x[i],key,here)
    return here


def nextLocation(lon: float, lat: float, speed: float, bearing: float, time:int=1, geojson: int=0):
    if not geojson:
        select = "st_x(p2) as x,st_y(p2) as y"
    else:
        select = "ST_AsGeoJSON(p2)"

    sql = f"""
    WITH 
        Q1 AS (
            SELECT ST_SetSRID(ST_Project('POINT({lon} {lat})'::geometry, {speed*time}, radians({bearing}))::geometry,4326) as p2
        )
 
    SELECT {select}
    FROM Q1
    """
    return cur.execute(sql)

#conn_string = "host='localhost' dbname='Datamodel' user='postgres' password='Gangster30'"
#conn = psycopg2.connect(conn_string)
missiles=pd.read_sql_query('select * from \"missile_properties\"',con=alchemyEngine)
# missile_speed  = pds.read_sql("select * from missile_speed", conn)
# missile_blast  = pds.read_sql("select * from missile_blast", conn)
# missile  = pds.read_sql("select * from missile", conn)
# missile_properties=pd.concat([missile_blast,missile_speed],axis=1)
# missile_properties = missile_properties.loc[:,~missile_properties.columns.duplicated()].copy()
# missiles = pd.merge(missile_properties,missile, how='left',left_on=['category'],right_on=['speedCat']).dropna().reset_index()
# missiles.drop(['index', 'category_x'],axis=1,inplace=True)
# missiles.columns=['blast_radius', 'ms', 'mph', 'category', 'name', 'speedCat','blastCat']
#missile_properties  = pds.read_sql("select * from missile_properties", conn)
# from sqlalchemy import create_engine
# engine = create_engine('postgresql://postgres:Gangster30@localhost:5432/Datamodel')
# missiles.to_sql('missile_properties', engine)
def parse_radar():
    radar_response=Request_radar()
    coordinates=[]
    bearings=[]
    altitudes=[]
    missile=[]
    time=[]
    if len(radar_response)>1:
        radar_response=dict_get(radar_response,'features')[0]
        for i in range(0,len(radar_response)):
            print(i)
            coord=dict_get(radar_response[i],'geometry')[0]['coordinates']
            print(radar_response[i])
            properties=dict_get(radar_response[i],'properties')[0]
            bearing=properties['bearing']
            alti=properties['altitude']
            missile_type=properties['missile_type']
            current_time=properties['current_time']        
            coordinates.append(coord)
            bearings.append(bearing)
            altitudes.append(alti)
            missile.append(missile_type)
            time.append(current_time)
        lis=[coordinates,bearings,altitudes,missile,time]
    else:
        lis='no data found'
    return(lis)   

from math import sqrt
def min_distance(x, y, iterable):
       list_of_distances = list(map(lambda t: sqrt(pow(t[0]-x,2)+pow(t[1]-y,2)),iterable))
       min_res = min(list_of_distances)
       index_of_min = list_of_distances.index(min_res)
       return iterable[index_of_min]
   

radar_info=parse_radar()
import itertools
def get_batteries_positions(radar_info):
        missile_positions=[]
        Region_response=Request_registeruser()
        if len(radar_info)>1 and len(Region_response)>1:
            Multipolygon_regions=dict_get(Region_response,'region')[0]
            poly_set=Multipolygon_regions['features'][0]['geometry']['coordinates']
            len_incomingmissiles=len(radar_info[0])
            missile_pos=random.sample(poly_set,len_incomingmissiles)
            for i in range(0,len(missile_pos)):
                try:
                    a = min_distance(missile_pos[i][0],missile_pos[i][1],radar_info[0])
                except:
                    a="none"
                positions=random.sample(missile_pos[i][0], 1)[0]
                missile_positions.append(positions)
        else:
            missile_positions='no data found'
        return(missile_positions)        


def get_bearing(lat1, long1, lat2, long2):
    dLon = (long2 - long1)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    brng = numpy.arctan2(x,y)
    brng = numpy.degrees(brng)
    return brng

if len(radar_info)>1:
    missile_positions=get_batteries_positions(radar_info)
else:
    missile_positions='no missiles found'
    
from geopy import distance
def get_distance(missile_positions,radar_info):
    distances=[]
    bearings=[]
    if len(missile_positions)>1 and len(radar_info)>1:
        missiles['coordinates']=pd.Series(missile_positions[:11])
        for j in range(0,len(radar_info[0])):
            coords_1 = (missile_positions[j][1], missile_positions[j][0])
            coords_2 = (radar_info[0][j][1], radar_info[0][j][0])
            dist=(distance.distance(coords_1, coords_2).miles)
            distances.append(dist)
            start_bearing=get_bearing(list(coords_1)[1],list(coords_1)[0], list(coords_2)[1],list(coords_2)[0])
#            inetrs=intersection_pt(list(coords_1)[1],list(coords_1)[0],start_bearing,list(coords_2)[1],list(coords_2)[0],radar_info[1][i])
#            intersections.append(inetrs)
            bearings.append(start_bearing)
        missiles["distance"]=pd.Series(distances)
        missiles['fire_time']=missiles["distance"]/missiles["mph"]
#     missiles['target_lat/lon']  =pd.Series(intersections)
    else:
        distances='no distances found'
        missiles='no missiles found'
        bearings='no bearings found'
    return(distances,missiles,bearings)


import math
def future_pt(lat,lon,bearing,distance):
    R = 6378.1 #Radius of the Earth
    brng = bearing #Bearing is 90 degrees converted to radians.
    conversion_factor = 0.62137119
    d = distance/conversion_factor #Distance in km
    lat1 = math.radians(lat) #Current lat point converted to radians
    lon1 = math.radians(lon) #Current long point converted to radians
    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
    math.cos(lat1)*math.sin(d/R)*math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
    math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return(lat2,lon2)

from geopy import distance


# with open('/Users/shyam/Downloads/Registeruser.json', 'r') as f:
#   data = json.load(f)
  
  
# missile_positions=data

import datetime as dt

def expected_response():
    future_point=[]
    expected_time_out=[]
    fired_time=[]
    target_missile=[]
    missile_type=[]
    aim_lat_lon=[]
    target_alt=[]    
    for times in range(10):
        #print(times)
        start = time.time()
        time.sleep(times)
        current_radar=parse_radar()
        if len(current_radar)>1:
            incoming_missiles=current_radar[0]
            type_missile=current_radar[3]
            crtime=current_radar[4]
            bearing=current_radar[1]
            altitude=current_radar[2] 
            time.sleep(10)
            current_radar1=parse_radar()
            altitude1=current_radar1[2] 
            crtime1=current_radar1[4]
            for i in range(0,len(incoming_missiles)-1):
            #print(i)
                speed=missiles[missiles['name']==type_missile[i]]['mph']
                distanced=speed*1
                future_coord=future_pt(incoming_missiles[i][1],incoming_missiles[i][0],bearing[i],distanced)
                future_point.append(future_coord)
                distance_gen=(distance.distance([missile_positions[i][1],missile_positions[i][0]], future_coord).miles)
                expected_time=distanced/(speed*speed)
                fired=str((datetime.strptime(crtime[i], "%H:%M:%S")+timedelta(seconds=10)).time())
                expect_time=[str((datetime.strptime(crtime[i], "%H:%M:%S")+timedelta(hours=int(expected_time))).time())]
                expected_time_out.extend(expect_time)
                fired_time.append(fired)
                target_missile.append(incoming_missiles[i])
                missile_type.append(type_missile[i])
                aim_lat_lon.append(future_point)
                avg_time_diff=sum([abs((datetime.strptime(crtime[i], "%H:%M:%S")-datetime.strptime(crtime1[i], "%H:%M:%S")).total_seconds()) ])/len(crtime)
                avg_altitude_diff=sum([abs(altitude[i]-altitude1[i])])/len(altitude)
                drop_rate=avg_altitude_diff/avg_time_diff
                altitude_drop_perhr=drop_rate*10*6*60
                target_alt.append(altitude_drop_perhr)
                all_data=[future_point,expected_time_out,fired_time,target_missile,missile_type,aim_lat_lon,target_alt]
                
        else:
            all_data='No solution found'
        return(all_data)

final_output= expected_response()




