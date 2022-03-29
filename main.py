import Util
from GUI_ import print_screen

def main():
    products = []
    Util.setup_products(products)
    print_screen(products, ["3080","3070 Ti","3070"], [800.00,700.00,600.00])
    
if __name__ == "__main__":
    main()