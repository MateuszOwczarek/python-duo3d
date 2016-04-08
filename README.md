python-duo3d
=========

About
-----
This package is a Python binding of [DUO API](https://duo3d.com/docs/articles/api).

Install
-------

    $ python setup.py install

*Remember to copy DUOLib.dll (Windows) or libDUO.so (Linux) from the DUOSDK into base folder of this package (where setup.py file is located) prior the installation (it will be copied automatically) or directly into Lib/site-packages/duo3d-***-py2.7.egg*

Dependencies
-------------

* ctypes
* DUOSDK >= 1.5.0.26

Usage
------
Examples how to use this package are located in the [samples](https://github.com/MateuszOwczarek/python-duo3d/tree/master/samples) directory. Those are more or less samples provided by the DUO, rewritten to Python.

License
--------
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/MateuszOwczarek/python-duo3d/master/LICENSE)

Mateusz Owczarek