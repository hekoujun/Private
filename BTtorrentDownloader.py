from selenium import webdriver
from pandas import Series
import threading
import time
import os
import stat
time_start=time.time()

dir1=r'‪C:\Users\KONGYU\Downloads'

options = webdriver.ChromeOptions()
#options.add_argument('headless')配置Chrome为headless模式
options.add_argument('--proxy-server=http://127.0.0.1:8580')
driver = webdriver.Chrome(chrome_options=options)
handle=driver.current_window_handle

doc='http://www.sis001.com/forum/attachment.php?aid=3057657, \
http://www.sis001.com/forum/attachment.php?aid=3054972, \
http://www.sis001.com/forum/attachment.php?aid=3057701, \
http://www.sis001.com/forum/attachment.php?aid=3054840, \
http://www.sis001.com/forum/attachment.php?aid=3057631, \
http://www.sis001.com/forum/attachment.php?aid=3054856, \
http://www.sis001.com/forum/attachment.php?aid=3057711, \
http://www.sis001.com/forum/attachment.php?aid=3054842, \
http://www.sis001.com/forum/attachment.php?aid=3057676, \
http://www.sis001.com/forum/attachment.php?aid=3054915, \
http://www.sis001.com/forum/attachment.php?aid=3057616, \
http://www.sis001.com/forum/attachment.php?aid=3055049'


def begin_end():
    list1=doc.split(',')
    site=Series(list1)

    f=lambda x: int(x[-7:])
    site=site.apply(f)

    begin_num,end_num=site.min(),site.max()
    return [begin_num,end_num]



def bttorrent_downloader(begin_end):
    if begin_end[0]*begin_end[1] ==0:
        pass
    else:
        for i in range(begin_end[0],begin_end[1]):
            driver.get('http://www.sis001.com/forum/attachment.php?aid=%s'%str(i))
            time.sleep(0.5)
            if i%35 == 0:
                handles = driver.window_handles
                time.sleep(0.5)
                for newhandle in handles:
                    if newhandle !=handle:
                        driver.switch_to_window(newhandle)
                        driver.close()

def main():
    beg_end=begin_end()
    bttorrent_downloader(beg_end)

def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):  
        for s in os.listdir(dir):
            #如果需要忽略某些文件夹，使用以下代码
            #if s == "xxx":
                #continue
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)  
    return fileList

def reselect(dir):
    list1=GetFileList(dir1, [])
    for i in range(len(list1)):
        if '_sd' in list1[i] or '1080p' in list1[i] or '88q.me' in list1[i]:
            os.chmod(list1[i], stat.S_IWRITE )
            os.remove(list1[i])
    

if __name__ =='__main__':
    main()
    driver.quit()
    reselect(dir1)


time_end=time.time()
delta=time_end-time_start
hh=(delta-delta%3600)/3600
mm=(delta%3600-(delta%3600)%60)/60
ss=(delta%3600)%60
print('程序用时%d小时%d分%d秒'%(hh,mm,ss))

