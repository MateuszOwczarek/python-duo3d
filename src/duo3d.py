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

import os
import ctypes as ct

__all__ = [
    "CloseDUO", "EnumerateDUOResolutions", "FindOptimalBinning",
    "GetDUOCalibrationPresent", "GetDUOCameraSwap", "GetDUODeviceName",
    "GetDUOExposure", "GetDUOExposureMS", "GetDUOExtrinsics", "GetDUOFOV",
    "GetDUOFirmwareBuild", "GetDUOFirmwareVersion", "GetDUOFrameDimension",
    "GetDUOGain", "GetDUOHFlip", "GetDUOIMURange", "GetDUOIntrinsics",
    "GetDUOLedPWM", "GetDUOSerialNumber", "GetDUOStereoParameters",
    "GetDUOUndistort", "GetDUOVFlip", "GetDUOLibVersion", "OpenDUO",
    "SetDUOCameraSwap", "SetDUOExposure", "SetDUOExposureMS", "SetDUOGain",
    "SetDUOHFlip", "SetDUOIMURange", "SetDUOLedPWM", "SetDUOLedPWMSeq",
    "SetDUOResolutionInfo", "SetDUOUndistort", "SetDUOVFlip", "StartDUO",
    "StopDUO",

    "DUOFrame", "DUOFrameCallback", "DUOIMUSample", "DUOInstance",
    "DUOLEDSeq", "DUOResolutionInfo", "PDUOFrame", "PDUOLEDSeq",
    "PDUOResolutionInfo",

    "DUO_ACCEL_16G", "DUO_ACCEL_2G", "DUO_ACCEL_4G", "DUO_ACCEL_8G",
    "DUO_BIN_ANY", "DUO_BIN_HORIZONTAL2", "DUO_BIN_HORIZONTAL4",
    "DUO_BIN_NONE", "DUO_BIN_VERTICAL2", "DUO_BIN_VERTICAL4",
    "DUO_CALIBRATION_PRESENT", "DUO_DEVICE_NAME", "DUO_EXPOSURE",
    "DUO_EXTR", "DUO_EXTRINSICS", "DUO_FIRMWARE_BUILD",
    "DUO_FIRMWARE_VERSION", "DUO_FOV", "DUO_FRAME_DIMENSION", "DUO_GAIN",
    "DUO_GYRO_1000", "DUO_GYRO_2000", "DUO_GYRO_250", "DUO_GYRO_500",
    "DUO_HFLIP", "DUO_IMU_RANGE", "DUO_INRINSICS", "DUO_INTR",
    "DUO_LED_PWM", "DUO_LED_PWM_SEQ", "DUO_MAX_IMU_SAMPLES",
    "DUO_MILLISECONDS", "DUO_PERCENTAGE", "DUO_RESOLUTION_INFO",
    "DUO_SERIAL_NUMBER", "DUO_STEREO", "DUO_STEREO_PARAMETERS",
    "DUO_SWAP_CAMERAS", "DUO_UNDISTORT", "DUO_VFLIP",
    ]

# Load shared library
if os.sys.platform.startswith( "win" ):
    _duolib_filename = "DUOLib.dll"
elif os.sys.platform.startswith( "linux" ):
    _duolib_filename = "libDUO.so"
elif os.sys.platform.startswith( "darwin" ):
    _duolib_filename = "libDUO.dylib"
_duolib_filepath = os.path.abspath(os.path.join( os.path.dirname( __file__ ),
                                                "..",
                                                _duolib_filename ) )

if not os.path.isfile( _duolib_filepath ):
    _duolib_dir = os.path.dirname( _duolib_filepath )
    error_str = "You need to copy '%s' from DUOSDK into %s to make this package work"
    raise ImportError( error_str % ( _duolib_filename, _duolib_dir ) )

_duolib = ct.cdll.LoadLibrary( _duolib_filepath )

