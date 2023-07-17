#g++ -shared -o taisim.so taisim.cpp -lSDL2 -lSDLimage
#g++ -c taisim.cpp -o taisim.o
#ar rcs libtaisim.a taisim.o
g++ taisim.cpp -o mylibrary -lSDL2 -lSDL2_image