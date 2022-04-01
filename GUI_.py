from curses import wrapper
from tkinter import *
from datetime import datetime
import curses
import sys
import time
from turtle import width
import webbrowser

import GPU_
import Util

DEFAULT_TIME_OUT = 60
GPU_GOAL_PRICE = {
    '3090 Ti': 0.0,
    '3090': 0.0,
    '3080 Ti': 0.0,
    '3080': 800.0,
    '3070 Ti': 700.0,
    '3070': 600.0,
    '3060 Ti': 0.0,
    '3060': 0.0,
    '3050 Ti': 0.0,
    '3050': 0.0
}

def curses_screen(stdscr, products: GPU_.GPU):
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
    last_sent = "00/00 00:00"
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
                curses_windows1(windows1, products, BLUE, BLACK, RED, YELLOW, GREEN)
                curses_windows2(windows2, products, BLUE, YELLOW, WHITE, GREEN)
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
            temp = Util.send_email_at_goal(products, GPU_GOAL_PRICE)
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

def curses_windows1(windows1, products, BLUE, BLACK, RED, YELLOW, GREEN):
    windows1.attron(BLUE)
    windows1.border()
    windows1.attroff(BLUE)

    products_lowest_price, products_highest_price = Util.find_lowest_highest(products)
    
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

def curses_windows2(windows2, products, BLUE, YELLOW, WHITE, GREEN):
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
    
def screen_curses(products: GPU_.GPU):
    wrapper(curses_screen, products)

## ------ tkinter ------

count_time = DEFAULT_TIME_OUT

## only for setup tkinter and frames
def screen_tk(products: GPU_.GPU):
    root = Tk()
    # root.geometry('500x200')
    root.title('GPU Price')
    main_frame = Frame(root)
    
    last_sent = '00/00 00:00'
    count_time = DEFAULT_TIME_OUT
    
    #status frame, at the top
    status_frame = Frame(main_frame)
    sent_label = Label(status_frame)
    time_label = Label(status_frame)
    count_label = Label(status_frame)
    setting_btn = Button(status_frame, text="Setting", relief=GROOVE, height = 1, width=10, command=lambda: setting_windows(root))
    sent_label.grid(row=0, column=0, padx=20)
    time_label.grid(row=0, column=1, padx=20)
    count_label.grid(row=0, column=2, padx=20)
    setting_btn.grid(row=0, column=3, padx=20)
    frame_status(sent_label, time_label, count_label, last_sent, count_time)
    status_frame.grid(row=0, column=0, columnspan=2)
    
    #log frame, on the right
    log_frame = LabelFrame(main_frame, text='Log')
    log_text = []
    log_label = Label(log_frame, text='', width=50 ,anchor='nw')
    log_label.pack()
    frame_log(log_label, log_text)
    log_frame.grid(row=1, column=1, padx = 1, pady= 1, sticky="nsew")
    
    #price and stock frame, left and bottom
    current_price_frame = LabelFrame(main_frame, text='Current price')
    current_stock_frame = LabelFrame(main_frame, text='Lowest stock')
    current_price_frame.grid(row=1, column=0, padx = 1, pady= 1, sticky="nsew")
    current_stock_frame.grid(row=2, column=0, padx = 1, pady= 1, sticky="nsew", columnspan=2)
    clear_frame(current_price_frame)
    clear_frame(current_stock_frame)
    frame_price(current_price_frame, products)
    frame_stock(current_stock_frame, products)
    
    ## every frame update at this function
    def update_main_frame(count_time, last_sent, log_text):
        frame_status(sent_label, time_label, count_label, last_sent, count_time)
        if count_time == 0:
            count_time = DEFAULT_TIME_OUT
            changed, changed_text = Util.update_products(products)
            if changed:
                for text in changed_text:
                    with open('log.txt', 'a') as f:
                        f.write(datetime.now().strftime("%m/%d %H:%M") + " " + text + '\n')
                    log_text.append(datetime.now().strftime("%m/%d %H:%M") + " " + text)
                while len(log_text) > 10:
                    log_text.pop(0)
                frame_log(log_label, log_text)
                Util.update_json(products)
                temp = Util.send_email_at_goal(products, GPU_GOAL_PRICE)
                if temp: last_sent = datetime.now().strftime("%m/%d %H:%M")
                
                clear_frame(current_price_frame)
                clear_frame(current_stock_frame)
                frame_price(current_price_frame, products)
                frame_stock(current_stock_frame, products)
        count_time -= 1
        status_frame.after(1000, lambda: update_main_frame(count_time, last_sent, log_text))
            
    update_main_frame(count_time, last_sent, log_text)
    main_frame.pack(padx=10,pady=10)
    root.mainloop()
    
