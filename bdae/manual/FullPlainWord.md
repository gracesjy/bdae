### 워드 파일의 서식을 모두 없앴을 경우 
## 아래의 매크로 실행 시킬 것
```
Sub ConvertSelectAutoNumberToText()
 If ActiveDocument.Lists.Count > 0 Then
   Selection.Range.ListFormat.ConvertNumbersToText
Else
End If
End Sub

Sub ConvertAllAutoNumberToText()
If ActiveDocument.Lists.Count > 0 Then
    Dim lisAutoNumList As List
    For Each lisAutoNumList In ActiveDocument.Lists
     lisAutoNumList.ConvertNumbersToText
    Next
Else: End If

End Sub
```

## 아래는 소스이다.
```
import re
def major_numbering(data):
    if data == None:
        return None
        
    p2 = re.compile('^[0-9]+\.[\s]+(.+)')
    result = p2.match(data)
    
    if result == None:
        return None

    result = result.group()
    print(result)
    words = result.split('\t')
    # THIS is TOC check.
    if len(words) > 2:
        return None
    return words[0]

def minor_numbering(data):
    if data == None:
        return None
        
    p2 = re.compile('^[0-9]+\.[0-9]+\.[\s]+(.+)')
    result = p2.match(data)
    
    if result == None:
        return None

    result = result.group()
    words = result.split('\t')
    # THIS is TOC check.
    if len(words) > 2:
        return None
    return words[0]

def abnormal_numbering(data):
    p1 = re.compile('^[0-9]+\.')
    result1 = p1.match(data)
    print(result1)
    p2 = re.compile('^[0-9]+\.[0-9]+\.')
    result2 = p2.match(data)
    print(result2)
    p3 = re.compile('^[0-9]+\.[0-9]+\.[0-9]+\.')
    result3 = p3.match(data)
    print(result3)
    
    if result1 == None and result2 == None and result3 == None:
        return False
    else:
        return True

def subTables(tables):
    sub_one_row = []
    for i in range(0, tables.Count):
        # Get a table
        
        table = tables.get_Item(i)
        # Initialize a string to store the table data
        tableData = ''
        # Loop through the rows of the table
        #print('table row count : %d' %  table.Rows.Count)
        step_no = ''

        ### 이 위치가 Row 정의 위치임.
        one_row = []
        prev_column_values = None
        local_row_idx = 0
        for j in range(0, table.Rows.Count):
            # Loop through the cells of the row
            col_idx = 0

            #print('cell count : %d' % table.Rows.get_Item(j).Cells.Count)
            
            # 여기에서 cell 의 one row 가 완성된다.

            column_values = []

            # 헷깔리지 말자. 여기가 표의 컬럼들을 순차적으로 보여준다.
            table_columns = table.Rows.get_Item(j).Cells
            for k in range(0, table_columns.Count):

                # Get a cell (컬럼 하나씩 )
                cell = table_columns.get_Item(k)
                # Get the text in the cell
                cellText = ''
                # 하나의 컬럼 안에 있는 모든 문구들을 모두 합친다.
                for para in range(cell.Paragraphs.Count):
                    paragraphText = cell.Paragraphs.get_Item(para).Text.strip()
                    cellText += (paragraphText + '\n')    

                print(cellText)
                column_values.append(cellText)
            sub_one_row.append(column_values)
    print(sub_one_row)
    return sub_one_row


## 모두 Text 로 전환했을 때...
def get_part(doc, numbering_part, all_data, done_list):
    mbr = 'E2BC05'
    print ('Doucment Section Count : %d' %  doc.Sections.Count)
    local_row_idx = 0
    paragraphNumbering = ''
    prevParagraphNumbering = ''

    numbering = None
    # 구문 분리될 때 생겨나는 것이 Section
    for i in range(doc.Sections.Count):
        section = doc.Sections.get_Item(i)

        # 1., .. , 3.1, .. 그리고 모든 글자들을 포함 한다.
        for j in range(section.Paragraphs.Count):
            paragraph = section.Paragraphs.get_Item(j)
            # Style Mode Deleted.
            if paragraph.Text == None:
                continue;

            # 1., 2., 3., Major Numbering
            numbering1 = major_numbering(paragraph.Text)
            # 1.1, 1.2, ... , 3.1, 3.2, ...
            numbering2 = minor_numbering(paragraph.Text)
            
            print('=========> numbering ............. :' + str(numbering1) + ',' + str(numbering2))

            ## init
            if numbering == None:
                if numbering2 == None:
                    continue
                elif numbering2.find(numbering_part) >= 0:
                    numbering = numbering2
                else:
                    continue
            else:        
                if numbering.find(numbering_part) < 0:
                    if numbering2 == None:
                        continue
                    elif numbering2.find(numbering_part) >= 0:
                        numbering = numbering2
                    else:
                        continue
                
            
            if numbering in done_list:
                print (numbering + ' is in ..')
                continue;
            else:
                done_list.append(numbering)

            tables = section.Tables
            print ('table count : %d' % tables.Count)
            table_idx = 0
            for i in range(0, tables.Count):
                # Get a table
                
                table = tables.get_Item(i)
                # Initialize a string to store the table data
                tableData = ''
                # Loop through the rows of the table
                #print('table row count : %d' %  table.Rows.Count)
                step_no = ''

                ### 이 위치가 Row 정의 위치임.
                one_row = []
                prev_column_values = None
                local_row_idx = 0
                for j in range(0, table.Rows.Count):
                    # Loop through the cells of the row
                    col_idx = 0
    
                    #print('cell count : %d' % table.Rows.get_Item(j).Cells.Count)
                    
                    # 여기에서 cell 의 one row 가 완성된다.
                    one_row.append(mbr)
                    one_row.append(numbering)
    
                    column_values = []

                    # 헷깔리지 말자. 여기가 표의 컬럼들을 순차적으로 보여준다.
                    table_columns = table.Rows.get_Item(j).Cells
                    for k in range(0, table_columns.Count):
    
                        # Get a cell (컬럼 하나씩 )
                        cell = table_columns.get_Item(k)
                        # Get the text in the cell
                        cellText = ''


                        if cell.Tables.Count > 0:
                            subTables(cell.Tables)

                        # 하나의 컬럼 안에 있는 모든 문구들을 모두 합친다.
                        for para in range(cell.Paragraphs.Count):
                            paragraphText = cell.Paragraphs.get_Item(para).Text.strip()
                            
                            paragraphNumbering = cell.Paragraphs.get_Item(para).Text.strip()
                            print('K : ' + str(k) + ', Para : ' + str(para) + ' Numbering of ListText : ' + paragraphNumbering)

                            if k == 0 and para == 0:
                                print('paranum :<' + paragraphNumbering + '>,<' + numbering.split(' ')[0] +'>')
                                if paragraphNumbering.find(numbering.split(' ')[0]) >= 0:
                                    print('ok find !')
                                
                            if k == 0 and para == 0 and len(paragraphNumbering) > 0 and paragraphNumbering.find(numbering) >= 0:
                                local_row_idx = 0
                                prevParagraphNumbering = paragraphNumbering

                            cellText += (paragraphText + ' ')
    
                        cellText = cellText.strip()
 
                        column_values.append(cellText)
                        col_idx = col_idx + 1
                    
                    # 같은 병합된 3.1.1(예) 내에서 몇 번째인지를 넣는다.
                    
                    one_row.append(str(local_row_idx))
                    # 보고라든지, 아예 없을 경우에는 table_idx 기반에서 숫자를 늘려서 보여준다.
                    if prevParagraphNumbering == '':
                        prevParagraphNumbering = numbering + str(table_idx)
                        table_idx = table_idx + 1
            
                    one_row.append(prevParagraphNumbering)
                    # 바로 직전의 row 에서 가져와야 할 것은 row 에서 병합이 이뤄졌을 때이다.
                    print('column values : ' + str(column_values))
                    print('prev column values : ' + str(prev_column_values))

                    if prev_column_values == None:
                        prev_column_values = column_values
                    else:
                        if len(prev_column_values) == len(column_values):
                            for a_idx in range(len(column_values)):
                                print('prev : ' + prev_column_values[a_idx] +', curr : ' + column_values[a_idx])
                                if column_values[a_idx] == '' and prev_column_values[a_idx] != '':
                                    column_values[a_idx] = prev_column_values[a_idx] 
                        else:
                            # 보고한다.
                            if len(column_values) == 1:
                                column_values = [prevParagraphNumbering, column_values[0]]
                                
                        prev_column_values = column_values    
                                    
                    # Bug 가능성  
                    
                    for column_idx in range(len(column_values)):
                        # 1.1 등이 들어 있는 경우에는 Skip 한다.
                        if column_idx == 0 and abnormal_numbering(column_values[0]) == True:
                            continue
                        else:
                            one_row.append(column_values[column_idx])
                    

                    
                    '''
                    # 숨겨진 번호가 그대로 찍히게 된다. 아래 1.1.1
                    # ['E2BC05', '3.1.', '1', '3.1.2.', '1.1.1.', 'Volume A = I2 step 7.2.3 in E2BC03', 'L1', '', '', ''],
                    for a in column_values:
                        
                        one_row.append(a)
                    '''

                    print(one_row)
                    if len(one_row) > 0:
                        if one_row not in all_data:
                            print('one_row : ' + str(one_row))
                            all_data.append(one_row)
                            local_row_idx = local_row_idx + 1
                            one_row = []


from spire.doc import *
from spire.doc.common import *
import re
# Create an instance of Document
doc = Document()

# DocuAutomation_PlainText2.docx, DocuAutomation_Only_Table_Plain.docx
input_path = r'G:\DeepLearning\DocuAutomation_PlainText2.docx'
# Load a Word document
doc.LoadFromFile(input_path)

# Loop through the sections
all_data = []
p1 = re.compile('^[0-9]+\.*')
p = re.compile('^[0-9]+\.[0-9]+\.*')
# 한번 뽑아 보는 것
mbr = 'E2BC05'
print ('Doucment Section Count : %d' %  doc.Sections.Count)
local_row_idx = 0
paragraphNumbering = ''
prevParagraphNumbering = ''
done_list = []
numbering_part = '3.1'
get_part(doc, numbering_part, all_data, done_list)
numbering_part = '3.2'
get_part(doc, numbering_part, all_data, done_list)
print('---------------------------------')
print(all_data)            
doc.Close()
```
