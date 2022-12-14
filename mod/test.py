from flask import render_template


def capPre(pre:str, cpc:str):
    return pre + cpc

def test():
    return render_template('test.jade', cap=lambda c : capPre('wumpel: ', c))    

