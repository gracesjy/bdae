### 보정

```
inputfile = r'I:\PDFGen.pdf'
import pdfplumber
pdf = pdfplumber.open(inputfile)
pages = pdf.pages
print(pages)
```

다음에서 Conferdential 끼어 드는 것들 제거 한다.
그리고, 활용해서 1 Recipe Name 등을 모두 빼어내는 함수를 만든다.
```
arrs = []
for i in range(len(pages)):
    txt = pages[i].extract_text()
    txt_arr = txt.split('\n')
    bStart = False
    for j in range(len(txt_arr)):
        if txt_arr[j].lower().find('parameter') >= 0:
            bStart = True
            arrs.append(txt_arr[j])
            continue
        else:
            if bStart:
                arrs.append(txt_arr[j])
            else:
                continue
```

```
def fill_(data, lenx):
    one_row = []
    if len(data) == lenx:
        one_row.extend(data)
    else:
        for i in range(lenx - len(data)):
            one_row.append('')
        one_row.extend(data)
    return one_row
```

```
def fill_all(data_all):
    ret_arr = []
    lenx = len(data_all[0])
    for i in range(1, len(data_all), 1):
        xxx = fill_(data_all[i], lenx)
        print(xxx)
        ret_arr.append(xxx)
    return ret_arr
```


```
def merge_list(data):
    final_arr = []
    #print('merge list : ' + str(data))
    for i in range(len(data)):
        a = data[i]
        if i == 0:
            final_arr.extend(a)
            continue

        if len(final_arr) != len(a):
            continue
        for j in range(len(a)):
            #print(final_arr[j] + '\n' + a[j])
            final_arr[j] = final_arr[j] + '\n' + a[j] 
    return final_arr
```

```
def merge_list2(formula_, data):
    print('merge_list2 - formula_ : ' + str(formula_))
    print('merge_list2 - data : ' + str(data))
    total = []
    total.append(formula_)
    for x in data:
        total.append(x)

    #return_arr = merge_list(total)
    return_arr = merge_list_(total, 2)
    return return_arr
```

```
def merge_list_(data, shorten_length):
    ret_arr = []
    print(data)
    aa = []
    dict = {}
    for j in range(len(data)):
        a_data = data[j]
        
        if j in dict.keys():
            x = dict.get(j)
            
            loop = int(len(a_data)/shorten_length)
            print(loop)
            step = shorten_length
    
            print('entering ...')
            for i in range(0, loop):
                #print(a_data[i])
                a = a_data[i*step] + ' ' + a_data[i*step+1]
                print('-->' + a)
                aa.append(a)
                x[i] = x[i] + a
        else:
            loop = int(len(a_data)/shorten_length)
            print(loop)
            step = shorten_length

            aa = []
            print('entering ...')
            for i in range(0, loop):
                #print(a_data[i])
                a = a_data[i*step] + ' ' + a_data[i*step+1]
                print('-->' + a)
                aa.append(a)
                
            dict.setdefault(j, aa)

            

    #print(ret_arr)
    print(dict)
    ret_arr = []
    print('--------------')
    for a in dict.keys():
        x = dict.get(a)
        print(x)
        if len(ret_arr) == 0:
            ret_arr.append(x)
        else:
            for i in range(len(x)):
                ret_arr[0][i] = ret_arr[0][i] + ' ' + x[i]

    
    return ret_arr
```

```
def merge_list_x(header, data, shorten_length):
    ret_arr = []
    print(data)
    aa = []
    dict = {}
    dict.setdefault(0, header)
    
    for j in range(len(data)):
        a_data = data[j]
        
        if j+1 in dict.keys():
            x = dict.get(j+1)
            
            loop = int(len(a_data)/shorten_length)
            print(loop)
            step = shorten_length
    
            print('entering ...')
            for i in range(0, loop):
                #print(a_data[i])
                a = a_data[i*step] + ' ' + a_data[i*step+1]
                print('-->' + a)
                aa.append(a)
                x[i] = x[i] + a
        else:
            loop = int(len(a_data)/shorten_length)
            print(loop)
            step = shorten_length

            aa = []
            print('entering ...')
            for i in range(0, loop):
                #print(a_data[i])
                a = a_data[i*step] + ' ' + a_data[i*step+1]
                print('-->' + a)
                aa.append(a)
                
            dict.setdefault(j+1, aa)

            

    #print(ret_arr)
    print(dict)
    ret_arr = []
    print('--------------')
    for a in dict.keys():
        x = dict.get(a)
        print(x)
        if len(ret_arr) == 0:
            ret_arr.append(x)
        else:
            for i in range(len(x)):
                ret_arr[0][i] = ret_arr[0][i] + ' ' + x[i]

    
    return ret_arr[0]
```

```
header = ['CIP_5', 'CIP_6']
data = [['(CIP', '4023', '(CIP', '4023'], ['To', '1140)', 'To', '3455)']]
merge_list_x(header, data, len(header))

a = [['(CIP', '4023', '(CIP', '4023'], ['To', '1140)', 'To', '3455)'], ['KK', 'MM)', 'JJ', 'CC)']]
merge_list_(a, 2)


```

