import os
import random
import requests
import subprocess

from PIL import Image
from aip import AipOcr
from io import BytesIO


config={
    '头脑王者':{
        'title':(80,500,1000,880),
        'answers':(80,960,1000,1720),
        'point':[
            (316,993,723,1078),
            (316,1174,723,1292),
            (316,1366,723,1469),
            (316,1570,723,1657),
        ]
    },
    '西瓜视频':{}
}

def get_screenshot():
    process=subprocess.Popen('adb shell screencap -p',shell=True,stdout=subprocess.PIPE)
    screenshot=process.stdout.read()

    screenshot=screenshot.replace(b'\r\n', b'\n')


    img_fb=BytesIO()
    img_fb.write(screenshot)
    img=Image.open(img_fb)
    title_img=img.crop((80,500,1000,880))
    answers_img=img.crop((80,960,1000,1720))

    new_img=Image.new('RGBA',(920,1140))
    new_img.paste(title_img,(0,0,920,380))
    new_img.paste(answers_img,(0,380,920,1140))

    new_img_fb=BytesIO()
    new_img.save(new_img_fb,'png')
    #with open('test.png','wb') as f:
    #    f.write(new_img_fb.getvalue())
    return new_img_fb
def get_word_by_image(img):
    APPID = '11788835'

    APIKey = 'tzZW1S0Ug3A5WhHCQP9RK9jT'
    SecretKey = 'TS9BAF7dIp4F7yDbVTd0qMXCUS6EjEB4'
    client = AipOcr(APPID, APIKey, SecretKey)
    res=client.basicGeneral(img)
    return res
def baidu(question,answer):
    url='https://www.baidu.com/s'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    data={
        'wd':question
    }
    res=requests.get(url=url,params=data,headers=headers)
    res.encoding=res.apparent_encoding
    html=res.text
    for i in range(len(answer)):
        answer[i]=(html.count(answer[i]),answer[i],i)
    answer.sort(reverse=True)
    return answer


def click(point):
    cmd='adb shell input swipe %s %s %s %s %s'%(
        point[0],
        point[1],
        point[0]+random.randint(0,3),
        point[1]+random.randint(0,3),
        200
    )
    os.system(cmd)
def run():
    print('准备答题')
    while True:
        input('请按回车键开始答题：')
        img=get_screenshot()
        info=get_word_by_image(img.getvalue())
        if info['words_result_num']<5:

            continue
        answers=[x['words'] for x in info['words_result'][-4:]]
        question=''.join([x['words'] for x in info['words_result'][:-4]])
        res=baidu(question,answers)
        print(question)
        print(res)
        print(config['头脑王者']['point'][res[0][2]])
        click(config['头脑王者']['point'][res[0][2]])
if __name__=='__main__':
    run()