def setting_windows(root):
    rows = 0
    setting_win = Toplevel(root)
    setting_win.title('Setting')
    setting_win.geometry('300x500')
    
    time_title = Label(setting_win, text='Time interval: ')
    time_input = Entry(setting_win, width=10)
    time_input.insert(0, DEFAULT_TIME_OUT)
    time_title.grid(row=rows, column=0, padx=5, pady=5)
    time_input.grid(row=rows, column=1, padx=5, pady=5)
    rows += 1
    
    goal_label = Label(setting_win, text='Price Goal', font=("Arial", 10))
    goal_label.grid(row=rows, column=0, padx=5, pady=5)
    rows += 1
    _3090Ti_label = Label(setting_win, text='3090 Ti:')
    _3090Ti_label.grid(row=rows, column=0, padx=5, pady=5)
    _3090Ti_input = Entry(setting_win, width=10)
    _3090Ti_input.insert(0, GPU_GOAL_PRICE['3090 Ti'])
    _3090Ti_input.grid(row=rows, column=1, padx=5, pady=5)
    rows += 1
    _3090_label = Label(setting_win, text='3090:')
    _3090_label.grid(row=rows, column=0, padx=5, pady=5)
    _3090_input = Entry(setting_win, width=10)
    _3090_input.insert(0, GPU_GOAL_PRICE['3090'])
    _3090_input.grid(row=rows, column=1, padx=5, pady=5)
    rows += 1
    _3080Ti_label = Label(setting_win, text='3080 Ti:')
    _3080Ti_label.grid(row=rows, column=0, padx=5, pady=5)
    _3080Ti_input = Entry(setting_win, width=10)
    _3080Ti_input.insert(0, GPU_GOAL_PRICE['3080 Ti'])
    _3080Ti_input.grid(row=rows, column=1, padx=5, pady=5)
    rows += 1
    _3080_label = Label(setting_win, text='3080:')
    _3080_label.grid(row=rows, column=0, padx=5, pady=5)
    _3080_input = Entry(setting_win, width=10)
    _3080_input.insert(0, GPU_GOAL_PRICE['3080'])
    _3080_input.grid(row=rows, column=1, padx=5, pady=5)
    rows += 1
    _3070Ti_label = Label(setting_win, text='3070 Ti:')
    _3070Ti_label.grid(row=rows, column=0, padx=5, pady=5)
    _3070Ti_input = Entry(setting_win, width=10)
    _3070Ti_input.insert(0, GPU_GOAL_PRICE['3070 Ti'])
    _3070Ti_input.grid(row=rows, column=1, padx=5, pady=5)
    rows += 1
    _3070_label = Label(setting_win, text='3070:')
    _3070_label.grid(row=rows, column=0, padx=5, pady=5)
    _3070_input = Entry(setting_win, width=10)
    _3070_input.insert(0, GPU_GOAL_PRICE['3070'])
    _3070_input.grid(row=rows, column=1, padx=5, pady=5)
    rows += 1
    _3060Ti_label = Label(setting_win, text='3060 Ti:')
    _3060Ti_label.grid(row=rows, column=0, padx=5, pady=5)
    _3060Ti_input = Entry(setting_win, width=10)
    _3060Ti_input.insert(0, GPU_GOAL_PRICE['3060 Ti'])
    _3060Ti_input.grid(row=rows, column=1, padx=5, pady=5)
    rows += 1
    _3060_label = Label(setting_win, text='3060:')
    _3060_label.grid(row=rows, column=0, padx=5, pady=5)
    _3060_input = Entry(setting_win, width=10)
    _3060_input.insert(0, GPU_GOAL_PRICE['3060'])
    _3060_input.grid(row=rows, column=1, padx=5, pady=5)
    rows += 1
    _3050_label = Label(setting_win, text='3050:')
    _3050_label.grid(row=rows, column=0, padx=5, pady=5)
    _3050_input = Entry(setting_win, width=10)
    _3050_input.insert(0, GPU_GOAL_PRICE['3050'])
    _3050_input.grid(row=rows, column=1, padx=5, pady=5)
    rows += 1
    
    def set_input():
        global DEFAULT_TIME_OUT
        global GPU_GOAL_PRICE
        try:
            DEFAULT_TIME_OUT = int(time_input.get())
            GPU_GOAL_PRICE['3090 Ti'] = float(_3090Ti_input.get())
            GPU_GOAL_PRICE['3090'] = float(_3090_input.get())
            GPU_GOAL_PRICE['3080 Ti'] = float(_3080Ti_input.get())
            GPU_GOAL_PRICE['3080'] = float(_3080_input.get())
            GPU_GOAL_PRICE['3070 Ti'] = float(_3070Ti_input.get())
            GPU_GOAL_PRICE['3070'] = float(_3070_input.get())
            GPU_GOAL_PRICE['3060 Ti'] = float(_3060Ti_input.get())
            GPU_GOAL_PRICE['3060'] = float(_3060_input.get())
            GPU_GOAL_PRICE['3050'] = float(_3050_input.get())
        except Exception as e:
            print(e)

    set_btn = Button(setting_win, text='Set', height=1, width=10, command=lambda: [set_input(), setting_win.destroy()])
    set_btn.grid(row=rows, column=0, padx=5, pady=5)
    Close_btn = Button(setting_win, text='Close', height=1, width=10, command=lambda: setting_win.destroy())
    Close_btn.grid(row=rows, column=1, padx=5, pady=5)

