  # -*- coding: utf-8 -*-

"""@package duo3d

    @brief: 

    @author: Mateusz Owczarek (mateusz.owczarek@dokt.p.lodz.pl)
    @version: 0.1
    @date: April, 2016
    @copyright: 2016 (c) by Lodz University of Technology (http://www.p.lodz.pl/en/)
    
	References:
	[1] http://scipy-cookbook.readthedocs.org/items/Ctypes.html
	[2] http://docs.scipy.org/doc/numpy-1.10.1/user/c-info.python-as-glue.html
	[3] http://stackoverflow.com/questions/5862915/passing-numpy-arrays-to-a-c-function-for-input-and-output
	[4] https://docs.python.org/2/library/ctypes.html#callback-functions
	[5] https://docs.python.org/2/library/ctypes.html#ctypes.create_string_buffer
	[6] http://www.nirsoft.net/utils/dll_export_viewer.html
"""

import os
import ctypes

__all__ = ['CloseDUO', 'DUOFrame', 'DUOFrameCallback', 'DUOIMUSample', 'DUOInstance', 'DUOResolutionInfo',
		'DUO_ACCEL_2G', 'DUO_ACCEL_4G', 'DUO_ACCEL_16G', 'DUO_ACCEL_8G',
		'DUO_BIN_ANY', 'DUO_BIN_HORIZONTAL2', 'DUO_BIN_HORIZONTAL4', 'DUO_BIN_NONE', 'DUO_BIN_VERTICAL2', 'DUO_BIN_VERTICAL4',
		'DUO_GYRO_250', 'DUO_GYRO_500', 'DUO_GYRO_1000', 'DUO_GYRO_2000',
		'EnumerateResolutions', 'GetDUODeviceName', 'GetDUOFirmwareBuild', 'GetDUOFirmwareVersion', 'GetDUOSerialNumber',
		'GetLibVersion', 'OpenDUO', 'SetDUOResolutionInfo', 'StartDUO', 'StopDUO']

_duolib_path = os.path.join( os.path.dirname( __file__ ), "../DUOLib" )
_duolib = ctypes.cdll.LoadLibrary( _duolib_path )

# DUO instance
DUOInstance = ctypes.c_void_p

# DUO binning
DUO_BIN_ANY = -1
DUO_BIN_NONE = 0
DUO_BIN_HORIZONTAL2 = 1  # Horizontal binning by factor of 2
DUO_BIN_HORIZONTAL4 = 2  # Horizontal binning by factor of 4
DUO_BIN_VERTICAL2 = 4  # Vertical binning by factor of 2
DUO_BIN_VERTICAL4 = 8  # Vertical binning by factor of 4

# DUO resolution info
class DUOResolutionInfo( ctypes.Structure ):
	"""
	
	"""
	_fields_ = [
		( "width", ctypes.c_int ),
		( "height", ctypes.c_int ),
		( "binning", ctypes.c_int ),
		( "fps", ctypes.c_float ),
		( "minFps", ctypes.c_float ),
		( "maxFps", ctypes.c_float ),
	 ]
PDUOResolutionInfo = ctypes.POINTER( DUOResolutionInfo )

# DUO IMU data sample
class DUOIMUSample( ctypes.Structure ):
	"""
	
	"""
	_fields_ = [
		( "tempData", ctypes.c_float ),  # DUO temperature data
		( "accelData", ctypes.c_float * 3 ),  # DUO accelerometer data (x,y,z)
		( "gyroData", ctypes.c_float * 3 )  # DUO gyroscope data (x,y,z)
		 ]

DUO_MAX_IMU_SAMPLES = 100

# DUO Frame
class DUOFrame( ctypes.Structure ):
	"""
	DUOFrame structure holds the sensor data that is passed to user via DUOFrameCallback function
	"""
	_fields_ = [
		( "width", ctypes.c_uint32 ),  # DUO frame width
		( "height", ctypes.c_uint32 ),  # DUO frame height
		( "ledSeqTag", ctypes.c_uint8 ),  # DUO frame LED tag
		( "timeStamp", ctypes.c_uint32 ),  # DUO frame time stamp in 100us increments
		( "leftData", ctypes.POINTER( ctypes.c_uint8 ) ),  # DUO left frame data
		( "rightData", ctypes.POINTER( ctypes.c_uint8 ) ),  # DUO right frame data
		( "IMUPresent", ctypes.c_uint8 ),  # True if IMU chip is present ( DUO MLX )
		( "IMUSamples", ctypes.c_uint32 ),  # Number of IMU data samples in this frame
		( "IMUData", DUOIMUSample * DUO_MAX_IMU_SAMPLES )  # DUO IMU data samples
		 ]
