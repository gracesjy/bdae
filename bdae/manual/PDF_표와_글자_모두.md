### PDF 파일의 표와 글자 모두를 한꺼번에

```
import pdfplumber
inputfile = r'I:\GenerateDoc1.pdf'

pages = pdf.pages
for page in pages:
    print(page.extract_text())
    print('------------------------------')
    print(page.extract_tables())

```
