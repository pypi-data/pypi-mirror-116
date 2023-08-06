"""Converts integers to strange number bases using customizable base definitions

"""
__version__ = '0.1'
DEFAULT_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def int2base(an_int, base, chars=None, allow_negative=True):
    # this is the "fountain" we'll get the weird base's digits from
    chars = DEFAULT_CHARS if chars is None else chars

    if type(an_int) != int:
        raise TypeError(f"int2base requires an int, not a {type(an_int)}")

    if base > len(chars):
        raise ValueError(f"Can't have a base ({base}) that exceeds the length of chars ({len(chars)}")

    if an_int < 0 and not allow_negative:
        raise ValueError("Negative numbers not permitted")

    converted = []  # the array that will store the converted value
    num = abs(an_int)  # working copy of the number, always positive

    while num > 0:
        converted.append(chars[int(num % base)])  # add a char at the index num mod base
        num = num // base  # integer division to remove the value that was calculated above

    if an_int < 0:
        converted.append('-')  # add the sign indicator

    converted.reverse()  # algorithm builds the converted value 'backwards', so fix that
    return ''.join(converted)  # return the converted value as a string


def base2int(value, base, chars=None, allow_negative=True):
    # this is the "fountain" we'll get the weird base's digits from
    chars = DEFAULT_CHARS if chars is None else chars
    charmap = {chars[i]: i for i in range(0, len(chars))}  # make dict of {char:position} pairs

    if base > len(chars):
        raise ValueError(f"Can't have a base ({base}) that exceeds the length of chars ({len(chars)}")

    converted = 0  # converted integer
    sign = 1  # 1= positive, -1= negative; multiply int by this to correct sign

    num = list(value)  # working copy of str as list
    num.reverse()  # makes the integer position equal to exponent

    if num[-1] == '-':
        # remember, "leading" char is now at the end due to the above reverse()
        if not allow_negative and '-' not in charmap:
            # this error won't raise if '-' is being used as a digit!
            raise ValueError("Negative values not allowed")
        # NOTE: if you want a leading '-' to be treated as a char, you must
        #       set allow_negative = False; else we assume it means "negative"
        sign = -1 if allow_negative else 1
        num.pop()  # remove the sign, kind of like abs() on an int

    for exp in range(0, len(num)):
        # for each char index, use it as an exponent as well as an index, and...
        try:
            converted += charmap[num[exp]] * (base ** exp)  # value of digit times base to the power of position
        except KeyError as e:
            raise KeyError(f"digit {e} not found in '{chars}'")

    converted *= sign  # multiply by sign to correct negative if needed
    return converted  # return the converted int


def base2base(value, from_base, to_base, chars=None, allow_negative=True):
    intermediate = base2int(str(value), from_base, chars, allow_negative)
    converted = int2base(intermediate, to_base, chars, allow_negative)
    return converted
