import re
import csv
import requests
from myData import datas
from myHeader import headers

# 打开文件
out = open('rate.csv', 'a', newline='', encoding='UTF-8')
csv_write = csv.writer(out, dialect='excel', )
csv_write.writerow(['username', 'time','content'])
# 标识评论页,评论计数器
pagePointer = 1
rateCount = 0
while 1:
    datas['currentPage'] = str(pagePointer)
    print("获取第" + str(pagePointer) + "页评论中......")
    res = requests.get(
        url="https://rate.tmall.com/list_detail_rate.htm",
        params=datas,
        headers=headers
    )
    # print(res.text)
    rateList = re.search(r'"rateList":\[(\{.+\})\]', res.text)
    if not rateList:
        print("第" + str(pagePointer) + "页没有评论了......")
        break
    rate = re.finditer(r'"rateDate":"(.+?)".*?"rateContent":"(.+?)".*?"displayUserNick":"(.+?)"', rateList.group(1))
    for i in rate:
        csv_write.writerow([
            i.group(3),
            i.group(1),
            i.group(2)
        ])
        rateCount += 1

    print("获取完成！")
    pagePointer += 1

print("共" + str(pagePointer) + "页、" + str(rateCount) + "条评论抓取完成")
