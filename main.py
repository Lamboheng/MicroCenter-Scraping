import Util
from GUI_ import screen_tk

def main():
    products = []
    
    Util.setup_products(products)
    Util.clear_json_file()
    screen_tk(products)
    
if __name__ == "__main__":
    main()