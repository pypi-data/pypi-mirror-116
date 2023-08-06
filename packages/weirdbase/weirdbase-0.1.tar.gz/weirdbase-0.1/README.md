# python-weirdbase - Convert weird and arbitrary number bases to and from integers

Want to convert an integer to a string representation of weird number base like base36? We have you covered.

```doctest
>>> import weirdbase
>>> weirdbase.int2base(12345, base=36)
'9IX'
>>> weirdbase.base2int('9IX', 36)
12345
```

By default, it's case-sensitive, so you can also do:

```doctest
>>> weirdbase.base2int('helloThere', 62)
590996557455853334
>>> weirdbase.int2base(590996557455853334, 62)
'helloThere'
```

And you can convert from one weird base to another; say from base 62 to hex:

```doctest
>>> weirdbase.base2base('helloThere', 62, 16)
'833A43CDEA28716'
```

And you can even make up your own set of digits to get weirder:

```doctest
>>> weirdbase.int2base(420, base=10, chars=')!@#$%^&*(')
'$@)'
>>> weirdbase.base2int('$@)', base=10, chars=')!@#$%^&*(')
420

```

## Installing

```bash
pip install pip+https://github.com/darrenpmeyer/python-weirdbase.git
```

