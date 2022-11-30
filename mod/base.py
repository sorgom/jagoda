import json
from sys import _getframe
from flask import request, render_template, escape    

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

def debug(*args):
    print(f'## {_getframe(1).f_code.co_name}>', *args)

def debugTemplate(template:str, **args):
    debug(template)
    return escape(render_template(template, **args))