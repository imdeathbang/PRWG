#pragma once

typedef struct VlWindow_T* VlWindow;

typedef enum VlResult {
    VL_SUCCESS = 0,
    VL_FAIL = 0
} VlResult;

void vlCreateWindow(
    const char* title,
    VlWindow* pOutWindow
);
void vlDestroyWindow(
    VlWindow window
);

const char* vlGetWindowWidth(
    VlWindow window
);

const char* vlSetWindowWidth(
    VlWindow window
);