# -*-codeing = utf-8 -*-
# @Time : 2020/12/30
# @Author : 山与河　qq 2900180755
# @FIle ： bicoin.py
# @Software : PyCharm
import requests
import  json
import time
import threading
import argparse
import multiprocessing

class Td:
    def __init__(self,cycle='',type=''):
        self.cycle = cycle
        self.type = type
    # 发送提示`
    def news(self,title, text):
        try:
            url = 'https://sc.ftqq.com/***.send?text=' + title + '&desp=' + text
            request = requests.get(url=url).json()
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())), '  ',json.loads('"%s"' % request))
            return json.loads('"%s"' % request)
        except Exception as a:
            print(a)
    # 获取行情
    def bi_data(self):
        try:
            close_list = []
            request = requests.get(
                url='https://api.hadax.com/market/history/kline?period='+self.cycle+'&size=17&symbol='+self.type+'usdt').json()
            for close in request['data']:
                close_list.append(close['close'])
            close_list.reverse()
            return close_list
        except Exception as a:
            print(a)

    # 买入td计算
    def td_purchase(self,close_list):
        front = 0
        after = 4
        i = 1
        td_len = 0
        td_num_set = []
        while i <= 13:
            if int(close_list[after]) <= int(close_list[front]):
                td_len += 1
                td_num_set.append(str(td_len))
            else:
                td_len = 0
                td_num_set.append(str(td_len))
            front += 1
            after += 1
            i += 1
        td_num_str = '-'.join(td_num_set)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), '  ',self.type,self.cycle,'买', td_num_str,'close',close_list[16])
        if td_len == 9 or td_len == 13:
            return td_len
    # 卖出td计算
    def td_out(self,close_list):
        front = 0
        after = 4
        i = 1
        td_len = 0
        td_num_set = []
        while i <= 13:
            if int(close_list[after]) >= int(close_list[front]):
                td_len += 1
                td_num_set.append(str(td_len))
            else:
                td_len = 0
                td_num_set.append(str(td_len))
            front += 1
            after += 1
            i += 1
            td_num_str = '-'.join(td_num_set)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), '  ',self.type,self.cycle,'卖',td_num_str,'close',close_list[16])
        if td_len == 9 or td_len == 13:
            return td_len
    # 监控计算
    def function(self,cycle,type):
        td_class = Td(cycle,type)
        data_list = td_class.bi_data()
        td_num = td_class.td_purchase(data_list)
        if td_num != None:
            text = type +' '+cycle+ ' --- ' + '买入' + str(td_num)+' close '+ str(data_list[16])
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),'  ',text)
            td_class.news(title=type, text=text)
        td_num = td_class.td_out(data_list)
        if td_num != None:
            text = type + ' '+cycle+ ' --- ' + '卖出' + str(td_num) +' close '+ str(data_list[16])
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),'  ',text)
            td_class.news(title=type, text=text)


    def time_set(self,type):
        td_class = Td()
        ts = time.strftime("%S")  # 获取 1min
        if ts == '55':
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            min1_thread = threading.Thread(target=td_class.function,args=('1min',type),daemon=True)
            min1_thread.start()
        ts = time.strftime("%M%S")  # 获取 5 min
        dc = ['0000', '0500', '1000', '1500', '2000', '2500', '3000', '3500', '4000', '4500', '5000', '5500']
        if ts in dc:
            min5_thread = threading.Thread(target=td_class.function,args=('5min',type),daemon=True)
            min5_thread.start()
        ts = time.strftime("%M%S")  # 获取 15 min
        dc = ['0000', '1500', '3000', '4500']
        if ts in dc:
            min15_thread = threading.Thread(target=td_class.function,args=('15min',type),daemon=True)
            min15_thread.start()
        ts = time.strftime("%M%S")  # 获取 30 min
        dc = ['0000', '3000']
        if ts in dc:
            min30_thread = threading.Thread(target=td_class.function, args=('30min', type),daemon=True)
            min30_thread.start()
        ts = time.strftime("%H%M%S")  # 获取 1 hour
        dc = ['000000', '100000', '200000', '300000', '400000', '500000', '600000', '700000', '800000', '900000', '100000', '110000', '120000', '130000', '140000', '150000', '160000', '170000', '180000', '190000','200000', '210000', '220000', '230000', '240000']
        if ts in dc:
            hour1_thread = threading.Thread(target=td_class.function, args=('1hour', type),daemon=True)
            hour1_thread.start()
        ts = time.strftime("%H%M%S")  # 获取 4 hour
        dc = ['035000', '085000', '115000', '155000', '195000', '235000']
        if ts in dc:
            hour4_thread = threading.Thread(target=td_class.function, args=('4hour', type),daemon=True)
            hour4_thread.start()
        ts = time.strftime("%H%M%S")  # 获取 1 day
        dc = ['235000']
        if ts in dc:
            day1_thread = threading.Thread(target=td_class.function, args=('1day', type),daemon=True)
            day1_thread.start()



if __name__ == '__main__':
    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', help='-t btc')
        args = parser.parse_args()
        if (args.t):
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), '  ','开始运行......')
            lock = threading.Lock()
            while True:
                lock.acquire()
                btc_class = Td()
                btc_process = threading.Thread(target=btc_class.time_set(type=args.t),daemon=True)
                btc_process.start()
                lock.release()
                time.sleep(1)

