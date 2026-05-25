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

#ifdef __cplusplus
}
#endif