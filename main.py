from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging
import os, json

import gzip
import azure.functions as func
from azure.storage.blob import ContainerClient
import datetime


def writeToBlob(requestJson,connectionString,containerName):
    file_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
    fileNameStr = "splineOutput"
    filename = fileNameStr + "-" + file_time + ".json"

    containerClinet = ContainerClient.from_connection_string(connectionString,containerName)
    blobClient = containerClinet.get_blob_client(filename)
    blobClient.upload_blob(requestJson)


app = FastAPI()




@app.post("/api/v1/lineage")
def writeLineageToBlob(request: Request):

    connString = "DefaultEndpointsProtocol=https;AccountName=informaticaedc1051test;AccountKey=VSuaTQMdj0+Lw1GHkoXhdFv+ljldYUaAqQ5NaSYEN8bHvifKySNizQ7M447t9wHdS+bBAMyQErIey7KFfFBZXQ==;EndpointSuffix=core.windows.net"
    contName = "openlineage"

    req_body = request.body()
    
    toBlob = writeToBlob(req_body,connString,contName)
    