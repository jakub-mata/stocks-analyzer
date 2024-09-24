import argparse

parser = argparse.ArgumentParser(
    prog="interface.py",
    description="Presents valuable data on given stocks"
)

parser.add_argument("query", nargs="+", help="stock name to evaluate")
parser.add_argument("--no_table", "-t", action="store_false", help="disable displaying a table with data")
parser.add_argument("--no_plot", "-p", action="store_false" ,help="disable showing a plot with data")
parser.add_argument("--merge", action = "store_true", help="display multiple stocks in one plot (disabled by default)")
parser.add_argument("--plain", action="store_false", help="disable displaying linear approximation")


def args():
    return parser.parse_args()

def find_wanted_stock(options) -> int or bool:
    """
    Takes in a list of options that might be the desired search. Then presents them to the user
    and checks which one he picked. 

    Args:
        options: a list of possible options

    Returns an index of the chosen search value relative to the options list. Returns false if none 
    matches. Returns False for incorrect input.   
    """
    print("Matches found. Type the correct number. Type -1 if none match:")
    for i in range(len(options)):
        print(f"{i+1}. {options[i]}")
    picked = input("Type here: ")

    try:
        picked = int(picked)
        if picked <=0 or picked > len(options):
            return False
        return (picked-1)
    except ValueError:  #picked cannot be converted to int
        return False