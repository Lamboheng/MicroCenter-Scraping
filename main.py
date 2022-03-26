import Util
import time

def main():
    products = []
    Util.setup_products(products)
    # time.sleep(3)
    # Util.update_products(products)
    Util.update_json(products)
    Util.print_products(products)
    
if __name__ == "__main__":
    main()