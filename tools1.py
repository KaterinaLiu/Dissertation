import datetime
import os
from tqdm import tqdm
import numpy as np

def calculate_volatility(price_dict_, span_, DATA_DIR):
    min_per = -100
    errorcompany = ['SCANA Corp', 'General Growth Properties Inc.']
    stock_volatility_3days = []
    text_all = []
    text_titles = os.listdir(DATA_DIR) #在指定目录 DATA_DIR 下获取所有文件的文件名列表。os.listdir() 函数返回指定目录中的所有文件和文件夹的名称，以字符串的形式存储在列表中。

    test_text_all = []
    test_stock_volatility_3days = []

    date = []
    company_ = []
    iter_ = 0
    for t in tqdm(text_titles): #遍历 text_titles 列表中的每个文件名，并将当前文件名存储在变量 t 中
        iter_ += 1
        cur_dir = os.path.join(DATA_DIR, t)#将目录路径 DATA_DIR 和当前文件名 t 拼接成完整的文件路径，并将结果存储在变量 cur_dir 中
        cur_dir = cur_dir + '\TextSequence.txt' #将文件名与 Text.txt 拼接在一起，形成最终的文件路径
        with open(cur_dir, 'r', encoding='utf-8') as f: #使用 open() 函数打开文件，指定读取模式 'r' 和编码方式为 'utf-8'，并将文件对象存储在变量 f 中
            text = f.read().strip().replace("<br />", " ") # strip() 方法去除开头和结尾的空白字符，然后使用 replace() 方法将 <br /> 替换为空格字符 " "，将处理后的文本存储在变量 text 中
        date_ = datetime.datetime.strptime(t[-8:], '%Y%m%d').strftime('%Y-%m-%d')#字符串 t 的后8个字符解析为日期，并将其格式化为 %Y-%m-%d 的日期字符串

        company = t[:-9]
        if company in errorcompany:
            continue
        else:
            stock_price = price_dict_[company]['Adj Close'] #从 price_dict_ 中获取相应公司的 'Adj Close' 价格数据，将其赋值给 stock_price
            try:
                today_index = stock_price.index.get_loc(date_) #根据 date_ 找到 stock_price 中对应的索引位置，赋值给 today_index
            except KeyError:
                try:
                    today_index = stock_price.index.get_loc(
                        (datetime.datetime.strptime(date_, '%Y-%m-%d') - datetime.timedelta(1)).strftime('%Y-%m-%d'))
                except KeyError:
                    try:
                        today_index = stock_price.index.get_loc(
                            (datetime.datetime.strptime(date_, '%Y-%m-%d') - datetime.timedelta(2)).strftime(
                                '%Y-%m-%d'))
                    except KeyError:
                        try:
                            today_index = stock_price.index.get_loc(
                                (datetime.datetime.strptime(date_, '%Y-%m-%d') - datetime.timedelta(3)).strftime(
                                    '%Y-%m-%d'))#如果找不到对应的索引位置，则尝试以前一天、前两天、前三天的日期进行查找，直到找到为止。
                        except:
                            print('Error Company: ' + str(company) + 'Date: ' + date_)
                            pass
                            continue

            today_data = stock_price.iloc[today_index] #将索引位置 today_index 对应的股票价格赋值给 today_data，表示今日股票价格。
            try:
                following_nday_price = stock_price.iloc[stock_price.index.get_loc(
                        (stock_price.index[today_index] + datetime.timedelta(span_)).strftime('%Y-%m-%d'))]#尝试以 today_index 对应的日期加上 span_ 天的日期作为目标日期，从 stock_price 中找到对应的股票价格。
            except KeyError:
                try:
                    following_nday_price = stock_price.iloc[stock_price.index.get_loc(
                        (stock_price.index[today_index] + datetime.timedelta(span_+1)).strftime('%Y-%m-%d'))]
                except KeyError:
                    try:
                        following_nday_price = stock_price.iloc[stock_price.index.get_loc(
                            (stock_price.index[today_index] + datetime.timedelta(span_+2)).strftime('%Y-%m-%d'))]
                    except KeyError:
                        try:
                            following_nday_price = stock_price.iloc[stock_price.index.get_loc(
                                (stock_price.index[today_index] + datetime.timedelta(span_+3)).strftime('%Y-%m-%d'))]
                        except:
                            print('Error following date: ' + str(company) + 'Date: ' + date_)
                            pass
                            continue

            # print(len(following_nday_data))
            if following_nday_price and today_data:
                log_diff = float(np.log(following_nday_price-today_data/today_data))#calculate stocks' volatility
                volatility = np.abs(log_diff)
                persent = volatility*100 # movement persentage
                if 104.28465722801789  > persent > min_per: #min_per=-100
                    min_per = persent
                # print(str(persent)+"%")
                if volatility == 80.39968485780167:
                    print(date_,str(company))
            else:
                print("Date Error, following_nday_price or today_data is null")
                continue
            if text == "": #处理后的文本
                print("Error File: no content", t)
                continue
            text_all.append(text)
            stock_volatility_3days.append(volatility)
            date.append(date_)
            company_.append(str(company))
            # if iter_ > 450:
            #     print('Company: ' + str(company) + 'Date: ' + date_)
            #     test_text_all.append(text)
            #     test_stock_movement_3days.append(movement)
    # print(len(test_text_all), len(test_stock_movement_3days))
    print(min_per)
    return stock_volatility_3days, text_all, date, company_

