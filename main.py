import Util
from GUI_ import screen_tk
from Email_ import check_gmail_server

def main():
    check_gmail_server()
    products = []
    
    Util.setup_products(products)
    Util.clear_json_file()
    screen_tk(products)
    
if __name__ == "__main__":
    main()