```
def merge_list3(formula_, data):
    print('merge_list2 - formula_ : ' + str(formula_))
    print('merge_list2 - data : ' + str(data))
    total = []
    total.append(formula_)
    for x in data:
        total.append(x)

    #return_arr = merge_list(total)
    return_arr = merge_list_(data, 2)
    return return_arr

```

```
def find_parameter_row(data):
    found = False
    loc = 0
    #print('find_parameter_row entering .. ' + str(data))
    for i in range(len(data)):
        if data[i].lower().find('parameter') >= 0: # formula 가 위치가 같은 위치 인가 확인
            found = True

        # 매우 중요하다.  위치를 잡는다. unit 다음 컬럼이 Formula 이다.
        if data[i].lower().find('eng') >= 0:
            loc = i + 1

        if data[i].find('□') >= 0:
            break
        
    return found, loc
```

```
def prepare_params(param_header, data):
    params = []
    params.append(param_header)
    yy = merge_list(fill_all(parameters_arr))
    if param_header[0].lower().find('parameter') >= 0 and yy[0].lower().find('value') >= 0:
        yy.insert(0, '')
    
    print('prepare_params >>>> ' + str(yy))
    params.append(yy)
    return params
```

```
def param_redef(params):
    
    # 아래와 같은 구조이다.
    # 'Parameter Default Eng. Formula',
    # 'Value Unit M9282 M888',
    # 'To To',
    # 'MMS AOS',
    
    redefined_params = []
    if len(params) > 2:
        param_len = len(params[0])
        formula_loc = 0
        for i in range(len(params[0])):
            if params[0][i].lower().find('formula') >= 0:
                formula_loc = i 
                break
        max_column = 0        
        if formula_loc > 0:
            for a in params:
                a_txt = ','.join(a)
                if a_txt.lower().find('parameter') >= 0:
                    continue
                if a_txt.lower().find('value') >= 0:
                    continue

                if max_column < len(a):
                    max_column = len(a)

        print('formula loc {}, no. of formula val {}'.format(formula_loc,max_column))

        # parameter line
        one_row = []
        # 파라미터 앞에 공란이면 one_row.append('')
        one_row.extend(params[0])
        for i in range(max_column):
            one_row.append('')

        redefined_params.append(one_row)
        # value, unit line
        one_row = []
        # one_row.append('') # parameter 가 같은 위치 이기 때문에 주석 처리, 다르다면 ..
        one_row.extend(params[1])
        for j in range(max_column):
            one_row.append('')
            
        redefined_params.append(one_row)

        # formula ..
        for i in range(2, len(params), 1):
            print('formalar val : ' + str(params[i]))
            one_row = []
            for j in range(formula_loc):
                one_row.append('')
                
            one_row.extend(params[i])
            redefined_params.append(one_row)

    return redefined_params

pars = [['Parameter', 'Default', 'Eng.', 'Formula'], ['Value', 'Unit', 'M9282', 'M888'], ['To', 'To'], ['MMS', 'AOS']]
xx = param_redef(pars)
xx
```

```
def merge_list_vertical(params):
    dic = {}
    return_arr = []
    param_final = []
    # para 줄과 unit (다음 줄)에 formula 값이 없을 때 !!
    for i in range(2):
        a_param = params[i]
        #print('original : ' + str(a_param))
        for j in range(len(a_param)):
            val = a_param[j]
            val = val.replace('\n','')
            #print('j th ' + str(j) + ',' + val)
            if j in dic.keys():
                x = dic.get(j)
                #print('before : ' + x + ', now : ' + val)
                x = x + '\n' + val
                x = x.replace('\n','')
                dic.update({j:x})
            else:
                dic.setdefault(j, val)

    for i in dic.keys():
        x = dic.get(i)
        x = x.replace('\n','')
        param_final.append(x)

    return_arr.append(param_final)
    param_final = []
    dic = {}            
    for i in range(2, len(params)):
        a_param = params[i]
        #print('original : ' + str(a_param))
        for j in range(len(a_param)):
            val = a_param[j]
            #print('j th ' + str(j) + ',' + val)
            if j in dic.keys():
                x = dic.get(j)
                #print('before : ' + x + ', now : ' + val)
                x = x + '\n' + val
                dic.update({j:x})
            else:
                dic.setdefault(j, val)

    for i in dic.keys():
        x = dic.get(i)
        x = x.replace('\n','')
        param_final.append(x)

    return_arr.append(param_final)

    return return_arr
```


