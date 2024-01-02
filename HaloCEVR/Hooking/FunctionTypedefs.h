#pragma once

typedef void(*Func_UpdateCameraRotation)();
typedef void(*Func_InitDirectX)();
typedef void(__cdecl* Func_DrawFrame)(struct Renderer*, short, short*, float, float);
typedef void(*Func_SetViewportSize)();
typedef void(__stdcall* Func_DrawHUD)();
typedef void(*Func_DrawMenu)();
typedef void(__stdcall* Func_DrawScope)(void*);