PDUOFrame = ctypes.POINTER( DUOFrame )

# DUO Accelerometer Range
DUO_ACCEL_2G = 0  # DUO Accelerometer full scale range +/- 2g
DUO_ACCEL_4G = 1  # DUO Accelerometer full scale range +/- 4g
DUO_ACCEL_8G = 2  # DUO Accelerometer full scale range +/- 8g
DUO_ACCEL_16G = 3  # DUO Accelerometer full scale range +/- 16g

# DUO Gyroscope Range
DUO_GYRO_250 = 0  # DUO Gyroscope full scale range 250 deg/s
DUO_GYRO_500 = 1  # DUO Gyroscope full scale range 500 deg/s
DUO_GYRO_1000 = 2  # DUO Gyroscope full scale range 1000 deg/s
DUO_GYRO_2000 = 3  # DUO Gyroscope full scale range 2000 deg/s

# DUO parameter unit
DUO_PERCENTAGE = 0
DUO_MILLISECONDS = 1
# DUO Camera parameters
DUO_DEVICE_NAME = 2  # Get only: ( string allocated by user min size 252 bytes )
DUO_SERIAL_NUMBER = 3  # Get only: ( string allocated by user min size 252 bytes )
DUO_FIRMWARE_VERSION = 4  # Get only: ( string allocated by user min size 252 bytes )
DUO_FIRMWARE_BUILD = 5  # Get only: ( string allocated by user min size 252 bytes )
DUO_RESOLUTION_INFO = 6  # Set/Get:  ( PDUOResolutionInfo ) - must be first parameter to set
DUO_FRAME_DIMENSION = 7  # Get only: ( uint32_t, uint32_t )
DUO_EXPOSURE = 8  # Set/Get:  ( double [ 0,100 ], DUO_PERCENTAGE ) or ( double in milliseconds, DUO_MILLISECONDS )
DUO_GAIN = 9  # Set/Get:  ( double [ 0,100 ] )
DUO_HFLIP = 10  # Set/Get:  ( bool [ false,true ] )
DUO_VFLIP = 11  # Set/Get:  ( bool [ false,true ] )
DUO_SWAP_CAMERAS = 12  # Set/Get:  ( bool [ false,true ] )
# DUO LED Control Parameters
DUO_LED_PWM = 13  # Set/Get:  ( double [ 0,100 ] )
DUO_LED_PWM_SEQ = 14  # Set only: ( PDUOLEDSeq, int ) - number of LED sequence steps ( max 64 )
# DUO Calibration Parameters
DUO_CALIBRATION_PRESENT = 15  # Get Only: return true if calibration data is present
DUO_FOV = 16  # Get Only: ( PDUOResolutionInfo, double* ( leftHFOV, leftVFOV, rightHFOV, rightVFOV )
DUO_UNDISTORT = 17  # Set/Get:  ( bool [ false,true ] )
DUO_INRINSICS = 18  # Get Only: ( pointer to DUO_INTR structure )
DUO_EXTRINSICS = 19  # Get Only: ( pointer to DUO_EXTR structure )
DUO_STEREO_PARAMETERS = 20  # Get Only: ( pointer to DUO_STEREO structure )
# DUO IMU Parameters
DUO_IMU_RANGE = 21  # Set/Get: ( DUOAccelRange, DUOGyroRange )

_duolib.GetLibVersion.argtypes = None
_duolib.GetLibVersion.restype = ctypes.c_char_p
def GetLibVersion():
	"""

	"""
	return _duolib.GetLibVersion()

# DUO resolution enumeration
# To enumerate resolution settings for specific resolution, set width and height and optionally fps.
# To enumerate all supported resolutions set width, height and fps all to -1.
# NOTE: There are large number of resolution setting supported.
_duolib.EnumerateResolutions.argtypes = [ ctypes.POINTER( DUOResolutionInfo ), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_float ]
_duolib.EnumerateResolutions.restype = ctypes.c_int
def EnumerateResolutions( resList, resListSize, width = -1, height = -1, binning = DUO_BIN_ANY, fps = -1.0 ):
	"""
	Enumerates supported resolutions.
	@param resList: 
	@param resListSize: 
	@param width: 
	@param height: 
	@param binning: 
	@param fps: 
	@return: number of resolutions found
	"""
	return _duolib.EnumerateResolutions( ctypes.byref( resList ), resListSize, width, height, binning, fps )

