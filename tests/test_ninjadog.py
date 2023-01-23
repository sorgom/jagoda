from ninjadog import render as render_dog
from sys import argv

def render_template(file:str, **args):
    print('rendering...')
    html = render_dog(file=file, context=args, pretty=True, with_jinja=True)
    print('done.')
    return html

if __name__ == '__main__':
    data = [
        [ 123, 'wumpel', 5 ],
        [ 124, 'rumpel', 2 ]
    ]
    html = render_template('templates/_obj_whats.jade', data=data)
    print(html)
