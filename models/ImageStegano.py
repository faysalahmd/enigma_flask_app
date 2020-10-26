import time
from PIL import Image
import binascii
import pdb
import os

'''
    Encoding:
    For each pixel (RGB), the R value is set to EVEN if the bit is 0 and ODD if the bit is 0
    Each pixels B value is set to even color code unless there is no more data, and its set to ODD for loop termination 
    
    Decoding:
    For each pixel's R value being even odd value denotes 0 or 1
    Termination points is pixel's B neing odd number 
'''

class ImageStegano:

    # Flag to identify encoded images
    FLAG = "XX"

    def encode(self, image, string_data, dir):
        string_data = self.FLAG + string_data
        im_basic = Image.open(image)

        im = im_basic.convert('RGB')

        px = im.load()

        # Convert string to binary
        data = bin(int(binascii.hexlify(str.encode(string_data)), 16))

        # Remove '0b' from the binary string.
        data = data[2:]

        width, height = im.size
        if len(data) > width:
            raise Exception("Image dimensions too small for data.")

        for iter, char in enumerate(data):

            r = px[iter, 0][0]
            g = px[iter, 0][1]
            b = px[iter, 0][2]

            # Make last color value even which denotes there is more data.
            if b % 2 != 0:
                if b < 255:
                    b = b + 1
                    px[iter, 0] = (r, g, b)
                else:
                    b = b - 1
                    px[iter, 0] = (r, g, b)

            if char == '0':
                # make even
                if r % 2 != 0:
                    if r < 255:
                        px[iter, 0] = (r+1, g, b)
                    else:
                        px[iter, 0] = (r-1, g, b)

            else:
                # make odd
                if r % 2 == 0:
                    if r < 255:
                        px[iter, 0] = (r+1, g, b)
                    else:
                        px[iter, 0] = (r-1, g, b)


        # Make last value of rgb odd, which denotes end of the data.
        last_pix = len(data) - 1
        r = px[last_pix, 0][0]
        g = px[last_pix, 0][1]
        b = px[last_pix, 0][2]

        if b % 2 == 0:
            if r < 255:
                px[last_pix, 0] = (r, g, b+1)
            else:
                px[last_pix, 0] = (r, g, b-1)
        filename = str(time.time_ns()) + "encoded.png"

        im.save(os.path.join(os.getcwd(), 'static', 'imports', dir, filename))
        return os.path.join('imports', dir, filename)

    def decode(self, image):
        im_basic = Image.open(image)
        im = im_basic.convert('RGB')
        px = im.load()
        list_data = []
        iter = 0
        while True:
            r = px[iter, 0][0]
            b = px[iter, 0][2]

            if b % 2 != 0:
                if r % 2 == 0:
                    list_data.append("0")
                else:
                    list_data.append("1")
                return list_data
            else:
                if r % 2 == 0:
                    list_data.append("0")
                else:
                    list_data.append("1")
            iter += 1

    def checkdata(self, raw_binary):

        # binary_str binary length should be at least 2 bytes if it contains the FLAG
        if len(raw_binary) < 15:
            return False, ''
        else:
            try:

                try:
                    n = int('0b' + raw_binary, 2)
                    parsed_data = str(binascii.unhexlify('%x' % n), 'utf-8')
                except:
                    return False, ''
                print(parsed_data)
                if parsed_data[:2] == self.FLAG:
                    return True, parsed_data.split(self.FLAG)[1]
                else:
                    return False, ''
            except Exception as e:
                print(str(e))
                return False, ''