# DUO instance
DUOInstance = ct.c_void_p

# DUO binning
DUO_BIN_ANY = -1
DUO_BIN_NONE = 0
DUO_BIN_HORIZONTAL2 = 1  # Horizontal binning by factor of 2
DUO_BIN_HORIZONTAL4 = 2  # Horizontal binning by factor of 4
DUO_BIN_VERTICAL2 = 4  # Vertical binning by factor of 2
DUO_BIN_VERTICAL4 = 8  # Vertical binning by factor of 4

class DUOResolutionInfo( ct.Structure ):
    """
    DUO resolution info
    """
    _fields_ = [
        ( "width", ct.c_int ),
        ( "height", ct.c_int ),
        ( "binning", ct.c_int ),
        ( "fps", ct.c_float ),
        ( "minFps", ct.c_float ),
        ( "maxFps", ct.c_float ),
        ]

PDUOResolutionInfo = ct.POINTER( DUOResolutionInfo )

class DUOIMUSample( ct.Structure ):
    """
    DUO IMU data sample
    """
    _fields_ = [
        ( "tempData", ct.c_float ),  # DUO temperature data
        ( "accelData", ct.c_float * 3 ),  # DUO accelerometer data (x,y,z)
        ( "gyroData", ct.c_float * 3 )  # DUO gyroscope data (x,y,z)
        ]

DUO_MAX_IMU_SAMPLES = 100

class DUOFrame( ct.Structure ):
    """
    DUOFrame structure holds the sensor data
    that is passed to user via DUOFrameCallback function
    """
    _fields_ = [
        ( "width", ct.c_uint32 ),  # DUO frame width
        ( "height", ct.c_uint32 ),  # DUO frame height
        ( "ledSeqTag", ct.c_uint8 ),  # DUO frame LED tag
        ( "timeStamp", ct.c_uint32 ),  # DUO frame time stamp in 100us increments
        ( "leftData", ct.POINTER( ct.c_uint8 ) ),  # DUO left frame data
        ( "rightData", ct.POINTER( ct.c_uint8 ) ),  # DUO right frame data
        ( "IMUPresent", ct.c_uint8 ),  # True if IMU chip is present ( DUO MLX )
        ( "IMUSamples", ct.c_uint32 ),  # Number of IMU data samples in this frame
        ( "IMUData", DUOIMUSample * DUO_MAX_IMU_SAMPLES )  # DUO IMU data samples
        ]

PDUOFrame = ct.POINTER( DUOFrame )

class DUOLEDSeq( ct.Structure ):
    """
    DUO LED PWM
    """
    _fields_ = [
        ( "ledPwmValue", ct.c_uint8 * 4 )  # LED PWM values are in percentage [0,100]
        ]

PDUOLEDSeq = ct.POINTER( DUOLEDSeq )

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

class DUO_INTR( ct.Structure ):
    """

    """

    class INTR( ct.Structure ):
        _pack_ = 1
        _fields_ = [
            ( "k1", ct.c_double ),  # Camera radial distortion coefficients
            ( "k2", ct.c_double ),
            ( "k3", ct.c_double ),
            ( "k4", ct.c_double ),  # Camera radial distortion coefficients
            ( "k5", ct.c_double ),
            ( "k6", ct.c_double ),
            ( "p1", ct.c_double ),  # Camera tangential distortion coefficients
            ( "p2", ct.c_double ),
            ( "fx", ct.c_double ),  # Camera focal lengths in pixel units
            ( "fy", ct.c_double ),
            ( "cx", ct.c_double ),  # Camera principal point
            ( "cy", ct.c_double ),
            ]

    _pack_ = 1
    _fields_ = [
        ( "width", ct.c_uint32 ),
        ( "height", ct.c_uint32 ),
        ( "left", INTR ),
        ( "right", INTR ),
        ]

