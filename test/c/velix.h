#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#if defined(_WIN32)
    #define APIEXPORT __declspec(dllexport)
#else
    #define APIEXPORT __attribute((visibility("default")))
#endif

#include <stdbool.h>

typedef struct VlWindow_T* VlWindow;
typedef struct VlTest_T* VlTest;

#ifdef __cplusplus
}
#endif