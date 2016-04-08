python-duo3d
=========

About
-----
This package is a (not so perfect) Python binding of [DUO API](https://duo3d.com/docs/articles/api) (DUOLib.)

Install
-------

    $ python setup.py install

*Remember to copy your DUOLib.dll (on Windows) or libDUO.so (on Linux) from the DUOSDK into base folder (where setup.py file is located) of this package prior the installation (it will be copied automatically,) or directly into Lib/site-packages/duo3d-***-py2.7.egg*

Dependencies
-------------

* ctypes
* DUOSDK >= v1.5.0.26

Usage
------
Examples how to use this package are located in the [samples](https://github.com/MateuszOwczarek/python-duo3d/tree/master/samples) directory. Those are more or less samples provided by the DUO, rewritten to Python and tweaked a bit. [DUO API](https://duo3d.com/docs/articles/) reference might be also handy  while preparing your own scripts.

License
--------
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/MateuszOwczarek/python-duo3d/master/LICENSE)

Mateusz Owczarek