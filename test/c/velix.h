#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#if defined(_WIN32)
    #define APIEXPORT __declspec(dllexport)
#else
    #define APIEXPORT __attribute__((visibility("default")))
#endif

#include <stdbool.h>

typedef struct VlWindow_T* VlWindow;
typedef struct VlTest_T* VlTest;

typedef enum VlResult {
    VL_SUCCESS = 0,
    VL_FAIL = 1
} VlResult;

APIEXPORT VlResult vlCreateWindow(
    const char* title,
    int width,
    VlWindow* pOutWindow
);

APIEXPORT void vlDestroyWindow(
    VlWindow window
);

APIEXPORT void vlShowWindow(
    VlWindow window,
    bool show
);

APIEXPORT const char* vlGetPip(
    VlWindow window
);

APIEXPORT int vlGetWindowWidth(
    VlWindow window
);

APIEXPORT int vlSetWindowWidth(
    VlWindow window,
    int width
);

APIEXPORT VlTest vlCreateTest();

APIEXPORT void vlDestroyTest(
    VlTest test
);

#ifdef __cplusplus
}
#endif
