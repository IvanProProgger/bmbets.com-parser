import requests
from bs4 import BeautifulSoup
#url = 'https://bmbets.com/'
#req = requests.get(url)
#soup = BeautifulSoup(req.text, 'html.parser')
#a = soup.find_all('li', 'highlight')
#print(a)

#with open('parsing.html') as file:
#    src = file.read()
#soup = BeautifulSoup(src, 'html.parser')
start_link = 'https://bmbets.com/'
category = input().replace(' ', '-').lower()+'/'
country = input().replace(' ', '-').lower()+'/'
division = input().replace(' ', '-').lower()+'/'
#parse_link = start_link + category + country + division
#req = requests.get(parse_link)
#print(req)
#soup = BeautifulSoup(req.text, 'html.parser')
#print(soup)
table_coef = {}
a = []
b = []
c = []
parse_link = start_link + category + country + division
req = requests.get(parse_link)
soup = BeautifulSoup(req.text, 'html.parser')

for link in soup.find_all('td', class_='players-name-col'):
    a.append(link.text.strip().replace('\n\n\n\n', ' vs '))
for link in soup.find_all('td', class_='odds-col4'):
    b.append(link.text.strip().replace("B's", ' ')[1:])
count = int(len(b) / len(a))
while len(b) > 0:
    c.append(', '.join(b[:count]))
    b = b[count:]
x = zip(a,c)
print(*x, sep = '\n')

