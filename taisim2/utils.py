
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