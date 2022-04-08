from tkinter import *
from tkinter import messagebox
from datetime import datetime
from datetime import timedelta
from Util import GPU_GOAL_PRICE, DEFAULT_RECORD_NAME
import sys
import json
import webbrowser

from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

import mplcursors as mpc

import GPU_
import Util

DEFAULT_TIME_OUT = 60

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
    frame_log(log_frame, log_text)
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
                # display any changes in log frame
                for text in changed_text:
                    with open('log.txt', 'a') as f:
                        f.write(datetime.now().strftime("%m/%d %H:%M") + " " + text + '\n')
                    log_text.append(datetime.now().strftime("%m/%d %H:%M") + " " + text)
                while len(log_text) > 10:
                    log_text.pop(0)
                frame_log(log_frame, log_text)
                
                # update json file
                Util.update_json(products)
                Util.clear_json_file()
                
                #update price and stock frame
                clear_frame(current_price_frame)
                clear_frame(current_stock_frame)
                frame_price(current_price_frame, products)
                frame_stock(current_stock_frame, products)
                
            #send email, return True is the email is sent, and list of sent products
            temp, result_products = Util.send_email_at_goal(products)
            if temp: 
                for result in result_products:
                    messagebox.showwarning("Price Alert!", f"{result.get_brand()} {result.get_model()} {result.get_price()}")
                last_sent = datetime.now().strftime("%m/%d %H:%M")
        count_time -= 1
        status_frame.after(1000, lambda: update_main_frame(count_time, last_sent, log_text))
            
    update_main_frame(count_time, last_sent, log_text)
    main_frame.pack(padx=10,pady=10)
    root.mainloop()
    
def setting_windows(root):
    rows = 0
    setting_win = Toplevel(root)
    setting_win.title('Setting')
    # setting_win.geometry('250x410')
    
    time_title = Label(setting_win, text='Time interval(min 10):')
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
            if int(time_input.get()) >= 10:
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
    set_btn.grid(row=rows, column=0, padx=10, pady=10)
    Close_btn = Button(setting_win, text='Close', height=1, width=10, command=lambda: setting_win.destroy())
    Close_btn.grid(row=rows, column=1, padx=10, pady=10)

def frame_log(log_frame, log_text):
    clear_frame(log_frame)
    for i in reversed(range(len(log_text))):
        Label(log_frame, text=log_text[i], width=50, anchor='w').pack(anchor='sw', padx=5)
    if len(log_text) == 0:
        Label(log_frame, text='Nothing', width=50, anchor='w').pack(anchor="sw", padx=5)

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
        label = Button(frame, text=f'{model}', fg='black', relief=GROOVE, command=lambda m=model: plotGraphFromFile(frame, "model", m) ,height = 1, width=10)
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

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def plotGraphFromFile(root, selecter: str, name: str):
    data_price_dic = {}
    data_stock_dic = {}
    data_date = []
    data_price = []
    data_stock = []
    
    with open(DEFAULT_RECORD_NAME, "r") as f:
        datas = json.load(f)
    for data in datas:
        if (datas[data][selecter] == name):
            for dic in datas[data]['price_records']: # look for the price record
                for key in dic: #only runs once
                    date = datetime.strptime(key, "%m/%d/%Y %H:%M:%S")
                    date = date.replace(hour=0, minute=0, second=0)
                    if date in data_price_dic:
                        if float(data_price_dic[date]) > float(dic[key]):
                            data_price_dic[date] = dic[key]
                    else:
                        data_price_dic[date] = dic[key]
            for dic in datas[data]['stock_records']: # look for the stock record
                for key in dic: #only runs once
                    date = datetime.strptime(key, "%m/%d/%Y %H:%M:%S")
                    date = date.replace(hour=0, minute=0, second=0)
                    
                    if date in data_stock_dic:
                        if int(data_stock_dic[date]) < int(dic[key]):
                            data_stock_dic[date] = dic[key]
                    else:
                        data_stock_dic[date] = dic[key]
    
    for key in data_price_dic:
        data_date.append(key)
    for key in data_stock_dic:
        if key not in data_date:
            data_date.append(key)
            
    data_date.sort()
    for key in data_date:
        if key in data_price_dic:
            data_price.append(data_price_dic[key])
        else:
            i = 1
            while((key - timedelta(days=i)) not in data_price_dic and i < 30):
                i += 1
            if (key - timedelta(days=i)) in data_price_dic:
                data_price.append(data_price_dic[key - timedelta(days=i)])
            else:
                data_price.append(0)
            
        if key in data_stock_dic:
            data_stock.append(data_stock_dic[key])
        else:
            i = 1
            while((key - timedelta(days=i)) not in data_stock_dic and i < 30):
                i += 1
            if key - timedelta(days=i) in data_stock_dic:
                data_stock.append(data_stock_dic[key - timedelta(days=i)])
            else:
                data_stock.append(0)
    
    plt.style.use('seaborn')
    fig = plt.figure(figsize=(6, 4), dpi=100)
    ax1 = fig.add_subplot(111)
    
    line1, = ax1.plot_date(data_date, data_price, color='g', fmt='o-', label='Price')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    
    ax2 = ax1.twinx()
    line2, = ax2.plot_date(data_date, data_stock, color='b', fmt='o-', label='Stock')
    ax2.set_ylabel('Stock')
    
    plt.title('Price and Stock of ' + name)
    
    plt.gcf().autofmt_xdate()
    date_format = mpl_dates.DateFormatter('%b, %d')
    plt.gca().xaxis.set_major_formatter(date_format)
    
    plt.tight_layout()
    plt.legend((line1, line2), ('Price', 'Stock'), loc='upper left')
    plt.grid()
    mpc.cursor(hover=True)
    plt.close()
    
    main_frame = Toplevel(root)
    graph_frame = Frame(main_frame)
    chart = FigureCanvasTkAgg(fig, master=graph_frame)
    chart.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(chart, graph_frame)
    toolbar.update()
    chart._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
    graph_frame.pack(side=TOP, fill=BOTH, expand=1)
    Button(main_frame, text='Quit', font=("Arial", 10), command=main_frame.destroy).pack(side=TOP, fill=BOTH, expand=1)
    return None