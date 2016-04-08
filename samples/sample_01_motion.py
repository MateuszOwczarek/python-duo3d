  #!/usr/bin/env python
# -*- coding: utf-8 -*-

from duo3d import *
from msvcrt import getch	# Windows only

def DUOCallback( pFrameData, pUserData ):
	"""
	"""
	print "DUO Frame Timestamp: %10.1f ms" % ( pFrameData.timeStamp / 10.0 )

	if pFrameData.IMUPresent:
		for i in range( 0, pFrameData.IMUSamples ):
			print " Sample #%d" % ( i + 1 )

			print "  Accelerometer: [%8.5f, %8.5f, %8.5f]" % ( pFrameData.IMUData[i].accelData[0],
															pFrameData.IMUData[i].accelData[1],
															pFrameData.IMUData[i].accelData[2] )

			print "  Gyro: [%8.5f, %8.5f, %8.5f]" % ( pFrameData.IMUData[i].gyroData[0],
													pFrameData.IMUData[i].gyroData[1],
													pFrameData.IMUData[i].gyroData[2] )

			print "  Temperature:   %8.6f C" % ( pFrameData.IMUData[i].tempData )

	print "------------------------------------------------------"

def main():
	"""

	"""

	print "DUOLib Version:       v%s" % GetLibVersion()

	ri = DUOResolutionInfo()

	# Select 320x240 resolution with 2x2 binning capturing at 30FPS
	if EnumerateResolutions( ri, 1, 320, 240, DUO_BIN_HORIZONTAL2 + DUO_BIN_VERTICAL2, 30.0 ):
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
