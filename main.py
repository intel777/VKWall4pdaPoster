import vk, requests, json, requests as r
from grab import Grab

token=''
groupid = ''

g = Grab()
news = input("Введите ссылку: ")
print("Получение данных...")
g.go(news)
headline = g.doc.select('//span[@itemprop="headline"]').text()
content = g.doc.select('//div[@class="content-box"]//meta/@content').text()
imgurl = g.doc.select('//div[@class="photo"]//img/@src').text()

print("Получение изображения...")
pic = requests.get(imgurl)
picname = "postpic.jpg"
out = open('{}'.format(picname), "wb")
out.write(pic.content)
out.close()
str(content)
str(headline)
msg = headline + ". \n" + "\n" + content

print("Логин VK...")
session = vk.AuthSession(access_token=token)
api = vk.API(session)

print("Выгрузка изображения...")
upload = api.photos.getWallUploadServer(group_id=groupid)
files = {'photo': ('{}'.format(picname), open(r'{}'.format(picname), 'rb'))}
url = upload['upload_url']
data={"aid":upload['aid'],
      "mid":upload['mid']
      }
resp = r.post(url, data, files=files)
response = json.loads(resp.text)

print('Сохранение изображения...')
method_url = 'https://api.vk.com/method/photos.saveWallPhoto?'
data = dict(access_token=token, gid=groupid, photo=response['photo'], hash=response['hash'], server=response['server'])
response = requests.post(method_url, data)
result = json.loads(response.text)['response'][0]['id']
api.wall.post(owner_id="-{}".format(groupid), message=msg, from_group=1, signed=1, attachment=result)
print('Готово!')
