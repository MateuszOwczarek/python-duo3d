#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""@package duo3d

    @brief:

    @author: Mateusz Owczarek (mateusz.owczarek@dokt.p.lodz.pl)
    @version: 0.2
    @date: April, 2016
    @copyright: 2016 (c) Mateusz Owczarek

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    This work was supported by the European Union's
    Horizon 2020 Research and Innovation Programme
    under grant agreement No 643636 "Sound of Vision."
"""

from distutils.sysconfig import get_python_lib
from setuptools import setup

def readme():
   with open( 'README.md' ) as f:
      return f.read()

def getDataFiles():
   import sys
   if sys.platform.startswith( "win" ):
      return [( get_python_lib(), [ "DUOLib.dll" ] )]
   elif sys.platform.startswith( "linux" ):
      return [( get_python_lib(), [ "libDUO.so" ] )]
   elif sys.platform.startswith( "dawrin" ):
      return [( get_python_lib(), [ "libDUO.dylib" ] )]
   else:
      return None

setup( name = 'duo3d',
   version = '0.2',
   description = 'DUOSDK python bindings',
   long_description = readme(),
   classifiers = [
	   'Development Status :: 3 - Alpha',
	   'License :: OSI Approved :: MIT License',
	   'Programming Language :: Python :: 2.7',
	   ],
   keywords = 'duo3d, imu',
   url = 'https://github.com/MateuszOwczarek/python-duo3d',
   author = 'Mateusz Owczarek',
   author_email = 'mateusz.owczarek@dokt.p.lodz.pl',
   license = 'MIT',
   packages = ['duo3d'],
   package_dir = {'duo3d': 'src'},
   data_files = getDataFiles(),
   include_package_data = True,
   zip_safe = False
 )
