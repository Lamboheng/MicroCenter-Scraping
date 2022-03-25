import Util
import json

def main():
    products = []
    Util.setup_products(products)
    
    Util.print_products(products)
    
if __name__ == "__main__":
    main()