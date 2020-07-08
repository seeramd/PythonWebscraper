import tkinter
from bs4 import BeautifulSoup
from time import time
from datetime import datetime
from requests import get
from csv import writer
import matplotlib.pyplot as plt
import psycopg2

class MyLoop():
    def __init__(self, root, interval=1):
        self.aboutToQuit = False
        self.root = root
        self.time_x = []
        self.temp_y = []
        self.interval = interval
        self.root.bind("<space>", self.switch)
        self.root.bind("<Escape>", self.exit) 
    
        self.data_collection()

        self.old_epoch = time()
        while not self.aboutToQuit:
            self.root.update() # always process new events

            if (time() - self.old_epoch) >= self.interval:
                self.data_collection()
                self.old_epoch = time()

    def switch(self, event):
            self.plot_print()
         
    def plot_print(self,bool=False):
        print('Generating plot...')
        x = [i*self.interval for i in range(len(self.time_x))]
        plt.plot(x, self.temp_y)
        plt.show(block=bool)

    def data_collection(self):
        self.time_x += [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        self.temp_webscraper(self.temp_y)
        print(self.time_x[-1] + ' | ' + str(self.temp_y[-1]) + '°F')
        
    @staticmethod
    def temp_webscraper(temp_list):
        source = get("https://forecast.weather.gov/MapClick.php?x=98&y=198&site=okx&zmx=&zmy=&map_x=98&map_y=199").text
        soup = BeautifulSoup(source,'lxml')

        tempF = soup.find('p',class_="myforecast-current-lrg").text

        temp_list += [int(tempF.strip('°F'))]
               
    def exit(self, event):
        self.aboutToQuit = True
        print('Ending data collection...')
        self.root.destroy()

print("""

  _______                    ____                                        __ 
 |__   __|                  / ___|                                      /_ |
    | | ___ _ __ ___  _ __ | (___   ___ _ __ __ _ _ __   ___ _ __  __   _| |
    | |/ _ \ '_ ` _ \| '_ \ \___ \ / __| '__/ _` | '_ \ / _ \ '__| \ \ / / |
    | |  __/ | | | | | |_) | ___) | (__| | | (_| | |_) |  __/ |     \ V /| |
    |_|\___|_| |_| |_| .__/ /____/ \___|_|  \__,_| .__/ \___|_|      \_/ |_|
                     | |                         | |                        
                     |_|                         |_|                        

                     written by Timaeus
""")


run_count = 1
while True:
    print('Enter sampling interval (in seconds)')
    interval = float(input())
    
    if __name__ == "__main__":
        root = tkinter.Tk()

        run = MyLoop(root,interval)
        root.mainloop()

    run.plot_print(bool=True)

    data_points = len(run.time_x)
    time_elapsed = [i*interval for i in range(0,data_points)]

    with open('run'+str(run_count)+'.csv','w',newline = '') as datafile:
        writer = writer(datafile)

        writer.writerow(['RUN '+str(run_count)])
        writer.writerow(['TIME','TIME ELAPSED (s)','TEMPERATURE (°F)'])

        for i in range(data_points):
            writer.writerow([run.time_x[i],time_elapsed[i],run.temp_y[i]])

    print('Data saved to run' + str(run_count) + '.csv' + ' in home directory')

    query = """INSERT INTO tempscraper (time,fahr_temperature,location) VALUES """

    for i in range(data_points):
        query += "('{}',{},'{}'),".format(run.time_x[i],str(run.temp_y[i]),'New York City')
    query = query.strip(',') + ';'
    
    conn = psycopg2.connect("dbname={YOUR DATABASE NAME HERE} user={USER HERE} password = {PASSWORD HERE}")
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    print('Data stored in PostreSQL server')
    cur.close()
    conn.close()
    
    
    print('New run?')
    n = input()
    if n.lower() == 'yes' or n.lower() == 'y':
        run_count += 1
        continue
    else:
        break

