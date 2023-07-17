

#include "taisim.h"
int main(int argc, char* argv[])
{

    Simulator::init();
    while(Simulator::isOpened())
        {
        Simulator::run();
        }
    Simulator::release();
    return 0;
}
