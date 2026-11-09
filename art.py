import rich
from rich import print
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt

# this script will have the ascii art and other info printed by main.py on run

# Other possable tool names: "API Choir", "Scooter chaos", "Aviary", "Not Evil Flock"
# Other notes:
# A banner with more lines would allow for a better color gradent
# I could also have it do stacked banners, Like printing the art 3 times insted of 1 
# Make a script that takes exported hex codes from https://colordesigner.io/gradient-generator and then
# Fills in the multi line gradent print stuff
LINE1 = r"▄█████  ▄▄▄▄  ▄▄▄   ▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄    ▄█████ ▄▄ ▄▄  ▄▄▄  ▄▄ ▄▄▄▄  "
LINE2 = r"▀▀▀▄▄▄ ██▀▀▀ ██▀██ ██▀██  ██   ██▄▄  ██▄█▄   ██     ██▄██ ██▀██ ██ ██▄█▄ "
LINE3 = r"█████▀ ▀████ ▀███▀ ▀███▀  ██   ██▄▄▄ ██ ██   ▀█████ ██ ██ ▀███▀ ██ ██ ██ "
# used this generator: https://patorjk.com/software/taag/#p=testall&f=Rebel&t=Scooter+Choir%0A&x=none&v=4&h=4&w=80&we=false
# style: ANSI Compact

def render_banner():
    # Multi art Cyan to Purple gradent
    print(f"[#00ffff]{LINE1}[/#00ffff]")
    print(f"[#10efff]{LINE2}[/#10efff]")
    print(f"[#5cdcff]{LINE3}[/#5cdcff]")
    print(f"[#72cbff]{LINE1}[/#72cbff]")
    print(f"[#81b9ff]{LINE2}[/#81b9ff]")
    print(f"[#91a5ff]{LINE3}[/#91a5ff]")
    print(f"[#a58cff]{LINE1}[/#a58cff]")
    print(f"[#c065ff]{LINE2}[/#c065ff]")
    print(f"[#d936f2]{LINE3}[/#d936f2]")

    print("\n[green]By James Perry | github: https://github.com/perryjc | Website: https://perryjc.github.io/[/green]")


# UNUSED BANNERS:

# Cyan to Purple gradent
#print(f"[dark_slate_gray2]{LINE1}[/dark_slate_gray2]")
#print(f"[cornflower_blue]{LINE2}[/cornflower_blue]")
#print(f"[blue_violet]{LINE3}[/blue_violet]")

# Cyian to Purple gradent (useing hex codes)
#print(f"[#10E4DA]{LINE1}[/#10E4DA]")
#print(f"[#648ED3]{LINE2}[/#648ED3]")
#print(f"[#B838CC]{LINE3}[/#B838CC]")

# Cyan to green gradent
# print(f"[cyan1]{LINE1}[/cyan1]")
# print(f"[spring_green1]{LINE2}[/spring_green1]")
# print(f"[green3]{LINE3}[/green3]")

# placeholder values:

#email = "bird@bird.co"
#alarm = False
#latitude = "38.8820057"
#longitude = "-77.1115141"
#auth_timestamp = "2026-11-09"
# connection_active = True
# auth_token_valid = True
# add something that finds how many birds will chirp near by (before line 218 of main.py)

def print_user_selections(email, alarm, lat, long, auth_time):
    if alarm:
        alarm_value = "[bold #5BEB42]ACTIVE[/bold #5BEB42]"
    else: 
        alarm_value = "[bold #F23C24]INACTIVE[/bold #F23C24]"

    print("")
    table = Table(title="[bold bright_cyan]Selections[/bold bright_cyan]")

    table.add_column("option", justify="left", style="#F5AE5D")
    table.add_column("value", justify="right", style="bold bright_cyan")

    table.add_row("Email:", f"[#C580F2]{email}[/#C580F2]") #value violet
    table.add_row("Token Timestamp:", f"[#C580F2]{auth_time}[/#C580F2]") #value violet
    table.add_row("Connection:", "[bold #5BEB42]ACTIVE[/bold #5BEB42]") # option yellow, value green
    table.add_row("Auth_token:", "[bold #5BEB42]VALID[/bold #5BEB42]") # option yellow, value green
    table.add_row("Latitude:", str(lat)) # value blue
    table.add_row("Longitude:", str(long)) # Value blue
    table.add_row("Alarm:", alarm_value) # Value green or red

    console = Console()
    console.print(table)

    Prompt.ask("[#F5AE5D]Press Enter to Continue...[/#F5AE5D]")

#print_user_selections(email, alarm, latitude, longitude, auth_timestamp)