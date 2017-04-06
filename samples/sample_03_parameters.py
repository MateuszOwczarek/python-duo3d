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

            # Set selected resolution
            SetDUOResolutionInfo( duo, ri )

            led_pwm = 30
            # Set the LED brightness value in %
            SetDUOLedPWM( duo, led_pwm )

            # Start capture (no callback function)
            if StartDUO( duo, None, None ):
                print "Use '+' to increase the brightness of the LEDs"
                print "Use '-' to decrease the brightness of the LEDs"
                print "Use '<Esc>' to exit the program\n"

                ch = 0
                while True:
                    ch = getch()

                    if ch == ord( '-' ):
                        led_pwm = ( led_pwm - 1 if led_pwm > 0 else 0 )
                    elif ch == ord( '+' ):
                        led_pwm = ( led_pwm + 1 if led_pwm < 100 else 100 )

                    print "LED: %3d%%" % led_pwm
                    SetDUOLedPWM( duo, led_pwm )

                    if ch == 27:
                        break;

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
