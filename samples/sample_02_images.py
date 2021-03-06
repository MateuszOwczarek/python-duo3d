﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
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

from duo3d import *
from msvcrt import getch  # Windows only

duo_frame_num = 0

def DUOCallback( pFrameData, pUserData ):
    """
    """
    global duo_frame_num
    frame_data = pFrameData.contents    # get the object to which the pointer points

    print "DUO Frame #%d\n" % ( duo_frame_num )
    print "  Timestamp:          %10.1f ms" % ( frame_data.timeStamp / 10.0 )
    print "  Frame Size:         %dx%d" % ( frame_data.width, frame_data.height )
    print "  Left Frame Buffer:  ", ( frame_data.leftData )    # FIXME: Do it more elegant way
    print "  Right Frame Buffer: ", ( frame_data.rightData )
    print "-" * 50

    duo_frame_num += 1

def main():
    """

    """

    WIDTH = 320
    HEIGHT = 240
    FPS = 30.0

    print "DUOLib Version:       v%s" % GetDUOLibVersion()

    ri = DUOResolutionInfo()

    # Select the resolution and frame rate
    binning = FindOptimalBinning( WIDTH, HEIGHT )
    if EnumerateDUOResolutions( ri, 1, WIDTH, HEIGHT, binning, FPS ):
        duo = DUOInstance()

        # Open DUO
        if OpenDUO( duo ):
            print "DUO Device Name:      '%s'" % GetDUODeviceName( duo )
            print "DUO Serial Number:    %s" % GetDUOSerialNumber( duo )
            print "DUO Firmware Version: v%s" % GetDUOFirmwareVersion( duo )
            print "DUO Firmware Build:   %s" % GetDUOFirmwareBuild( duo )

            print "Hit any key to start capturing"
            getch()

            # Set selected resolution
            SetDUOResolutionInfo( duo, ri )

            # Start capture and pass callback function that will be called on every frame captured
            callback = DUOFrameCallback( DUOCallback )
            if StartDUO( duo, callback, None ):
                # Wait for any key
                getch()
                # Stop capture
                StopDUO( duo )
            else:
                print "Could not start DUO camera"

            # Close DUO
            CloseDUO( duo )
        else:
            print "Could not open DUO camera"

    return 0

if __name__ == '__main__':
    main()
