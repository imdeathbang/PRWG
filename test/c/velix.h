#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#if defined(_WIN32)
    #define APIEXPORT __declspec(dllexport)
#else
    #define APIEXPORT __attribute((visibility("default")))
#endif

typedef struct VlWindow_T* VlWindow;
typedef struct VlTest_T* VlTest;

//Pepe
APIEXPORT VlResult vlCreateWindow()
//Pepe
APIEXPORT VlTest vlCreateTest()

#ifdef __cplusplus
}
#endif