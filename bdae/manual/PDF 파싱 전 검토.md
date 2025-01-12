###
```
inputfile = r'I:\PDFGen.pdf'
import pdfplumber

pdf = pdfplumber.open(inputfile)
pages = pdf.pages
print(pages)

arrs = []
for i in range(len(pages)):
    txt = pages[i].extract_text()
    txt_arr = txt.split('\n')
    
    for a in txt_arr:
        a_arr = a.split(' ')
        arrs.append(a_arr)
    

arrs


from openpyxl import Workbook
from openpyxl.utils import get_column_letter

wb = Workbook()
dest_filename = r'I:\empty_book.xlsx' #생성할 엑셀 파일 이름
print(dest_filename)
ws1 = wb.active
ws1.title = "range names"
# 1번 결과 이미지 참고
for row in range(len(params)):    # row 1 ~ 39 까지 반복하여
    print(params[row])
    ws1.append(params[row])
wb.save(dest_filename)
wb.close()


```