class DUO_EXTR( ct.Structure ):
    """

    """
    _pack_ = 1
    _fields_ = [
        ( "rotation", ct.c_double * 9 ),
        ( "translation", ct.c_double * 3 )
        ]

class DUO_STEREO( ct.Structure ):
    """

    """
    _pack_ = 1
    _fields_ = [
        ( "M1", ct.c_double * 9 ),  # 3x3 - Camera matrices
        ( "M2", ct.c_double * 9 ),
        ( "D1", ct.c_double * 8 ),  # 1x8 - Camera distortion parameters
        ( "D2", ct.c_double * 8 ),
        ( "R", ct.c_double * 9 ),  # 3x3 - Rotation between left and right camera
        ( "T", ct.c_double * 3 ),  # 3x1 - Translation vector between left and right camera
        ( "R1", ct.c_double * 9 ),  # 3x3 - Rectified rotation matrices
        ( "R2", ct.c_double * 9 ),
        ( "P1", ct.c_double * 12 ),  # 3x4 - Rectified projection matrices
        ( "P2", ct.c_double * 12 ),
        ( "Q", ct.c_double * 16 )  # 4x4 - Disparity to depth mapping matrix
        ]

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

_duolib.GetDUOLibVersion.argtypes = None
_duolib.GetDUOLibVersion.restype = ct.c_char_p

def GetDUOLibVersion():
    """

    """
    return _duolib.GetDUOLibVersion()

# DUO resolution enumeration
_duolib.EnumerateDUOResolutions.argtypes = [
    PDUOResolutionInfo,
    ct.c_int32,
    ct.c_int32,
    ct.c_int32,
    ct.c_int32,
    ct.c_float
    ]
_duolib.EnumerateDUOResolutions.restype = ct.c_int

def EnumerateDUOResolutions( resList, resListSize, width = -1, height = -1,
                          binning = DUO_BIN_ANY, fps = -1.0 ):
    """
    Enumerates supported resolutions.
    To enumerate resolution settings for specific resolution,
    set width and height and optionally fps.
    To enumerate all supported resolutions set width, height and fps all to -1.

    @note: There are large number of resolution setting supported.
    @param resList:
    @param resListSize:
    @param width:
    @param height:
    @param binning:
    @param fps:
    @return: number of resolutions found
    """
    return _duolib.EnumerateDUOResolutions( ct.byref( resList ),
                                         resListSize,
                                         width,
                                         height,
                                         binning,
                                         fps )

def FindOptimalBinning( width, height ):
    """
    Finds optimal binning.
    This maximizes sensor imaging area for given resolution.

    @note: Not a part of DUO API, just a helper function
    @param width: width of the frame
    @param height: height of the frame
    @return: optimal binning parameters for given (width, height)
    """
    binning = DUO_BIN_NONE
    if width <= 752 / 2:
        binning += DUO_BIN_HORIZONTAL2
    if height <= 480 / 4:
        binning += DUO_BIN_VERTICAL4
    elif height <= 480 / 2:
        binning += DUO_BIN_VERTICAL2

    return binning

# DUO device initialization
_duolib.OpenDUO.argtypes = [ ct.POINTER( DUOInstance ) ]
_duolib.OpenDUO.restype = ct.c_bool

def OpenDUO( duo ):
    """
    Opens the DUO device and initialized the passed DUOInstance handle pointer.

    @param duo: DUOInstance handle pointer
    @return: True on success
    """
    return _duolib.OpenDUO( ct.byref( duo ) )

_duolib.CloseDUO.argtypes = [ DUOInstance ]
_duolib.CloseDUO.restype = ct.c_bool

def CloseDUO( duo ):
    """
    Closes the DUO device.

    @param duo: DUOInstance handle pointer
    @return: True on success
    """
    return _duolib.CloseDUO( duo )

# DUO frame callback function
# NOTE: This function is called in the context of the DUO capture thread.
#          To prevent any dropped frames, this function must return as soon as possible.
DUOFrameCallback = ct.CFUNCTYPE( None, PDUOFrame, ct.c_void_p )

