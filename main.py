import Util
from Email_ import send_email
from GUI_ import print_screen

def main():
    products = []
    Util.setup_products(products)
    # time.sleep(3)
    # Util.update_products(products)
    # Util.update_json(products)
    # print(Util.products_str(products))
    print_screen(products)
    
    
    
if __name__ == "__main__":
    main()