import os
from taisim2.logging_system import logger
VERSION='0.0.1'
logger.info(f"VERSION : \033[92m{VERSION}\033[0m",)

LEVEL1 = os.path.join(os.path.dirname(__file__), 'data/LineFollower1.png')
LEVEL2 = os.path.join(os.path.dirname(__file__), 'data/LineFollower2.png')
LEVEL3 = os.path.join(os.path.dirname(__file__), 'data/LaneKeeper1.png')
LEVEL4 = os.path.join(os.path.dirname(__file__), 'data/LaneKeeper2.png')
LEVEL5 = os.path.join(os.path.dirname(__file__), 'data/LaneKeeper3.png')
LEVEL6 = os.path.join(os.path.dirname(__file__), 'data/Cropps1.png')
LEVEL7 = os.path.join(os.path.dirname(__file__), 'data/Cropps2.png')
LOGO   = os.path.join(os.path.dirname(__file__), 'data/taisim_logo.png')

data=[LEVEL1,LEVEL2,LEVEL3,LEVEL4,LEVEL5,LEVEL6,LEVEL7,LOGO]
ok=0
for item in data:

    if os.path.exists(item) and ok==0:
        continue
    else:
        ok=1
        break

    
if ok==1:
    logger.info("ASSETS : \033[92m Not OK\033[0m")
else:
    logger.info("ASSETS : \033[92m OK\033[0m")

SIMULATOR=os.path.join(os.path.dirname(__file__), 'simulator.py')

UTILS=os.path.join(os.path.dirname(__file__), 'utils.py')
if os.path.exists(SIMULATOR):
    logger.info("SCRIPTS : \033[92mOK\033[0m")



def rgb_to_ansi_escape(red, green, blue):
    # Convert normalized values to standard 8-bit integers (0-255)
    r_int = round(red * 255)
    g_int = round(green * 255)
    b_int = round(blue * 255)

    # Construct the ANSI escape sequence for setting text color
    ansi_color_code = f"\033[38;2;{r_int};{g_int};{b_int}m"

    return ansi_color_code
def rgb_to_ansi_background(red, green, blue):
    # Convert normalized values to standard 8-bit integers (0-255)
    r_int = round(red * 255)
    g_int = round(green * 255)
    b_int = round(blue * 255)

    # Construct the ANSI escape sequence for setting background color
    ansi_color_code = f"\033[48;2;{r_int};{g_int};{b_int}m"

    return ansi_color_code
