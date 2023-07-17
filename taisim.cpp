#include "taisim.h"
namespace Simulator
{
    
    bool Render::isRunning = false;
    SDL_Window* Render::window = nullptr;
    SDL_Renderer* Render::renderer = nullptr;
    SDL_Surface* Render::logoSurface=nullptr;
    SDL_Texture* Render::logoTexture=nullptr;
    void release()
    {
                // Clean up resources
        SDL_DestroyTexture(Render::logoTexture);
        SDL_DestroyRenderer(Render::renderer);
        SDL_DestroyWindow(Render::window);

        // Quit SDL_image and SDL
        IMG_Quit();
        SDL_Quit();
    }
    int isOpened()
    {
        if (Render::isRunning)
        {
            return 1;
        }
        else return 0;
    }
    void init()
    {
        Render::isRunning = true;
         if (SDL_Init(SDL_INIT_VIDEO) < 0) {
            SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "SDL initialization failed: %s", SDL_GetError());
            return;
        }

        // Initialize SDL_image library
        if (IMG_Init(IMG_INIT_PNG) < 0) {
            SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "SDL_image initialization failed: %s", IMG_GetError());
            SDL_Quit();
            return;
        }

        Render::window = SDL_CreateWindow("SDL Animation", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
        if (!Render::window) {
            SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Window creation failed: %s", SDL_GetError());
            SDL_Quit();
            return;
        }

        Render::renderer = SDL_CreateRenderer(Render::window, -1, SDL_RENDERER_ACCELERATED);
        if (!Render::renderer) {
            SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Renderer creation failed: %s", SDL_GetError());
            SDL_DestroyWindow(Render::window);
            SDL_Quit();
            return;
        }
                // Load PNG image
        Render::logoSurface = IMG_Load("taisim.png");
        // Create texture from the loaded image
        Render::logoTexture = SDL_CreateTextureFromSurface(Render::renderer, Render::logoSurface);
        // Get the image dimensions
        int imageWidth = Render::logoSurface->w;
        int imageHeight = Render::logoSurface->h;

        SDL_FreeSurface(Render::logoSurface);  // Free the surface after creating the texture
    }
    void run()
    {

        Render::isRunning = true;

            SDL_Event event;
            while (SDL_PollEvent(&event) != 0) {
                if (event.type == SDL_QUIT) {
                    Render::isRunning = false;
                }
            }

            // Update animation logic

            SDL_SetRenderDrawColor(Render::renderer, 0, 0, 0, 255);
            SDL_RenderClear(Render::renderer);

            // Render the image texture
            SDL_RenderCopy(Render::renderer, Render::logoTexture, nullptr, nullptr);

            SDL_RenderPresent(Render::renderer);

            SDL_Delay(10);
        


    }
}
