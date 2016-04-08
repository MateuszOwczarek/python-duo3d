python-duo3d
=========

About
-----
This package is a (not so perfect) Python binding of [DUO API](https://duo3d.com/docs/articles/api) (DUOLib.)

Install
-------

    $ python setup.py install

*Remember to copy your DUOLib.dll (on Windows,) libDUO.so (on Linux) or libDUO.dylib (on Mac OSX) from the DUOSDK into base folder (where setup.py file is located) of this package prior the installation (it will be copied automatically,) or directly into Lib/site-packages/duo3d-***-py2.7.egg*

Dependencies
-------------

* ctypes
* DUOSDK >= v1.5.0.26 (get it from [duo3d.com/downloads/](http://duo3d.com/downloads/))

Usage
------
Examples how to use this package are located in the [samples](https://github.com/MateuszOwczarek/python-duo3d/tree/master/samples) directory. Those are more or less samples provided by the DUO, rewritten to Python and tweaked a bit. [DUO API](https://duo3d.com/docs/articles/) reference might be also handy  while preparing your own scripts.

License
--------
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/MateuszOwczarek/python-duo3d/master/LICENSE)

Mateusz Owczarek