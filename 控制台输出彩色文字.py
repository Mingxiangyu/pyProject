from colorama import init, Fore, Back, Style


def 初级使用():
    init(autoreset=True)
    print(Style.BRIGHT + Back.BLACK + Fore.RED + "from colorama import init, Fore, Back, Style")


# 简单的变色函数
background_color_dict = {
    'BLACK': 40,
    'RED': 41,
    'GREEN': 42,
    'YELLOW': 43,
    'BLUE': 44,
    'MAGENTA': 45,
    'CYAN': 46,
    'WHITE': 47
}

text_color_dict = {
    'BLACK': 30,
    'RED': 31,
    'GREEN': 32,
    'YELLOW': 33,
    'BLUE': 34,
    'MAGENTA': 35,
    'CYAN': 36,
    'WHITE': 37
}

style_dict = {
    'normal': 0,
    'bold': 1,
    'light': 2,
    'italicize': 3,
    'underline': 4,
    'blink': 5
}


def set_text_color(str_text, style, text_color, background_color):
    str = str_text
    style_code = style_dict[style]
    text_color_code = text_color_dict[text_color]
    back_color_code = background_color_dict[background_color]
    print_text = f'\033[{style_code};{text_color_code};{back_color_code}m{str}\033[0m'
    return print_text


print(set_text_color("ceshishuchu", "bold", "RED", "BLACK"))
