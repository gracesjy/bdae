## Basic Concept
```
from spire.doc import *
from spire.doc.common import *

# Create an instance of Document
doc = Document()

input_path = r'G:\DeepLearning\DocuAutomation.docx'
# Load a Word document
doc.LoadFromFile(input_path)

# Loop through the sections
all_data = []

# 한번 뽑아 보는 것
mbr = 'E2BC05'
print ('Doucment Section Count : %d' %  doc.Sections.Count)
local_row_idx = 0
paragraphNumbering = ''
prevParagraphNumbering = ''
for i in range(doc.Sections.Count):
    section = doc.Sections.get_Item(i)
    for j in range(section.Paragraphs.Count):
        paragraph = section.Paragraphs.get_Item(j)
        numbering = paragraph.ListText
        if len(numbering) > 0:
            print('>>> ' + paragraph.ListText + ' ' + paragraph.Text)
        else:
            continue

        #if numbering.find('3.1') < 0:
        #    continue

        local_row_idx = 0
        tables = section.Tables
        print ('table count : %d' % tables.Count)
        
        
        for i in range(0, tables.Count):
            # Get a table
            
            table = tables.get_Item(i)
            # Initialize a string to store the table data
            tableData = ''
            # Loop through the rows of the table
            #print('table row count : %d' %  table.Rows.Count)
            step_no = ''

            one_row = []

            for j in range(0, table.Rows.Count):
                # Loop through the cells of the row
                col_idx = 0

                #print('cell count : %d' % table.Rows.get_Item(j).Cells.Count)
                
                # 여기에서 cell 의 one row 가 완성된다.
                one_row.append(mbr)
                one_row.append(numbering)

                
                column_values = []
                
                for k in range(0, table.Rows.get_Item(j).Cells.Count):

                    # Get a cell
                    cell = table.Rows.get_Item(j).Cells.get_Item(k)
                    # Get the text in the cell
                    cellText = ''
                    
                    for para in range(cell.Paragraphs.Count):
                        paragraphText = cell.Paragraphs.get_Item(para).Text.strip()
                        if para == 0:
                            paragraphNumbering = cell.Paragraphs.get_Item(para).ListText.strip()
                            #print('Numbering : ' + paragraphNumbering)
                            if len(paragraphNumbering) > 0:
                                local_row_idx = 0
                                prevParagraphNumbering = paragraphNumbering
                        cellText += (paragraphText + ' ')

                    cellText = cellText.strip()
                    #print('row idx : %d, col_idx : %d, cellText : >%s<' % (local_row_idx, col_idx, cellText))
                    column_values.append(cellText)
                    col_idx = col_idx + 1
                
                
                one_row.append(str(local_row_idx))
                #print('<<< Numbering : ' + prevParagraphNumbering)
                one_row.append(prevParagraphNumbering)
                for a in column_values:
                    one_row.append(a)
                
                print(one_row)
                if len(one_row) > 0:
                    all_data.append(one_row)
                    local_row_idx = local_row_idx + 1
                    one_row = []


print(all_data)            
doc.Close()
```

LOGS
```
>>> 3. ATLAS is Good
>>> 3.1. Ddd
table count : 1
['E2BC05', '3.1.', '0', '', 'Step-No', 'Procedures and Description', 'Author', 'Confirmer']
['E2BC05', '3.1.', '0', '3.1.1.', '', '[SOP-2000] 이것은 Instruction 이다.  연장된 Instruction 이다. 아래 표에 나온다.', '', '']
['E2BC05', '3.1.', '1', '3.1.1.', '', 'Bioreactor', '', '']
['E2BC05', '3.1.', '2', '3.1.1.', '', 'Temperature', '2002', '', '']
['E2BC05', '3.1.', '3', '3.1.1.', '', 'Pressure', '433', '', '']
['E2BC05', '3.1.', '4', '3.1.1.', '위에 문제가 있을 때에는 관리자에게 보고 한다.']
['E2BC05', '3.1.', '0', '3.1.2.', '', '', '', '']
['E2BC05', '3.1.', '0', '3.1.3.', '', '', '', '']
['E2BC05', '3.1.', '0', '3.1.4.', '', '', '', '']
['E2BC05', '3.1.', '0', '3.1.5.', '', '', '', '']
[['E2BC05', '3.1.', '0', '', 'Step-No', 'Procedures and Description', 'Author', 'Confirmer'],
['E2BC05', '3.1.', '0', '3.1.1.', '', '[SOP-2000] 이것은 Instruction 이다.  연장된 Instruction 이다. 아래 표에 나온다.', '', ''],
['E2BC05', '3.1.', '1', '3.1.1.', '', 'Bioreactor', '', ''],
['E2BC05', '3.1.', '2', '3.1.1.', '', 'Temperature', '2002', '', ''],
['E2BC05', '3.1.', '3', '3.1.1.', '', 'Pressure', '433', '', ''],
['E2BC05', '3.1.', '4', '3.1.1.', '위에 문제가 있을 때에는 관리자에게 보고 한다.'],
 ['E2BC05', '3.1.', '0', '3.1.2.', '', '', '', ''],
['E2BC05', '3.1.', '0', '3.1.3.', '', '', '', ''],
['E2BC05', '3.1.', '0', '3.1.4.', '', '', '', ''],
['E2BC05', '3.1.', '0', '3.1.5.', '', '', '', '']]
```
