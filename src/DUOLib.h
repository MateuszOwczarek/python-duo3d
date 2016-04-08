//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// This library is part of DUO SDK that allows the use of DUO devices in your own applications
//
// For updates and file downloads go to: http://duo3d.com/
//
// Copyright 2014-2015 (c) Code Laboratories, Inc.  All rights reserved.
//
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifndef _DUOLIB_H
#define _DUOLIB_H

#include <stdint.h>

#ifdef WIN32
    #ifdef DUOLIB_DLL
		#define API_FUNCTION(type)	__declspec(dllexport) type __cdecl
	#else
		#define API_FUNCTION(type)	__declspec(dllimport) type __cdecl
	#endif
    #define CALLBACK    __stdcall
#else
	#define API_FUNCTION(type)	 __attribute__((visibility("default"))) type
	#define CALLBACK
#endif

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// DUO C API
extern "C" {

// DUO instance
typedef void *DUOInstance;

// DUO binning
enum DUOBinning
{
	DUO_BIN_ANY = -1,
	DUO_BIN_NONE = 0,
	DUO_BIN_HORIZONTAL2 = 1,        // Horizontal binning by factor of 2
	DUO_BIN_HORIZONTAL4 = 2,        // Horizontal binning by factor of 4
	DUO_BIN_VERTICAL2 = 4,          // Vertical binning by factor of 2
	DUO_BIN_VERTICAL4 = 8           // Vertical binning by factor of 4
};

// DUO resolution info
typedef struct
{
	int   width;
	int   height;
	int   binning;
	float fps;
	float minFps;
	float maxFps;
}DUOResolutionInfo, *PDUOResolutionInfo;

// DUO IMU data sample
typedef struct
{
    float tempData;                 // DUO temperature data
    float accelData[3];             // DUO accelerometer data (x,y,z)
    float gyroData[3];      		// DUO gyroscope data (x,y,z)
}DUOIMUSample;

#define DUO_MAX_IMU_SAMPLES     100

// DUO Frame
typedef struct
{
    uint32_t     width;				// DUO frame width
    uint32_t     height;			// DUO frame height
    uint8_t      ledSeqTag;			// DUO frame LED tag
    uint32_t     timeStamp;			// DUO frame time stamp in 100us increments
    uint8_t     *leftData;			// DUO left frame data
    uint8_t     *rightData;			// DUO right frame data
    uint8_t      IMUPresent;        // True if IMU chip is present (DUO MLX)
    uint32_t     IMUSamples;        // Number of IMU data samples in this frame
    DUOIMUSample IMUData[DUO_MAX_IMU_SAMPLES];	// DUO IMU data samples
}DUOFrame, *PDUOFrame;

// DUO LED PWM
typedef struct  
{
	uint8_t ledPwmValue[4];			// LED PWM values are in percentage [0,100]
}DUOLEDSeq, *PDUOLEDSeq;

// DUO Accelerometer Range
enum DUOAccelRange
{
    DUO_ACCEL_2G = 0,				// DUO Accelerometer full scale range +/- 2g
    DUO_ACCEL_4G,               	// DUO Accelerometer full scale range +/- 4g
    DUO_ACCEL_8G,               	// DUO Accelerometer full scale range +/- 8g
    DUO_ACCEL_16G               	// DUO Accelerometer full scale range +/- 16g
};

// DUO Gyroscope Range
enum DUOGyroRange
{
    DUO_GYRO_250 = 0,				// DUO Gyroscope full scale range 250 deg/s
    DUO_GYRO_500,               	// DUO Gyroscope full scale range 500 deg/s
    DUO_GYRO_1000,               	// DUO Gyroscope full scale range 1000 deg/s
    DUO_GYRO_2000               	// DUO Gyroscope full scale range 2000 deg/s
};

#pragma pack(push, 1)
struct DUO_INTR
{
    uint16_t width;
    uint16_t height;
    struct INTR
    {
        double k1, k2, k3;          // Camera radial distortion coefficients
        double k4, k5, k6;          // Camera radial distortion coefficients
        double p1, p2;              // Camera tangential distortion coefficients
        double fx, fy;              // Camera focal lengths in pixel units
        double cx, cy;              // Camera principal point
    };
    INTR left;
    INTR right;
};
struct DUO_EXTR
{
    double rotation[9];
    double translation[3];
};
struct DUO_STEREO
{
    double M1[9], M2[9];            // 3x3 - Camera matrices
    double D1[8], D2[8];            // 1x8 - Camera distortion parameters
    double R[9];                    // 3x3 - Rotation between left and right camera
    double T[3];                    // 3x1 - Translation vector between left and right camera
    double R1[9], R2[9];            // 3x3 - Rectified rotation matrices
    double P1[12], P2[12];          // 3x4 - Rectified projection matrices
    double Q[16];                   // 4x4 - Disparity to depth mapping matrix
};
#pragma pack(pop)

// DUO parameters
enum DUOParameter
{
	// DUO parameter unit
	DUO_PERCENTAGE,
	DUO_MILLISECONDS,
	// DUO Camera parameters
	DUO_DEVICE_NAME,                // Get only: (string allocated by user min size 252 bytes)
	DUO_SERIAL_NUMBER,              // Get only: (string allocated by user min size 252 bytes)
	DUO_FIRMWARE_VERSION,           // Get only: (string allocated by user min size 252 bytes)
	DUO_FIRMWARE_BUILD,             // Get only: (string allocated by user min size 252 bytes)
	DUO_RESOLUTION_INFO,            // Set/Get:  (PDUOResolutionInfo) - must be first parameter to set
	DUO_FRAME_DIMENSION,            // Get only: (uint32_t, uint32_t)
	DUO_EXPOSURE,                   // Set/Get:  (double [0,100], DUO_PERCENTAGE) or (double in milliseconds, DUO_MILLISECONDS)
	DUO_GAIN,                       // Set/Get:  (double [0,100])
	DUO_HFLIP,                      // Set/Get:  (bool [false,true])
	DUO_VFLIP,                      // Set/Get:  (bool [false,true])
	DUO_SWAP_CAMERAS,               // Set/Get:  (bool [false,true])
	// DUO LED Control Parameters
	DUO_LED_PWM,                    // Set/Get:  (double [0,100])
	DUO_LED_PWM_SEQ,                // Set only: (PDUOLEDSeq, int) - number of LED sequence steps (max 64)
	// DUO Calibration Parameters
	DUO_CALIBRATION_PRESENT,        // Get Only: return true if calibration data is present
	DUO_FOV,                        // Get Only: (PDUOResolutionInfo, double* (leftHFOV, leftVFOV, rightHFOV, rightVFOV)
	DUO_UNDISTORT,                  // Set/Get:  (bool [false,true])
    DUO_INRINSICS,                  // Get Only: (pointer to DUO_INTR structure)
    DUO_EXTRINSICS,                 // Get Only: (pointer to DUO_EXTR structure)
    DUO_STEREO_PARAMETERS,          // Get Only: (pointer to DUO_STEREO structure)
	// DUO IMU Parameters
	DUO_IMU_RANGE,                  // Set/Get: (DUOAccelRange, DUOGyroRange)
};

API_FUNCTION(char*) GetLibVersion();

// DUO resolution enumeration
// To enumerate resolution settings for specific resolution, set width and height and optionally fps.
// To enumerate all supported resolutions set width, height and fps all to -1.
// NOTE: There are large number of resolution setting supported.
API_FUNCTION(int) EnumerateResolutions(DUOResolutionInfo *resList, int32_t resListSize, 
									   int32_t width = -1, int32_t height = -1, int32_t binning = DUO_BIN_ANY, float fps = -1);

// DUO device initialization
API_FUNCTION(bool) OpenDUO(DUOInstance *duo);
API_FUNCTION(bool) CloseDUO(DUOInstance duo);

// DUO frame callback function
// NOTE: This function is called in the context of the DUO capture thread.
//		 To prevent any dropped frames, this function must return as soon as possible.
typedef void (CALLBACK *DUOFrameCallback)(const PDUOFrame pFrameData, void *pUserData);

// DUO device capture control
API_FUNCTION(bool) StartDUO(DUOInstance duo, DUOFrameCallback frameCallback, void *pUserData, bool masterMode = true);
API_FUNCTION(bool) StopDUO(DUOInstance duo);

// DUO Camera parameters control
// Do not call these functions directly
// Use below defined macros
API_FUNCTION(bool) __DUOParamSet__(DUOInstance duo, int param, ...);
API_FUNCTION(bool) __DUOParamGet__(DUOInstance duo, int param, ...);

// Get DUO parameters
#define GetDUODeviceName(duo, val)          __DUOParamGet__(duo, DUO_DEVICE_NAME, (char*)val)
#define GetDUOSerialNumber(duo, val)        __DUOParamGet__(duo, DUO_SERIAL_NUMBER, (char*)val)
#define GetDUOFirmwareVersion(duo, val)     __DUOParamGet__(duo, DUO_FIRMWARE_VERSION, (char*)val)
#define GetDUOFirmwareBuild(duo, val)       __DUOParamGet__(duo, DUO_FIRMWARE_BUILD, (char*)val)
#define GetDUOResolutionInfo(duo, val)      __DUOParamGet__(duo, DUO_RESOLUTION_INFO, (DUOResolutionInfo*)val)
#define GetDUOFrameDimension(duo, w, h)     __DUOParamGet__(duo, DUO_FRAME_DIMENSION, (uint32_t*)w, (uint32_t*)h)
#define GetDUOExposure(duo, val)            __DUOParamGet__(duo, DUO_EXPOSURE, (double*)val, DUO_PERCENTAGE)
#define GetDUOExposureMS(duo, val)          __DUOParamGet__(duo, DUO_EXPOSURE, (double*)val, DUO_MILLISECONDS)
#define GetDUOGain(duo, val)                __DUOParamGet__(duo, DUO_GAIN, (double*)val)
#define GetDUOHFlip(duo, val)               __DUOParamGet__(duo, DUO_HFLIP, (int*)val)
#define GetDUOVFlip(duo, val)               __DUOParamGet__(duo, DUO_VFLIP, (int*)val)
#define GetDUOCameraSwap(duo, val)          __DUOParamGet__(duo, DUO_SWAP_CAMERAS, (int*)val)
#define GetDUOLedPWM(duo, val)              __DUOParamGet__(duo, DUO_LED_PWM, (double*)val)
#define GetDUOCalibrationPresent(duo)       __DUOParamGet__(duo, DUO_CALIBRATION_PRESENT)
#define GetDUOFOV(duo, ri, val)             __DUOParamGet__(duo, DUO_FOV, (DUOResolutionInfo&)ri, (double*)val)
#define GetDUOUndistort(duo, val)           __DUOParamGet__(duo, DUO_UNDISTORT, (int*)val)
#define GetDUOIntrinsics(duo, val)          __DUOParamGet__(duo, DUO_INRINSICS, (DUO_INTR*)val)
#define GetDUOExtrinsics(duo, val)          __DUOParamGet__(duo, DUO_EXTRINSICS, (DUO_EXTR*)val)
#define GetDUOStereoParameters(duo, val)    __DUOParamGet__(duo, DUO_STEREO_PARAMETERS, (DUO_STEREO*)val)
#define GetDUOIMURange(duo, accel, gyro)    __DUOParamGet__(duo, DUO_IMU_RANGE, (int*)accel, (int*)gyro)

// Set DUO parameters
#define SetDUOResolutionInfo(duo, val)      __DUOParamSet__(duo, DUO_RESOLUTION_INFO, (DUOResolutionInfo&)val)
#define SetDUOExposure(duo, val)            __DUOParamSet__(duo, DUO_EXPOSURE, (double)val, DUO_PERCENTAGE)
#define SetDUOExposureMS(duo, val)          __DUOParamSet__(duo, DUO_EXPOSURE, (double)val, DUO_MILLISECONDS)
#define SetDUOGain(duo, val)                __DUOParamSet__(duo, DUO_GAIN, (double)val)
#define SetDUOHFlip(duo, val)               __DUOParamSet__(duo, DUO_HFLIP, (int)val)
#define SetDUOVFlip(duo, val)               __DUOParamSet__(duo, DUO_VFLIP, (int)val)
#define SetDUOCameraSwap(duo, val)          __DUOParamSet__(duo, DUO_SWAP_CAMERAS, (int)val)
#define SetDUOLedPWM(duo, val)              __DUOParamSet__(duo, DUO_LED_PWM, (double)val)
#define SetDUOLedPWMSeq(duo, val, size)     __DUOParamSet__(duo, DUO_LED_PWM_SEQ, (PDUOLEDSeq)val, (uint32_t)size)
#define SetDUOUndistort(duo, val)           __DUOParamSet__(duo, DUO_UNDISTORT, (int)val)
#define SetDUOIMURange(duo, accel, gyro)    __DUOParamSet__(duo, DUO_IMU_RANGE, (int)accel, (int)gyro)

} // extern "C"

#endif // _DUOLIB_H
