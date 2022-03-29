import curses
import sys
from curses import wrapper
from datetime import datetime
import time
import GPU_
import Util

DEFAULT_TIME_OUT = 60

def screen(stdscr, products: GPU_.GPU, GPU_GOAL_MODEL = ["3080","3070 Ti","3070"], GPU_GOAL_PRICE = [800.00,700.00,600.00]):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)
    BLUE = curses.color_pair(1)
    CYAN = curses.color_pair(2)
    GREEN = curses.color_pair(3)
    MAGENTA = curses.color_pair(4)
    RED = curses.color_pair(5)
    WHITE = curses.color_pair(6)
    YELLOW = curses.color_pair(7)
    BLACK = curses.color_pair(8)
    
    stdscr.nodelay(True)
    count_time = DEFAULT_TIME_OUT
    last_sent = datetime.now().strftime("%m/%d %H:%M")
    while True:
        rows, cols = stdscr.getmaxyx()
        if rows > 22 and cols > 80:
            windows3 = curses.newwin(1,75, 1, 1)
            windows3.clear()
            windows3.addstr(0, 0, f"'R'/Refresh   'DEL'/Exit   Next update: {count_time}   last email at {last_sent}")
            if count_time == DEFAULT_TIME_OUT:
                stdscr.clear()
                windows1 = curses.newwin(10, 70, 2, int(cols/2)-35)
                windows2 = curses.newwin(12, 70, 12, int(cols/2)-35)
                windows1.clear()
                windows2.clear()
                stdscr.attron(WHITE)
                stdscr.border()
                stdscr.attroff(WHITE)
                print_windows1(windows1, products, BLUE, BLACK, RED, YELLOW, GREEN)
                print_windows2(windows2, products, BLUE, YELLOW, WHITE, GREEN)
                # stdscr.move(rows-1,cols-1)
                stdscr.refresh()
                windows1.refresh()
                windows2.refresh()
            windows3.refresh()
        else:
            stdscr.refresh()
            
        if count_time == 0:
            Util.update_products(products)
            Util.update_json(products)
            temp = Util.send_email_at_goal(products, GPU_GOAL_MODEL, GPU_GOAL_PRICE)
            if temp: last_sent = datetime.now().strftime("%m/%d %H:%M")
            count_time = DEFAULT_TIME_OUT
            continue
        else:
            count_time -= 1
            time.sleep(1)
        try:
            key = stdscr.getkey()
        except:
            key = None
        if key == "KEY_DC":
            break
        if key == "r":
            count_time = DEFAULT_TIME_OUT
            continue

def print_windows1(windows1, products, BLUE, BLACK, RED, YELLOW, GREEN):
    windows1.attron(BLUE)
    windows1.border()
    windows1.attroff(BLUE)

    products_lowest_price = {
        "3090": sys.float_info.max, 
        "3080 Ti": sys.float_info.max, 
        "3080": sys.float_info.max, 
        "3070 Ti": sys.float_info.max, 
        "3070": sys.float_info.max, 
        "3060 Ti": sys.float_info.max, 
        "3060": sys.float_info.max, 
        "3050": sys.float_info.max
    }
    products_highest_price = {
        "3090": 0.0, 
        "3080 Ti": 0.0, 
        "3080": 0.0, 
        "3070 Ti": 0.0, 
        "3070": 0.0, 
        "3060 Ti": 0.0, 
        "3060": 0.0, 
        "3050": 0.0
    }
    for product in products:
        if (products_lowest_price[product.model] > product.price):
            products_lowest_price[product.model] = product.price
        if (products_highest_price[product.model] < product.price):
            products_highest_price[product.model] = product.price
    for i in range(len(GPU_.GPU_MODELS)):
        if GPU_.GPU_MODELS[i] not in products_lowest_price.keys():
            continue
        totalLen = 1
        windows1.addstr(i+1, totalLen, "                   ", BLACK)
        totalLen += len("                   ")
        if len(str(products_highest_price[GPU_.GPU_MODELS[i]])) < 7:
            windows1.addstr(i+1, totalLen, " " + str(products_highest_price[GPU_.GPU_MODELS[i]]), RED)
            totalLen += len(str(products_highest_price[GPU_.GPU_MODELS[i]])) + 1
        else:
            windows1.addstr(i+1, totalLen, str(products_highest_price[GPU_.GPU_MODELS[i]]), RED)
            totalLen += len(str(products_highest_price[GPU_.GPU_MODELS[i]]))
        windows1.addstr(i+1, totalLen, " <- ", BLUE)
        totalLen += len(str(" <- "))
        if len(GPU_.GPU_MODELS[i]) < 7:
            windows1.addstr(i+1, totalLen, "  " + GPU_.GPU_MODELS[i] + " ", YELLOW)
            totalLen += len(str(GPU_.GPU_MODELS[i])) + 3
        else:
            windows1.addstr(i+1, totalLen, GPU_.GPU_MODELS[i], YELLOW)
            totalLen += len(str(GPU_.GPU_MODELS[i]))
        windows1.addstr(i+1, totalLen, " -> ", BLUE)
        totalLen += len(str(" -> "))
        windows1.addstr(i+1, totalLen, str(products_lowest_price[GPU_.GPU_MODELS[i]]), GREEN)

def print_windows2(windows2, products, BLUE, YELLOW, WHITE, GREEN):
    windows2.attron(BLUE)
    windows2.border()
    windows2.attroff(BLUE)
    windows2.addstr(1,1, 'Lowest in stock:', BLUE)
    windows2.addstr(2,1, ' GPU      Price   Stock Name')
    line = 3
    for model in GPU_.GPU_MODELS:
        found = False
        lowest = sys.float_info.max
        title = ""
        stock = 0
        for product in products:
            if product.get_model() == model and product.get_stock() > 0:
                found = True
                if product.get_price() < lowest:
                    lowest = product.get_price()
                    title = product.get_title()
                    stock = product.get_stock()
        if found:
            totalLen = 2
            if len(model) < 7:
                windows2.addstr(line, totalLen, str(f'{model}   : '), YELLOW)
                totalLen += len(str(f'{model}   : '))
            else:
                windows2.addstr(line, totalLen, str(f'{model}: '), YELLOW)
                totalLen += len(str(f'{model}: '))
            if len(str(lowest)) < 7:
                windows2.addstr(line, totalLen, " " + str(lowest) + " ", GREEN)
                totalLen += len(" " + str(lowest) + " ")
            else:
                windows2.addstr(line, totalLen, str(lowest) + " ", GREEN)
                totalLen += len(str(lowest) + " ")
            if len(str(stock)) < 2:
                windows2.addstr(line, totalLen, " (" + str(stock) + ")  ", GREEN)
                totalLen += len(" (" + str(stock) + ")  ")
            else:
                windows2.addstr(line, totalLen, "(" + str(stock) + ")  ", GREEN)
                totalLen += len("(" + str(stock) + ")  ")
            if len(title) > 43:
                windows2.addstr(line, totalLen, title[0:43], WHITE)
            else:
                windows2.addstr(line, totalLen, title, WHITE)
            line += 1
    
def print_screen(products: GPU_.GPU):
    wrapper(screen, products)