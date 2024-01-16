#pip install pandas bs4 requests

#import thư viện 
import requests
from bs4 import BeautifulSoup
import pandas as pd

#list lưu thông tin riêng của xe
carName = []
price = []
year = []
style = []
stat = []
xx = []
km = []
tt = []
hs = []
nl = []

dict = {'Tên xe': carName, 'Giá': price, 'Năm sản xuất': year, 'Kiểu dáng': style,'Tình trạng': stat, 'Xuất xứ': xx, 
        'Số km đã đi': km, 'Tỉnh thành': tt, 'Hộp số': hs, 'Nhiên liệu': nl}  

#lưu danh sách link xe
listCarLinks = []
baseUrl = 'https://oto.com.vn/'

#vòng lặp lấy thông tin link xe và lưu vào biến listCarLinks
for i in range(0,1):
    try:
        response = requests.get('https://oto.com.vn/mua-ban-xe-cu-da-qua-su-dung/p' + str(i))
        soup = BeautifulSoup(response.content, "html.parser")

        links = soup.select('.item-car > .photo > a')
        for link in links:
            if link['href']:
                listCarLinks.append(link['href'])
        
        print('done: ' + str(i), response.status_code)
    except:
        pass

#hàm truy cập vào link xe trong listCarLinks, lấy thông tin tương ứng
def processingData(link: str):
    try:
        link = baseUrl + link
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")

        

        TenXe = soup.select_one('.group-title-detail > .title-detail').get_text().strip().replace('  ', ' ')
        Gia = soup.select_one('.price').get_text().strip().replace('  ', ' ')

        carInfos = soup.select('.box-info-detail > .list-info > li')
        carInforTitles = ['Năm SX', 'Kiểu dáng', 'Tình trạng', 'Xuất xứ', 'Km đã đi', 'Tỉnh thành', 'Hộp số', 'Nhiên liệu']

        carName.append(TenXe)
        price.append(Gia)
        year.append('')
        style.append('')
        stat.append('')
        xx.append('')
        km.append('')
        tt.append('')
        hs.append('')
        nl.append('')

        current_page = 0
        for carInfo in carInfos:
            for carInforTitle in carInforTitles:
                if carInforTitle in carInfo.get_text().strip().replace('  ', ' '):
                    value = carInfo.get_text().replace(carInforTitle, '').strip()

                    if carInforTitle == 'Năm SX':
                        year[-1] = value
                    elif carInforTitle == 'Kiểu dáng':
                        style[-1] = value
                    elif carInforTitle == 'Tình trạng':
                        stat[-1] = value
                    elif carInforTitle == 'Xuất xứ':
                        xx[-1] = value
                    elif carInforTitle == 'Km đã đi':
                        km[-1] = value
                    elif carInforTitle == 'Tỉnh thành':
                        tt[-1] = value
                    elif carInforTitle == 'Hộp số':
                        hs[-1] = value
                    elif carInforTitle == 'Nhiên liệu':
                        nl[-1] = value

                    current_page += 1
    except Exception as e:
        print(f"An error occurred for link {link}: {e}")


#sử dụng hàm
for link in listCarLinks:
    processingData(link)
  #lưu vào dataframe để xử lý
df = pd.DataFrame(dict)


df.to_csv('data-1.csv', encoding='utf-8-sig',index=False)