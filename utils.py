
from itertools import chain
import cv2
import os
from xpinyin import Pinyin as p
import pyautogui
import os
import time
import csv

def checkMatch(coords, picName = ''):
    
    if coords == None:
        #print(f"找不到图片{picName}")
        return True
    
    else: return False
    
    
# abort
def findKeyboardInput(word):
    keyboardInput = p().get_pinyin(word,'')
    return keyboardInput
    
    
# abort
def checkVideo(ignore_items,x,y,nav_y):
    '''
    跳过视频,不获取小红书中的视频,只要文章,视频会使寻找退出按钮的图像不易定位
    '''
    if y-nav_y<350:
        return True
    for i,j in ignore_items:
        if abs(i-x)<=100 and y-j>0 and y-j<350:
            return True
        
    return False
#findKeyboardInput("代餐")

# abort
def getVideoIcon(cfg):
    
    video_icon = []
    MAX_VIDEO_ICON = cfg['MAX_VIDEO_ICON']
    for i in range(1,MAX_VIDEO_ICON):
        if os.path.exists(f'./image_folder/video{i}.png'):
            video_icon.append(pyautogui.locateAllOnScreen(f'./image_folder/video{i}.png',confidence = 0.6))
        else:
            break
        
    video_icon = chain(*video_icon)
    return video_icon

# abort
def getVideoReturnIcon(cfg):
    
    video_return = []
    
    MAX_RETURN_ICON = cfg['MAX_RETURN_ICON']
    for i in range(1,MAX_RETURN_ICON):
        if os.path.exists(f'./image_folder/video_return/return{i}.png'):
            video_return.append(pyautogui.locateAllOnScreen(f'./image_folder/video_return/return{i}.png',confidence = 0.6))
        else:
            break
    
    video_return = chain(*video_return)
    return video_return
        
        
# abort
def checkVideoReturn():
    coords = pyautogui.locateOnScreen('./image_folder/search.png',confidence = 0.8)
    return not checkMatch(coords)


def leftClick(image_name,interval=0.5,stay_interval = 0):
    #print(f'matching icon {image_name}')
    coords = pyautogui.locateOnScreen(image_name,confidence = 0.8)
    if checkMatch(coords):
        print('------------------------\n\n')
        print('三种原因异常:')
        print(f'1. 匹配图标{image_name}失败,请检查是否打开fiddler\n')
        print(f'2. 匹配图标{image_name}失败,请检查fiddler是否上方有黄色警示条,解决方式见README\n')
        print(f'3. 由于图标显示问题造成匹配失败,请查找{image_name}路径的图片,截取您电脑端对应的图标,替换对应图标\n\n')
        print('------------------------\n')
        exit(0)
    x,y=pyautogui.center(coords)
    if stay_interval!=0:
        pyautogui.moveTo(x,y)
        time.sleep(stay_interval)
    pyautogui.click(x,y,button='left')
    time.sleep(interval)
    
def saveArticles(word,articles):
    
    # txt+csv
    txt_file = open(f'./result/{word}文章内容.txt','w',encoding='utf-8')
    csv_file = open(f'./result/{word}文章内容.csv','w',encoding='utf-8',newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["url","content"])
    
    print('writing ...')
    for data in articles:
        #txt_file.write(data['url']+'\n')
        txt_file.write(data['content']+'\n')
        csv_writer.writerow([data['url'],data['content']])
    
    txt_file.close()
    csv_file.close()
    
    print(f'./result/{word}文章内容.csv 成功保存')
    print(f'./result/{word}文章内容.txt 成功保存')
    

def PictureResize(scale_before,scale_after):
    '''
    different computer screens have different scales, different size of screenshots didn't match
    well, do picture resize for picture match in the future program
    
    '''
    rate = scale_before/scale_after
    
    for root,_,files in os.walk("image_folder"):
        for file_name in files:
            image_path = os.path.join(root,file_name)
            image = cv2.imread(image_path)
            H,W,C = image.shape
            dim = (int(W/rate),int(H/rate))
            new_image = cv2.resize(image,dim)
            cv2.imwrite(image_path,new_image)
            print(f'changing image {image_path} from ({W} , {H}) -> {dim}')
            