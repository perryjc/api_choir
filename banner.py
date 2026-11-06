import rich
from rich import print
from rich.console import Console
from rich.text import Text

# this script will have the ascii art and other info printed by main.py on run

# Other possable tool names: "API Choir", "Scooter chaos", "Aviary", "Not Evil Flock"
LINE1 = r"▄█████  ▄▄▄▄  ▄▄▄   ▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄    ▄█████ ▄▄ ▄▄  ▄▄▄  ▄▄ ▄▄▄▄  "
LINE2 = r"▀▀▀▄▄▄ ██▀▀▀ ██▀██ ██▀██  ██   ██▄▄  ██▄█▄   ██     ██▄██ ██▀██ ██ ██▄█▄ "
LINE3 = r"█████▀ ▀████ ▀███▀ ▀███▀  ██   ██▄▄▄ ██ ██   ▀█████ ██ ██ ▀███▀ ██ ██ ██ "
# used this generator: https://patorjk.com/software/taag/#p=testall&f=Rebel&t=Scooter+Choir%0A&x=none&v=4&h=4&w=80&we=false
# style: ANSI Compact

# Cyian to Purple gradent
# print(f"[dark_slate_gray2]{LINE1}[/dark_slate_gray2]")
# print(f"[cornflower_blue]{LINE2}[/cornflower_blue]")
# print(f"[blue_violet]{LINE3}[/blue_violet]")

print(f"[dark_slate_gray2]{LINE1}[/dark_slate_gray2]")
print(f"[cornflower_blue]{LINE2}[/cornflower_blue]")
print(f"[blue_violet]{LINE3}[/blue_violet]")