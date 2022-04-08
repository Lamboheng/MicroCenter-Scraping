import Util
from GUI_ import screen_tk
from Email_ import check_gmail_server

def main():
    try:
        check_gmail_server()
        products = []
        
        Util.setup_products(products)
        Util.clear_json_file()
        screen_tk(products)
    except Exception as e:
        print(e)
        input("Press Enter to exit.")
        
    
if __name__ == "__main__":
    main()