```
before_arr = []
# parameter = 4 개
# 그러면 formula 가 있으므로 3개, '□' 포함하면 4개
# formmula 갯수는 2개라는 것을 추축할 수 있다.
ext_arr = []
params = []

parameters_arr = []
before_loc = 0
bParaWork = False

for i in range(len(arrs)):
    txt = arrs[i]
    txt_arr = txt.split(' ')
    found, loc = find_parameter_row(txt_arr)
    print('1) 원본 : ' + txt)
    if loc > 0:
        #print(txt_arr)
        #한 페이지에 2개 이상이 있을 때 앞의 것을 정리한다.
        print('2) parameter 문구 발견')
        if len(before_arr) > 0:
            params.append(before_arr)
        before_loc = loc
        print('\tformula location : ' + str(loc))
        print('\t' + str(txt_arr))
        parameters_arr.append(txt_arr)
        bParaWork = True
        # 새로 시작하는 것이다.
        before_arr = []
        ext_arr = []
        continue
        
    #if before_loc > 0 and txt_arr[0] != '□':
    #    parameters_arr.append(txt_arr)

    if txt_arr[0] == '□':
        print('3) □ 문구 발견')
        ## parameter 헤더를 정리하는 과정이다.
        if len(parameters_arr) > 0:
            print('4) parameter 정리 ' + str(parameters_arr))
            yy = prepare_params(parameters_arr[0], parameters_arr[1:])
            for aaa in yy:
                params.append(aaa)


            
            bParaWork = False   
            parameters_arr = []

            
        if len(before_arr) > 1 and len(ext_arr) > 0:
            print('4) parameter 붙어 있는 것들 Merge : ' + str(before_arr))
            # Formaula 위치는 unit 위치에서 전체 array 의 length 를 제거 한다.
            formula_loc = len(before_arr) - (before_loc + 1)
            print('.... formula loc ' + str(formula_loc))
            header = before_arr[:len(before_arr) - formula_loc]
            if len(header) == 0:
                #print('--- header ..')
                print('5) 직전의 것을 ..')
                params.append(txt_arr)
                ext_arr = []
                continue
            #formula_ = before_arr[len(before_arr) - 2:]
            formula_ = before_arr[len(before_arr) - formula_loc:]
            #print('formula :' + str(formula_))
            #print('ext_arr : ' + str(ext_arr))
            merge_ = merge_list_x(formula_, ext_arr, len(formula_))
            print('5) merge ' + str(merge_))
            ext_arr = []
            header.extend(merge_)
            print('6) before params append *****' + str(header))
            params.append(header)
            before_arr = txt_arr
        else:
            #if len(before_arr) > 0:
            #    params.append(before_arr)
            #print('---- just append -----')
            params.append(before_arr)
            before_arr = txt_arr
        before_arr = txt_arr
    else:
        #print('before array len : ' + str(len(before_arr)) + ',' + str(before_arr))
        #print('now array len : ' + str(len(txt_arr)) + ',' + str(txt_arr))
        #print(txt_arr)
        # 중간의 Recipe 이름
        if len(txt_arr) == 1:
            # 여기서 정리해야 한다. append
            if len(parameters_arr) > 0:
                print('7) sub recipe 에서 먼저 parameter 정리 ' + str(parameters_arr))
                yy = prepare_params(parameters_arr[0], parameters_arr[1:])
                for aaa in yy:
                    params.append(aaa)
    
                bParaWork = False   
                parameters_arr = []

            if len(before_arr) > 1 and len(ext_arr) > 0:
                print('7) sub recipe 에서 parameter 붙어 있는 것들 Merge : ' + str(before_arr))
                # Formaula 위치는 unit 위치에서 전체 array 의 length 를 제거 한다.
                formula_loc = len(before_arr) - (before_loc + 1)
                print('.... formula loc ' + str(formula_loc))
                header = before_arr[:len(before_arr) - formula_loc]
                if len(header) == 0:
                    #print('--- header ..')
                    print('8) 직전의 것을 ..')
                    params.append(txt_arr)
                    ext_arr = []
                    continue
                #formula_ = before_arr[len(before_arr) - 2:]
                formula_ = before_arr[len(before_arr) - formula_loc:]
                #print('formula :' + str(formula_))
                #print('ext_arr : ' + str(ext_arr))
                merge_ = merge_list_x(formula_, ext_arr, len(formula_))
                print('9) merge ' + str(merge_))
                ext_arr = []
                header.extend(merge_)
                print('10) before params append *****' + str(header))
                params.append(header)
                before_arr = txt_arr

            
            #params.append(txt_arr)
            #before_arr = txt_arr
            continue
            
        if bParaWork == True:
            parameters_arr.append(txt_arr)
        else:
            if len(before_arr) > 0: #formular 갯수와 같을 때는 그냥 array 에 담는다.
                ext_arr.append(txt_arr)
                print('extra : txt_arr : ' + str(txt_arr))
            else:
                one_row = []
                for j in range(0, len(txt_arr), formula_loc):
                    #print(txt_arr[j] + ' ' + txt_arr[j+1])
                    one_row.append(txt_arr[j] + ' ' + txt_arr[j+1])
                ext_arr.append(one_row)

if len(before_arr) > 0:
    params.append(before_arr)

tmp_params = []
for a in params:
    if len(a) > 0:
        tmp_params.append(a)

params = tmp_params
params
```

```
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
