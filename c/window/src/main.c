#include <Windows.h>

LRESULT CALLBACK WinProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    HDC hDc;
    switch (uMsg) {
        case WM_PAINT:
            hDc = GetDC(hWnd);
            RECT rect = {
                75,
                75,
                250,
                250,
            };
            HBRUSH hBr = CreateSolidBrush(RGB(0, 255, 0));
            FillRect(hDc, &rect, hBr);
            DeleteObject(hBr);
            ReleaseDC(hWnd, hDc);
            return 0;

        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;

        default:
            return DefWindowProcA(hWnd, uMsg, wParam, lParam);
    }

    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE a, PSTR b, int nCmdShow) {
    WNDCLASSA class = {
        0,
        WinProc,
        0,
        0,
        hInstance,
        NULL,
        NULL,
        NULL,
        NULL,
        "C_Window",
    };

    RegisterClassA(&class);

    HWND windowHandle = CreateWindowA("C_Window", "C Window", WS_CAPTION | WS_POPUP | WS_SYSMENU, 50, 50, 500, 500, NULL, NULL, hInstance, NULL);

    ShowWindow(windowHandle, nCmdShow);

    MSG msg;

    while (TRUE) {
        if (GetMessageA(&msg, NULL, 0, 0) == 0) {
            break;
        }

        DispatchMessageA(&msg);
    }

    return 0;
}