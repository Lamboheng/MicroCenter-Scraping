import Util
from GUI_ import screen_curses
from GUI_ import screen_tk

def main():
    products = []
    
    Util.setup_products(products)
    Util.clear_json_file()
    # screen_curses(products, ["3080","3070 Ti","3070"], [800.00,700.00,600.00])
    screen_tk(products)
    
if __name__ == "__main__":
    main()