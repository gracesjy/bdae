### Beautiful Soup

```
import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')

data = []
tables = soup.findAll('table')
depth = []
for t in tables:
    rows = t.find_all('tr')
    found = False
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values

total_data = []
for x in data:
    if x in total_data:
        continue
    else:
        if len(x) > 0:
            ok = True
            for y in x:
                print('element : ' + y + '---> len : ' + str(len(y)))
                if len(y) > 40:
                    ok = False

            if ok == True:
                total_data.append(x)

total_data
```