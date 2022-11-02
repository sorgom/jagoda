from os import path as osp
from sys import path as sysp

up = osp.abspath(osp.join(osp.dirname(__file__), '..'))
if not up in sysp:
    sysp.append(up)

from mod.saveImg import allImgMini

def fakeIdsWithMinis(offset=1000):
    return [[n + offset, img] for n, img in enumerate(allImgMini())] 


if __name__ == '__main__':
    print(fakeIdsWithMinis())
