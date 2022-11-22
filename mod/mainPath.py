from os import path as osp
from sys import path as sysp

up = osp.abspath(osp.join(osp.dirname(__file__), '..'))
if not up in sysp:
    sysp.append(up)