# DUO device capture control
_duolib.StartDUO.argtypes = [ DUOInstance,
                             DUOFrameCallback,
                             ct.c_void_p,
                             ct.c_bool ]
_duolib.StartDUO.restype = ct.c_bool

def StartDUO( duo, frameCallback = None, pUserData = None, masterMode = True ):
    """
    Starts capturing frames.

    @param duo: DUOInstance handle pointer
    @param frameCallback: pointer to user defined DUOFrameCallback callback function
    @param pUserData: any user data that needs to be passed to the callback function
    @param masterMode:
    @return: True on success
    """
    callback = ( frameCallback if frameCallback is not None else DUOFrameCallback() )
    return _duolib.StartDUO( duo, callback, pUserData, masterMode )

_duolib.StopDUO.argtypes = [ DUOInstance ]
_duolib.StopDUO.restype = ct.c_bool

def StopDUO( duo ):
    """
    Stops capturing frames.

    @param duo: DUOInstance handle pointer
    @return: True on success
    """
    return _duolib.StopDUO( duo )

# DUO Camera parameters control
_duolib.ParamSet.restype = ct.c_bool
_duolib.ParamGet.restype = ct.c_bool

# Get DUO parameters
def GetDUODeviceName( duo ):
    """

    """
    val = ct.create_string_buffer( 260 )
    _duolib.ParamGet( duo, DUO_DEVICE_NAME, val )
    return val.value

def GetDUOSerialNumber( duo ):
    """

    """
    val = ct.create_string_buffer( 260 )
    _duolib.ParamGet( duo, DUO_SERIAL_NUMBER, val )
    return val.value

def GetDUOFirmwareVersion( duo ):
    """

    """
    val = ct.create_string_buffer( 260 )
    _duolib.ParamGet( duo, DUO_FIRMWARE_VERSION, val )
    return val.value

def GetDUOFirmwareBuild( duo ):
    """

    """
    val = ct.create_string_buffer( 260 )
    _duolib.ParamGet( duo, DUO_FIRMWARE_BUILD, val )
    return val.value

def GetDUOFrameDimension( duo ):
    """

    @return: tuple(width, height)
    """
    w = ct.c_uint32()
    h = ct.c_uint32()
    _duolib.ParamGet( duo, DUO_FRAME_DIMENSION, ct.byref( w ), ct.byref( h ) )
    return ( w.value, h.value )

def GetDUOExposure( duo ):
    """

    """
    val = ct.c_double()
    _duolib.ParamGet( duo, DUO_EXPOSURE, ct.byref( val ), DUO_PERCENTAGE )
    return val.value

def GetDUOExposureMS( duo ):
    """

    """
    val = ct.c_double()
    _duolib.ParamGet( duo, DUO_EXPOSURE, ct.byref( val ), DUO_MILLISECONDS )
    return val.value

def GetDUOGain( duo ):
    """

    """
    val = ct.c_double()
    _duolib.ParamGet( duo, DUO_GAIN, ct.byref( val ) )
    return val.value

def GetDUOHFlip( duo ):
    """

    """
    val = ct.c_int()
    _duolib.ParamGet( duo, DUO_HFLIP, ct.byref( val ) )
    return val.value

def GetDUOVFlip( duo ):
    """

    """
    val = ct.c_int()
    _duolib.ParamGet( duo, DUO_VFLIP, ct.byref( val ) )
    return val.value

def GetDUOCameraSwap( duo ):
    """

    """
    val = ct.c_int()
    _duolib.ParamGet( duo, DUO_SWAP_CAMERAS, ct.byref( val ) )
    return val.value

def GetDUOLedPWM( duo ):
    """

    """
    val = ct.c_double()
    _duolib.ParamGet( duo, DUO_LED_PWM, ct.byref( val ) )
    return val.value

