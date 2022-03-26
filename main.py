import Util
from Email_ import send_email
import time

def main():
    products = []
    Util.setup_products(products)
    # time.sleep(3)
    # Util.update_products(products)
    # Util.update_json(products)
    Util.print_products(products)
    if send_email(products[0]):
        print("email sent")
    
    
if __name__ == "__main__":
    main()