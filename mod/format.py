
from mod.base import debug
import re

rxDotZero = re.compile(r'\.0+\b')

def formatDims(dims:list):
    val = rxDotZero.sub('', ' x '.join(map(str, [dim for dim in dims if dim != 0.0])))
    return val