def GetDUOCalibrationPresent( duo ):
    """

    """
    return _duolib.ParamGet( duo, DUO_CALIBRATION_PRESENT )

def GetDUOFOV( duo, ri ):
    """

    """
    # FIXME: Type check
    val = ct.c_double()
    _duolib.ParamGet( duo, DUO_FOV, ct.byref( ri ), ct.byref( val ) )  # FIXME: is byref( ri ) necessary?
    return val.value

def GetDUOUndistort( duo ):
    """

    """
    val = ct.c_int()
    _duolib.ParamGet( duo, DUO_UNDISTORT, ct.byref( val ) )
    return val.value

def GetDUOIntrinsics( duo, val ):
    """

    """
    # FIXME: Type check
    return _duolib.ParamGet( duo, DUO_INRINSICS, ct.byref( val ) )

def GetDUOExtrinsics( duo, val ):
    """

    """
    return _duolib.ParamGet( duo, DUO_EXTRINSICS, ct.byref( val ) )

def GetDUOStereoParameters( duo, val ):
    """

    """
    # FIXME: Type check
    return _duolib.ParamGet( duo, DUO_STEREO_PARAMETERS, ct.byref( val ) )

def GetDUOIMURange( duo ):
    """
    @return: tuple(accel, gyro)
    """
    accel = ct.c_int()
    gyro = ct.c_int()
    _duolib.ParamGet( duo, DUO_IMU_RANGE, ct.byref( accel ), ct.byref( gyro ) )
    return ( accel.value, gyro.value )

# Set DUO parameters
def SetDUOResolutionInfo( duo, val ):
    """
    Sets the desired resolution, binning and the frame rate
    @return: True on success
    """
    return _duolib.ParamSet( duo, DUO_RESOLUTION_INFO, ct.byref( val ) )

def SetDUOExposure( duo, val ):
    """

    @return: True on success
    """
    return _duolib.ParamSet( duo, DUO_EXPOSURE, ct.c_double( val ), DUO_PERCENTAGE )

def SetDUOExposureMS( duo, val ):
    """

    @return: True on success
    """
    return _duolib.ParamSet( duo, DUO_EXPOSURE, ct.c_double( val ), DUO_MILLISECONDS )

def SetDUOGain( duo, val ):
    """

    @return: True on success
    """
    return _duolib.ParamSet( duo, DUO_GAIN, ct.c_double( val ) )

def SetDUOHFlip( duo, val ):
    """

    @return: True on success
    """
    return _duolib.ParamSet( duo, DUO_HFLIP, ct.c_int( val ) )

def SetDUOVFlip( duo, val ):
    """

    @return: True on success
    """
    return _duolib.ParamSet( duo, DUO_VFLIP, ct.c_int( val ) )

def SetDUOCameraSwap( duo, val ):
    """

    @return: True on success
    """
    return _duolib.ParamSet( duo, DUO_SWAP_CAMERAS, ct.c_int( val ) )

def SetDUOLedPWM( duo, val ):
    """

    @return: True on success
    """
    return _duolib.ParamSet( duo, DUO_LED_PWM, ct.c_double( val ) )

def SetDUOLedPWMSeq( duo, val, size ):
    """
    @param val: DUOLEDSeq array
    @return: True on success
    """
    return _duolib.ParamSet( duo, DUO_LED_PWM_SEQ, ct.byref( val ), ct.c_uint32( size ) )

def SetDUOUndistort( duo, val ):
    """

    @return: True on success
    """
    return _duolib.ParamSet( duo, DUO_UNDISTORT, ct.c_int( val ) )

def SetDUOIMURange( duo, accel, gyro ):
    """
    Sets the IMU DUOAccelRange and DUOGyroRange range.
    @return: True on success
    """
    return _duolib.ParamSet( duo, DUO_IMU_RANGE, ct.c_int( accel ), ct.c_int( gyro ) )
