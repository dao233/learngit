import requests
import json
import random
import time
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
url='http://product.mapi.dangdang.com/index.php?access-token=&product_id=25137790&time_code=9d4c2f34f3d12cae4a4a417cc210d993&client_version=8.9.2&action=get_product_comment_list&source_page=&union_id=537-468&timestamp=1538829465&permanent_id=20181005093219799766790870290696642&custSize=b&global_province_id=144&sort_type=1&product_medium=0&page_size=15&filter_type=1&udid=f8fb9028b237e39504f7b9b77524e916&main_product_id=&user_client=android&label_id=&page='
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

}
def getComments(url,page):
    url=url+str(page)
    r=requests.get(url=url,headers=headers)
    res=json.loads(r.text)
    result=res.get('review_list')
    #print(result)
    comments=[]
    for comment in result:
        comments.append(comment['content'])
        try:
            with open('comments.txt','a') as f:
                f.write(comment['content']+'\n')
        except:
            print('第'+str(page)+'页出错')
            continue
for i in range(1,100):
    time.sleep(random.choice([1,2,3]))
    getComments(url,i)