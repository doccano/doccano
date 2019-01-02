
def lightness(rgbstr):
    '''calculate lightness in 8-bit range from an RGB hex string or tuple
    https://en.wikipedia.org/wiki/Relative_luminance
    '''
    if isinstance(rgbstr, str):
        rgbstr = rgbstr.lstrip('#')
        rgb_tuple = bytearray.fromhex(rgbstr)
    elif isinstance(rgbstr, (tuple,list)):
        rgb_tuple = rgbstr
    else:
        raise ValueError
    red, green, blue = map(inverse_gamma_sRGB, rgb_tuple)
    return gamma_sRGB(0.2126 * red + 0.7152 * green + 0.0722 * blue)


def inverse_gamma_sRGB(ic):
    """Inverse of sRGB gamma function. (approx 2.2)"""
    c = ic/255.0
    if ( c <= 0.04045 ):
        return c/12.92
    else:
        return pow(((c+0.055)/(1.055)),2.4)
    

def gamma_sRGB(v):
    """sRGB gamma function (approx 2.2)"""
    if(v<=0.0031308):
        v *= 12.92
    else:
        v = 1.055*pow(v,1.0/2.4)-0.055
    return int(v*255)
