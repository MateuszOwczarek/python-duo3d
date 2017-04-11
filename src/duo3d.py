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
    "GetDUOFirmwareBuild", "GetDUOFirmwareVersion", "GetDUOResolutionInfo",
    "GetDUOFrameDimension", "GetDUOGain", "GetDUOHFlip", "GetDUOIMURange",
    "GetDUOIntrinsics", "GetDUOLedPWM", "GetDUOSerialNumber",
    "GetDUOStereoParameters", "GetDUOUndistort", "GetDUOVFlip",
    "GetDUOLibVersion", "OpenDUO", "SetDUOCameraSwap", "SetDUOExposure",
    "SetDUOExposureMS", "SetDUOGain", "SetDUOHFlip", "SetDUOIMURange",
    "SetDUOIMURate", "SetDUOLedPWM", "SetDUOLedPWMSeq", "SetDUOResolutionInfo",
    "SetDUOUndistort", "SetDUOVFlip", "StartDUO", "StopDUO",

    "DUOFrame", "DUOFrameCallback", "DUOIMUSample", "DUOInstance",
    "DUOLEDSeq", "DUOResolutionInfo", "PDUOFrame", "PDUOLEDSeq",
    "PDUOResolutionInfo",

    "DUO_ACCEL_16G", "DUO_ACCEL_2G", "DUO_ACCEL_4G", "DUO_ACCEL_8G",
    "DUO_BIN_ANY", "DUO_BIN_HORIZONTAL2", "DUO_BIN_HORIZONTAL4",
    "DUO_BIN_NONE", "DUO_BIN_VERTICAL2", "DUO_BIN_VERTICAL4",
    "DUO_GYRO_1000", "DUO_GYRO_2000", "DUO_GYRO_250", "DUO_GYRO_500",
    ]

# Load shared library
if os.sys.platform.startswith( "win" ):
    _duolib_filename = "DUOLib.dll"
elif os.sys.platform.startswith( "linux" ):
    _duolib_filename = "libDUO.so"
elif os.sys.platform.startswith( "darwin" ):
    _duolib_filename = "libDUO.dylib"
