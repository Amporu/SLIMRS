#ifndef TAISIM_H  // Header guard to prevent multiple inclusion
#define TAISIM_H
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>  // Added SDL_image header
namespace Simulator
{
    const int SCREEN_WIDTH = 640;
    const int SCREEN_HEIGHT = 480;

    class Render //Class for rendering graphics
    {
    public:
        static bool isRunning;
        static SDL_Window* window;
        static SDL_Renderer* renderer;
        static SDL_Surface* logoSurface;
        static SDL_Texture* logoTexture;
        //static SDL_Surface* logo;
        
    };
    void release();
    int isOpened();
    void init();  //init simulator

    void run();
}
#endif
