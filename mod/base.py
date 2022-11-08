import json
from flask import request

BOTH = ['GET', 'POST']
GET  = ['GET']
POST = ['POST']

ERR_DATA = 'DATA ERROR'
ERR_AUTH = 'NOT AUTHORIZED'

def getJson():
    return json.loads(request.form.get('json'))

def rf(field:str):
    return request.form.get(field, '')

def post():
    return request.method == 'POST'