_duolib_filepath = os.path.abspath( os.path.join( os.path.dirname( __file__ ),
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
        ( "timeStamp", ct.c_uint32 ),  # DUO IMU time stamp in 100us increments
        ( "tempData", ct.c_float ),  # DUO temperature data in degrees Centigrade
        ( "accelData", ct.c_float * 3 ),  # DUO accelerometer data (x,y,z) in g units
        ( "gyroData", ct.c_float * 3 )  # DUO gyroscope data (x,y,z) id degrees/s
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
        ( "width", ct.c_uint16 ),
        ( "height", ct.c_uint16 ),
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

# Get DUO parameters
_duolib.GetDUODeviceName.argtypes = [ DUOInstance,
                                     ct.c_char_p ]
_duolib.GetDUODeviceName.restype = ct.c_bool

def GetDUODeviceName( duo ):
    """
    Returns DUO device name
    """
    val = ct.create_string_buffer( 260 )
    _duolib.GetDUODeviceName( duo, val )
    return val.value

_duolib.GetDUOSerialNumber.argtypes = [ DUOInstance,
                                       ct.c_char_p ]
_duolib.GetDUOSerialNumber.restype = ct.c_bool

def GetDUOSerialNumber( duo ):
    """
    Returns DUO serial number
    """
    val = ct.create_string_buffer( 260 )
    _duolib.GetDUOSerialNumber( duo, val )
    return val.value

_duolib.GetDUOFirmwareVersion.argtypes = [ DUOInstance,
                                          ct.c_char_p ]
_duolib.GetDUOFirmwareVersion.restype = ct.c_bool

def GetDUOFirmwareVersion( duo ):
    """
    Returns DUO firmware version
    """
    val = ct.create_string_buffer( 260 )
    _duolib.GetDUOFirmwareVersion( duo, val )
    return val.value

_duolib.GetDUOFirmwareBuild.argtypes = [ DUOInstance,
                                        ct.c_char_p ]
_duolib.GetDUOFirmwareBuild.restype = ct.c_bool

def GetDUOFirmwareBuild( duo ):
    """
    Returns DUO firmware build information
    """
    val = ct.create_string_buffer( 260 )
    _duolib.GetDUOFirmwareBuild( duo, val )
    return val.value

_duolib.GetDUOResolutionInfo.argtypes = [ DUOInstance,
                                         PDUOResolutionInfo ]
_duolib.GetDUOResolutionInfo.restype = ct.c_bool

def GetDUOResolutionInfo( duo ):
    """

    """
    res_info = DUOResolutionInfo()
    _duolib.GetDUOResolutionInfo( duo, ct.byref( res_info ) )
    return res_info

_duolib.GetDUOFrameDimension.argtypes = [ DUOInstance,
                                         ct.POINTER( ct.c_uint32 ),
                                         ct.POINTER( ct.c_uint32 ) ]
_duolib.GetDUOFrameDimension.restype = ct.c_bool

def GetDUOFrameDimension( duo ):
    """
    Returns DUO frame width and height
    @return: tuple(width, height)
    """
    w = ct.c_uint32()
    h = ct.c_uint32()
    _duolib.GetDUOFrameDimension( duo, ct.byref( w ), ct.byref( h ) )
    return ( w.value, h.value )

_duolib.GetDUOExposure.argtypes = [ DUOInstance,
                                   ct.POINTER( ct.c_double ) ]
_duolib.GetDUOExposure.restype = ct.c_bool

def GetDUOExposure( duo ):
    """
    Returns DUO exposure value in percentage [0,100]
    """
    val = ct.c_double()
    _duolib.GetDUOExposure( duo, ct.byref( val ) )
    return val.value

_duolib.GetDUOExposureMS.argtypes = [ DUOInstance,
                                     ct.POINTER( ct.c_double ) ]
_duolib.GetDUOExposureMS.restype = ct.c_bool

def GetDUOExposureMS( duo ):
    """
    Returns DUO exposure value in milliseconds
    """
    val = ct.c_double()
    _duolib.GetDUOExposureMS( duo, ct.byref( val ) )
    return val.value

_duolib.GetDUOAutoExposure.argtypes = [ DUOInstance,
                                       ct.POINTER( ct.c_bool ) ]
_duolib.GetDUOAutoExposure.restype = ct.c_bool

def GetDUOAutoExposure( duo ):
    """
    Returns DUO auto exposure value
    """
    val = ct.c_bool()
    _duolib.GetDUOAutoExposure( duo, ct.byref( val ) )
    return val.value

_duolib.GetDUOGain.argtypes = [ DUOInstance,
                               ct.POINTER( ct.c_double ) ]
_duolib.GetDUOGain.restype = ct.c_bool

def GetDUOGain( duo ):
    """
    Returns DUO gain value in percentage [0,100]
    """
    val = ct.c_double()
    _duolib.GetDUOGain( duo, ct.byref( val ) )
    return val.value

_duolib.GetDUOHFlip.argtypes = [ DUOInstance,
                               ct.POINTER( ct.c_bool ) ]
_duolib.GetDUOHFlip.restype = ct.c_bool

def GetDUOHFlip( duo ):
    """
    Returns DUO horizontal image flip value
    """
    val = ct.c_bool()
    _duolib.GetDUOHFlip( duo, ct.byref( val ) )
    return val.value

_duolib.GetDUOVFlip.argtypes = [ DUOInstance,
                               ct.POINTER( ct.c_bool ) ]
_duolib.GetDUOVFlip.restype = ct.c_bool

def GetDUOVFlip( duo ):
    """
    Returns DUO vertical image flip value
    """
    val = ct.c_bool()
    _duolib.GetDUOVFlip( duo, ct.byref( val ) )
    return val.value

_duolib.GetDUOCameraSwap.argtypes = [ DUOInstance,
                               ct.POINTER( ct.c_bool ) ]
_duolib.GetDUOCameraSwap.restype = ct.c_bool

def GetDUOCameraSwap( duo ):
    """
    Returns DUO camera swap value
    """
    val = ct.c_bool()
    _duolib.GetDUOCameraSwap( duo, ct.byref( val ) )
    return val.value

_duolib.GetDUOLedPWM.argtypes = [ DUOInstance,
                               ct.POINTER( ct.c_double ) ]
_duolib.GetDUOLedPWM.restype = ct.c_bool

def GetDUOLedPWM( duo ):
    """
    Returns DUO LED brightness in percentage [0,100]
    """
    val = ct.c_double()
    _duolib.GetDUOLedPWM( duo, ct.byref( val ) )
    return val.value

_duolib.GetDUOCalibrationPresent.argtypes = [ DUOInstance,
                               ct.POINTER( ct.c_bool ) ]
_duolib.GetDUOCalibrationPresent.restype = ct.c_bool

def GetDUOCalibrationPresent( duo ):
    """
    Returns DUO calibration present status value
    """
    val = ct.c_bool()
    _duolib.GetDUOCalibrationPresent( duo, ct.byref( val ) )
    return val.value

_duolib.GetDUOFOV.argtypes = [ DUOInstance,
                              ct.POINTER( ct.c_double ) ]
_duolib.GetDUOFOV.restype = ct.c_bool

def GetDUOFOV( duo ):
    """
    Returns DUO field of view for currently selected resolution.
    """
    val = ( ct.c_double * 4 )()
    _duolib.GetDUOFOV( duo, val )
    return tuple( val )

_duolib.GetDUORectifiedFOV.argtypes = [ DUOInstance,
                                       ct.POINTER( ct.c_double ) ]
_duolib.GetDUORectifiedFOV.restype = ct.c_bool

def GetDUORectifiedFOV( duo ):
    """
    Returns DUO rectified field of view for currently selected resolution.
    """
    val = ( ct.c_double * 4 )()
    _duolib.GetDUORectifiedFOV( duo, val )
    return tuple( val )

_duolib.GetDUOUndistort.argtypes = [ DUOInstance,
                                    ct.POINTER( ct.c_bool ) ]
_duolib.GetDUOUndistort.restype = ct.c_bool

def GetDUOUndistort( duo ):
    """
    Returns DUO image undistort value
    """
    val = ct.c_bool()
    _duolib.GetDUOUndistort( duo, ct.byref( val ) )
    return val.value

_duolib.GetDUOIntrinsics.argtypes = [ DUOInstance,
                                     ct.POINTER( DUO_INTR ) ]
_duolib.GetDUOIntrinsics.restype = ct.c_bool

def GetDUOIntrinsics( duo ):
    """
    Returns DUO camera intrinsics parameters, see DUO_INTR structure
    """
    val = DUO_INTR()
    _duolib.GetDUOIntrinsics( duo, ct.byref( val ) )
    return val

_duolib.GetDUOExtrinsics.argtypes = [ DUOInstance,
                                     ct.POINTER( DUO_EXTR ) ]
_duolib.GetDUOExtrinsics.restype = ct.c_bool

def GetDUOExtrinsics( duo, val ):
    """
    Returns DUO camera extrinsics parameters, see DUO_EXTR structure
    """
    val = DUO_EXTR()
    _duolib.GetDUOExtrinsics( duo, ct.byref( val ) )
    return val

_duolib.GetDUOStereoParameters.argtypes = [ DUOInstance,
                                     ct.POINTER( DUO_STEREO ) ]
_duolib.GetDUOStereoParameters.restype = ct.c_bool

def GetDUOStereoParameters( duo ):
    """
    Returns DUO camera stereo parameters, see DUO_STEREO structure
    """
    val = DUO_STEREO()
    return _duolib.GetDUOStereoParameters( duo, ct.byref( val ) )
    return val

_duolib.GetDUOIMURange.argtypes = [ DUOInstance,
                                   ct.POINTER( ct.c_int ),
                                   ct.POINTER( ct.c_int ) ]
_duolib.GetDUOIMURange.restype = ct.c_bool

def GetDUOIMURange( duo ):
    """
    Returns DUO currently selected IMU range
    @return: tuple(accel, gyro)
    """
    accel = ct.c_int()
    gyro = ct.c_int()
    _duolib.GetDUOIMURange( duo, ct.byref( accel ), ct.byref( gyro ) )
    return ( accel.value, gyro.value )

# Set DUO parameters
_duolib.SetDUOResolutionInfo.argtypes = [ DUOInstance, DUOResolutionInfo ]
_duolib.SetDUOResolutionInfo.restype = ct.c_bool

def SetDUOResolutionInfo( duo, res_info ):
    """
    Set current resolution for DUO.
    The DUOResolutionInfo is obtained by calling EnumerateDUOResolutions
    with desired image size, binning and frame rate.
    @return: True on success
    """
    return _duolib.SetDUOResolutionInfo( duo, res_info )

_duolib.SetDUOExposure.argtypes = [ DUOInstance, ct.c_double ]
_duolib.SetDUOExposure.restype = ct.c_bool

def SetDUOExposure( duo, val ):
    """
    Sets DUO exposure value in percentage [0,100]
    @return: True on success
    """
    return _duolib.SetDUOExposure( duo, ct.c_double( val ) )

_duolib.SetDUOExposureMS.argtypes = [ DUOInstance, ct.c_double ]
_duolib.SetDUOExposureMS.restype = ct.c_bool

def SetDUOExposureMS( duo, val ):
    """
    Sets DUO exposure value in milliseconds
    @return: True on success
    """
    return _duolib.SetDUOExposureMS( duo, ct.c_double( val ) )

_duolib.SetDUOAutoExposure.argtypes = [ DUOInstance, ct.c_bool ]
_duolib.SetDUOAutoExposure.restype = ct.c_bool

def SetDUOAutoExposure( duo, val ):
    """
    Sets DUO auto exposure value, default: false.
    The target exposure value is set using SetDUOExposure.
    @return: True on success
    """
    return _duolib.SetDUOAutoExposure( duo, ct.c_bool( val ) )

_duolib.SetDUOGain.argtypes = [ DUOInstance, ct.c_double ]
_duolib.SetDUOGain.restype = ct.c_bool

def SetDUOGain( duo, val ):
    """
    Sets DUO gain value in percentage [0,100], default: 0
    @return: True on success
    """
    return _duolib.SetDUOGain( duo, ct.c_double( val ) )

_duolib.SetDUOHFlip.argtypes = [ DUOInstance, ct.c_bool ]
_duolib.SetDUOHFlip.restype = ct.c_bool

def SetDUOHFlip( duo, val ):
    """
    Sets DUO horizontal image flip value, default: false
    @return: True on success
    """
    return _duolib.SetDUOHFlip( duo, ct.c_bool( val ) )

_duolib.SetDUOVFlip.argtypes = [ DUOInstance, ct.c_bool ]
_duolib.SetDUOVFlip.restype = ct.c_bool

def SetDUOVFlip( duo, val ):
    """
    Sets DUO vertical image flip value, default: false
    @return: True on success
    """
    return _duolib.SetDUOVFlip( duo, ct.c_bool( val ) )

_duolib.SetDUOCameraSwap.argtypes = [ DUOInstance, ct.c_bool ]
_duolib.SetDUOCameraSwap.restype = ct.c_bool

def SetDUOCameraSwap( duo, val ):
    """
    Sets DUO camera swap value, default: false
    @return: True on success
    """
    return _duolib.SetDUOCameraSwap( duo, ct.c_bool( val ) )

_duolib.SetDUOLedPWM.argtypes = [ DUOInstance, ct.c_double ]
_duolib.SetDUOLedPWM.restype = ct.c_bool

def SetDUOLedPWM( duo, val ):
    """
    Sets DUO LED brightness in percentage [0,100], default: 0
    @return: True on success
    """
    return _duolib.SetDUOLedPWM( duo, ct.c_double( val ) )

_duolib.SetDUOLedPWMSeq.argtypes = [ DUOInstance, PDUOLEDSeq, ct.c_uint32 ]
_duolib.SetDUOLedPWMSeq.restype = ct.c_bool

def SetDUOLedPWMSeq( duo, val, size ):
    """
    Sets DUO LED sequence, see DUOLEDSeq, default: none
    @param val: DUOLEDSeq array
    @return: True on success
    """
    return _duolib.SetDUOLedPWMSeq( duo, val, ct.c_uint32( size ) )

_duolib.SetDUOUndistort.argtypes = [ DUOInstance, ct.c_bool ]
_duolib.SetDUOUndistort.restype = ct.c_bool

def SetDUOUndistort( duo, val ):
    """
    Sets DUO image undistort value, default: false
    @return: True on success
    """
    return _duolib.SetDUOUndistort( duo, ct.c_bool( val ) )

_duolib.SetDUOIMURange.argtypes = [ DUOInstance, ct.c_int, ct.c_int ]
_duolib.SetDUOIMURange.restype = ct.c_bool

def SetDUOIMURange( duo, accel, gyro ):
    """
    Sets DUO IMU range, default: DUO_ACCEL_2G, DUO_GYRO_250
    @return: True on success
    """
    return _duolib.SetDUOIMURange( duo, ct.c_int( accel ), ct.c_int( gyro ) )

_duolib.SetDUOIMURate.argtypes = [ DUOInstance, ct.c_double ]
_duolib.SetDUOIMURate.restype = ct.c_bool

def SetDUOIMURate( duo, rate ):
    """
    Sets DUO IMU sampling rate [50,500] Hz, default: 100Hz.
    @return: True on success
    """
    return _duolib.SetDUOIMURate( duo, ct.c_double( rate ) )
