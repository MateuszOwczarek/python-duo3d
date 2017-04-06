#!/usr/bin/env python
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

def DUOCallback( pFrameData, pUserData ):
    """
    """
    frame_data = pFrameData.contents  # get the object to which the pointer points

    print "DUO Frame Timestamp: %10.1f ms" % ( frame_data.timeStamp / 10.0 )

    if pFrameData.contents.IMUPresent:
        for i in range( 0, pFrameData.contents.IMUSamples ):
            print " Sample #%d" % ( i + 1 )

            # One way to access array data ...
            print "  Accelerometer: [%8.5f, %8.5f, %8.5f]" % ( frame_data.IMUData[i].accelData[0],
                                                            frame_data.IMUData[i].accelData[1],
                                                            frame_data.IMUData[i].accelData[2] )

            # ... and another one
            print "  Gyro: [%8.5f, %8.5f, %8.5f]" % ( tuple( frame_data.IMUData[i].gyroData ) )

            print "  Temperature:   %8.6f C" % ( frame_data.IMUData[i].tempData )

    print "-" * 50

def main():
    """

    """

    WIDTH = 320
    HEIGHT = 240
    FPS = 30.0

    print "DUOLib Version:       v%s" % GetLibVersion()

    ri = DUOResolutionInfo()

    # Select the resolution and frame rate
    binning = FindOptimalBinning( WIDTH, HEIGHT )
    if EnumerateResolutions( ri, 1, WIDTH, HEIGHT, binning, FPS ):
        duo = DUOInstance()

        # Open DUO
        if OpenDUO( duo ):
            print "DUO Device Name:      '%s'" % GetDUODeviceName( duo )
            print "DUO Serial Number:    %s" % GetDUOSerialNumber( duo )
            print "DUO Firmware Version: v%s" % GetDUOFirmwareVersion( duo )
            print "DUO Firmware Build:   %s" % GetDUOFirmwareBuild( duo )

            print "Hit any key to start capturing"
#             getch()

            # Set selected resolution
            SetDUOResolutionInfo( duo, ri )

            # Set IMU range
            SetDUOIMURange( duo, DUO_ACCEL_2G, DUO_GYRO_250 )

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