def frame_log(log_label: Label, log_text):
    resutl_text = ''
    for i in reversed(range(len(log_text))):
        resutl_text += log_text[i] + '\n'
    if len(resutl_text) == 0: resutl_text = 'Nothing'
    log_label.config(text=resutl_text)

def frame_status(sent_label: Label, time_label: Label, count_label: Label, last_sent, count_time):
    sent_label.config(text= 'Last email: ' + last_sent)
    time_label.config(text= 'Live time: ' + datetime.now().strftime('%H:%M:%S %p'))
    count_label.config(text= 'Next update: ' + str(count_time))

## pull data from products and put it to frame
def frame_price(frame, products: GPU_.GPU):
    rows, columns = 0, 0
    lowest_price, highest_price = Util.find_lowest_highest(products)
    for model in GPU_.GPU_MODELS:
        if highest_price[model] == 0.0:
            continue
        label = Label(frame, text=f'{highest_price[model]}', fg='red')
        label.grid(row=rows, column=columns)
        columns +=1
        label = Label(frame, text=f' <- ', fg='blue')
        label.grid(row=rows, column=columns)
        columns +=1
        label = Button(frame, text=f'{model}', fg='black', relief=GROOVE, height = 1, width=10)
        label.grid(row=rows, column=columns)
        columns +=1
        label = Label(frame, text=f' -> ', fg='blue')
        label.grid(row=rows, column=columns)
        columns +=1
        label = Label(frame, text=f'{lowest_price[model]}', fg='green')
        label.grid(row=rows, column=columns)
        columns +=1
        rows += 1
        columns = 0
    return

## pull data from products and put it to frame
def frame_stock(frame, products: GPU_.GPU):
    rows, columns = 1, 0
    Label(frame,  text='Model', fg='magenta').grid(row=0, column=0)
    Label(frame,  text='Price', fg='magenta').grid(row=0, column=1)
    Label(frame,  text='Stock', fg='magenta').grid(row=0, column=2)
    Label(frame,  text='Title', fg='magenta').grid(row=0, column=3)
    for model in GPU_.GPU_MODELS:
        found = False
        lowest = sys.float_info.max
        title = ""
        stock = 0
        link = ""
        for product in products:
            if product.get_model() == model and product.get_stock() > 0:
                found = True
                if product.get_price() < lowest:
                    lowest = product.get_price()
                    title = product.get_title()
                    stock = product.get_stock()
                    link = product.get_link()
        if found:
            temp_str = model
            if len(temp_str) < 7:
                temp_str = "   " + temp_str
            Label(frame, text=f'{temp_str}: ', fg='blue').grid(row=rows, column=columns)
            columns += 1
            Label(frame, text=f'{lowest} ', fg='green').grid(row=rows, column=columns)
            columns += 1
            Label(frame, text=f'({stock}) ', fg='green').grid(row=rows, column=columns)
            columns += 1
            Button(frame, text=f'{title}', fg='black', relief=GROOVE, height = 1, width=70, anchor='w', command=lambda n=link:webbrowser.open(n)).grid(row=rows, column=columns)
            columns += 1
            rows, columns = rows+1, 0
    return

def web_link(link):
    webbrowser.open(link)

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
