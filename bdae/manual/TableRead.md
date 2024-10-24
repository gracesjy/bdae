## Table Read Out

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
'''
for i in range(doc.Sections.Count):
    section = doc.Sections.get_Item(i)
    for j in range(section.Paragraphs.Count):
        paragraph = section.Paragraphs.get_Item(j)
        print(paragraph.Text)
'''        
for s in range(doc.Sections.Count):
    # Get a section
    section = doc.Sections.get_Item(s)
    paragraph = section.Paragraphs[i]
    print('>>> ' + paragraph.Text)
    # Get the tables in the section
    tables = section.Tables
    # Loop through the tables
    local_row_idx = 0
    for i in range(0, tables.Count):
        # Get a table
        table = tables.get_Item(i)
        # Initialize a string to store the table data
        tableData = ''
        # Loop through the rows of the table
        print('table row count : %d' %  table.Rows.Count)
        step_no = ''
    
        for j in range(0, table.Rows.Count):
            # Loop through the cells of the row
            col_idx = 0
            
            one_row = []
            print('cell count : %d' % table.Rows.get_Item(j).Cells.Count)

            # 여기에서 cell 의 one row 가 완성된다.

            for k in range(0, table.Rows.get_Item(j).Cells.Count):
                # Get a cell
                cell = table.Rows.get_Item(j).Cells.get_Item(k)
                # Get the text in the cell
                cellText = ''

                for para in range(cell.Paragraphs.Count):
                    paragraphText = cell.Paragraphs.get_Item(para).Text
                    cellText += (paragraphText + ' ')

                # 7.x 가 애초에 아니라면 제거
                if k == 0:
                    cellText = cellText.strip()
                    if cellText.find('3.') >= 0:
                        # only change
                        step_no = cellText
                        local_row_idx = 0
                    elif cellText == '':
                        cellText = step_no
            
                one_row.append(cellText)

                    
                print('col_idx : %d, cellText : %s' % (col_idx, cellText))
                if col_idx == 0 and cellText.find ('3.') >= 0:
                    step_no = cellText
                    one_row.append(local_row_idx)
                
                col_idx = col_idx + 1
                # Add the text to the string
                tableData += cellText
                if k < table.Rows.get_Item(j).Cells.Count - 1:
                    tableData += '\t' 



                
            if len(one_row) > 0 and one_row[0].find('3.') >= 0:
                all_data.append(one_row)
                local_row_idx = local_row_idx + 1

            # Add a new line
            tableData += '\n'
    
        # Save the table data to a text file
        print(tableData)
print(all_data)

doc.Close()
```
