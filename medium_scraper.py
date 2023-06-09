import requests
from bs4 import BeautifulSoup

url = 'https://medium.com/'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

links = []
for div in soup.find_all('div', class_="hh y"):
    for link in div.find_all('a', class_="ax ay az ba bb bc bd be bf bg bh bi bj bk bl"):
        href = link.get('href')
        if href is not None and 'http' in href:
            links.append(href)
    

# Create a text file and write the links to it
with open('medium_links.txt', 'w') as file:
    for link in links:
        file.write(link + '\n')

print('Links saved to medium_links.txt file.')
