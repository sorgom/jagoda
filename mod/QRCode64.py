from qrcode import QRCode
from base64 import b64encode
from io import BytesIO

class QRCode64(QRCode):
    def __init__(self, version=3, box_size=6, border=2):
        super().__init__(
            version=version,
            box_size=box_size,
            border=border
        )
        self.prefix = ''

    def setPrefix(self, prefix:str=''):
        self.prefix = prefix

    def ascii(self, data:str):
        self.add_data(data)
        self.make(fit=True)
        img = self.make_image(fill_color='black', back_color='white')
        bios = BytesIO()
        img.save(bios, format='PNG')
        self.clear()
        return b64encode(bios.getvalue()).decode('ascii')

    def html(self, data:str, dataInAlt=False):
        asc = self.ascii(data)
        alt = data if dataInAlt else 'qrcode'
        return f'<img src="data:image/png;base64, {asc}" alt="{alt}"/>'

if __name__ == '__main__':
    print('...')
    q64 = QRCode64()
    input = 'https://sorgo.de/'
    a1 = q64.ascii(input)
    a2 = q64.ascii(input)
    c = 'OK' if a1 == a2 else 'NOK'
    print(c) 

    a1 = q64.html(input)
    a2 = q64.html(input)
    c = 'OK' if a1 == a2 else 'NOK'
    print(c) 

    # print(q64.html(input, True))
    # print(q64.html(input))
    