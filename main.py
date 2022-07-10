# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 20:44:59 2022

@author: TEVIN
"""
import uvicorn   #####comment when deployed
rom fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from redis_om import get_redis_connection, HashModel

app = FastAPI()
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "IOTuser")
    correct_password = secrets.compare_digest(credentials.password, "iot_user@20220406")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

redis = get_redis_connection(
    host  = "redis-15365.c277.us-east-1-3.ec2.cloud.redislabs.com",
    port=15365,
    password="ruqK6OVaQpYajpp1glVruZYZdTHQfMlq",
    decode_responses=True
)

class SensorData(HashModel):
    device: str
    time: str
    Humidity: int
    Temperature: int
    
    
    class Meta:
        database = redis
   
@app.get('/getsensordata')
async def RetrieveAll(username= Depends(get_current_username)):
    return [format(pk) for pk in SensorData.all_pks()]

def format(pk: str):
    sensordata = SensorData.get(pk)
   
    return{
        'id': sensordata.pk,
        'device': sensordata.device,
        'time': sensordata.time,
        'Humidity': sensordata.Humidity, 
        'Temperature': sensordata.Temperature


    }

@app.post('/postsensordata')
async def PostData(sensordata: SensorData,username= Depends(get_current_username)):
    return sensordata.save()


if __name__ == "__main__":    #####comment when deployed
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)   #####comment when deployed