# DUO device initialization
_duolib.OpenDUO.argtypes = [ ctypes.POINTER( DUOInstance ) ]
_duolib.OpenDUO.restype = ctypes.c_bool
def OpenDUO( duo ):
	"""
	Opens the DUO device and initialized the passed DUOInstance handle pointer.
	@param duo: DUOInstance handle pointer
	@return: True on success
	"""
	return _duolib.OpenDUO( ctypes.byref( duo ) )

_duolib.CloseDUO.argtypes = [ DUOInstance ]
_duolib.CloseDUO.restype = ctypes.c_bool
def CloseDUO( duo ):
	"""
	Closes the DUO device.
	@param duo: DUOInstance handle pointer
	@return: True on success
	"""
	return _duolib.CloseDUO( duo )

# DUO frame callback function
# NOTE: This function is called in the context of the DUO capture thread.
# 		 To prevent any dropped frames, this function must return as soon as possible.
DUOFrameCallback = ctypes.CFUNCTYPE( PDUOFrame, ctypes.c_void_p )  # [4]

# DUO device capture control
_duolib.StartDUO.argtypes = [ DUOInstance, DUOFrameCallback, ctypes.c_void_p, ctypes.c_bool ]
_duolib.StartDUO.restype = ctypes.c_bool
def StartDUO( duo, frameCallback, pUserData, masterMode = True ):
	"""
	Starts capturing frames.
	@param duo: DUOInstance handle pointer
	@param frameCallback: pointer to user defined DUOFrameCallback callback function
	@param pUserData: any user data that needs to be passed to the callback function
	@param masterMode: 
	@return: True on success
	"""
	callback = DUOFrameCallback( frameCallback )
	return _duolib.StartDUO( duo, callback, pUserData, masterMode )

_duolib.StopDUO.argtypes = [ DUOInstance ]
_duolib.StopDUO.restype = ctypes.c_bool
def StopDUO( duo ):
	"""
	Stops capturing frames.
	@param duo: DUOInstance handle pointer
	@return: True on success
	"""
	return _duolib.StopDUO( duo )

# DUO Camera parameters control
# Do not call these functions directly
# Use below defined macros
__DUOParamGet__ = _duolib[0x7]  # ! Due to underscores, functions cannot be imported by name
__DUOParamSet__ = _duolib[0x8]  # ... instead ordinals were used (use [6] to view ordinals)
__DUOParamSet__.restype = ctypes.c_bool
__DUOParamGet__.restype = ctypes.c_bool

def SetDUOResolutionInfo( duo, val ):
	"""
	Sets the desired resolution, binning and the frame rate
	@return: True on success
	"""
	return __DUOParamSet__( duo, DUO_RESOLUTION_INFO, ctypes.byref( val ) )

def SetDUOIMURange( duo, accel, gyro ):
	"""
	Sets the IMU DUOAccelRange and DUOGyroRange range.
	@return: True on success
	"""
	return __DUOParamSet__( duo, DUO_IMU_RANGE, ctypes.c_int( accel ), ctypes.c_int( gyro ) )

def GetDUODeviceName( duo ):
	"""
	
	"""
	val = ctypes.create_string_buffer( 260 )  # [5]
	__DUOParamGet__( duo, DUO_DEVICE_NAME, val )
	return val.value

def GetDUOSerialNumber( duo ):
	"""
	
	"""
	val = ctypes.create_string_buffer( 260 )  # [5]
	__DUOParamGet__( duo, DUO_SERIAL_NUMBER, val )
	return val.value

def GetDUOFirmwareVersion( duo ):
	"""
	
	"""
	val = ctypes.create_string_buffer( 260 )  # [5]
	__DUOParamGet__( duo, DUO_FIRMWARE_VERSION, val )
	return val.value

def GetDUOFirmwareBuild( duo ):
	"""
	
	"""
	val = ctypes.create_string_buffer( 260 )  # [5]
	__DUOParamGet__( duo, DUO_FIRMWARE_BUILD, val )
	return val.value
