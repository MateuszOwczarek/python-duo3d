  #!/usr/bin/env python
# -*- coding: utf-8 -*-

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
