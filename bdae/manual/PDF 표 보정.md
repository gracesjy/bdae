### 보정 하기 힘들다.

```
import pdfplumber
inputfile = r'I:\PDFGen1.pdf'

pages = pdf.pages

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

arrs 에 모두 담은 다음
아래는 리스트를 merge
```
def merge_list(data):
    final_arr = []
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
아래는 header (parameter .. ) 를 주고
```
def merge_list2(formula_, data):
    print('formula_ : ' + str(formula_))
    print('data : ' + str(data))
    total = []
    total.append(formula_)
    for x in data:
        total.append(x)

    return_arr = merge_list(total)
    return return_arr
# 호출 방법
header = ['Parameter Default', 'Unit Formula']
data = [['Value Eng', 'M9282 M888'], ['To', 'To'], ['MMS', 'AOS']]
merge_list2(header, data)
```

가장 중요한 것은 Formula 를 찾는 것이다. (단위 위치를 알면 될까 ?)
```
def find_parameter_row(data):
    found = False
    loc = 0
    for i in range(len(data)):
        if data[i].lower().find('parameter') >= 0: # formula 가 위치가 같은 위치 인가 확인
            found = True

        if data[i].lower().find('unit') >= 0:
            loc = i + 1

        if data[i].find('□') >= 0:
            break
        
    return found, loc

```

Parameter 의 Formula 때문에 고통 받고 있다.
```
before_arr = []
# parameter = 4 개
# 그러면 formula 가 있으므로 3개, '□' 포함하면 4개
# formmula 갯수는 2개라는 것을 추축할 수 있다.
ext_arr = []
params = []

parameters_arr = []
before_loc = 0
for i in range(len(arrs)):
    txt = arrs[i]
    txt_arr = txt.split(' ')

    print(txt_arr)
    found, loc = find_parameter_row(txt_arr)
    print('loc : ' + str(loc))
    if loc > 0:
        print(txt_arr)
        before_loc = loc
        parameters_arr.append(txt_arr)
        continue
        
    if before_loc > 0 and txt_arr[0] != '□':
        parameters_arr.append(txt_arr)

    if txt_arr[0] == '□':
        break

parameters_arr
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

def fill_all(data_all):
    ret_arr = []
    lenx = len(data_all[0])
    for i in range(1, len(data_all), 1):
        xxx = fill_(data_all[i], lenx)
        print(xxx)
        ret_arr.append(xxx)
    return ret_arr

merge_list(fill_all(parameters_arr))
## 아래는 결과이다.
## Value -- Default Value이고, Eng는 Unit.Eng 이고 나머지는 Formala 의 값이다.
## 결국 Formula 위치와 갯수를 알면 ..
['Value', 'Eng', 'M9282', 'M888']
['', '', 'To', 'To']
['', '', 'MMS', 'AOS']
## 결국 Formula 위치와 갯수를 알면 .. 뒤의 것만 추출할 수 있다.
['Value\n\n', 'Eng\n\n', 'M9282\nTo\nMMS', 'M888\nTo\nAOS']
```
파라미터 관련 된 것만 먼저 넣는다.
```
params = []
a = parameters_arr[0]
parameter_header_completion = []
parameter_header_completion.append(a)
params.append(a)
yy = merge_list(fill_all(parameters_arr))
parameter_header_completion.append(yy)
params.append(yy)

#for jj in yy:
#    parameter_header_completion.append(jj)
#    params.append(jj)

parameter_header_completion
```
이것은 완본이다.
위의 것과 붙이면 된다.
```
before_arr = []
# parameter = 4 개
# 그러면 formula 가 있으므로 3개, '□' 포함하면 4개
# formmula 갯수는 2개라는 것을 추축할 수 있다.
ext_arr = []
params = []
for i in range(len(arrs)):
    txt = arrs[i]
    txt_arr = txt.split(' ')

    print(' i th {}, data : {}'.format(i, arrs[i]))
    ## formular 를 찾아도 된다.

    found, loc = find_parameter_row(txt_arr)
    if found == True:
        continue
        
    if txt_arr[0] == '□':
        print(' i th {}, params ------------- : {}'.format(i, txt_arr))
        if len(ext_arr) > 0:
            header = before_arr[:len(before_arr) - 2]
            if len(header) == 0:
                params.append(txt_arr)
                ext_arr = []
                continue
            formula_ = before_arr[len(before_arr) - 2:]
            print('formula :' + str(formula_))
            merge_ = merge_list2(formula_, ext_arr)
            print('merge ' + str(merge_))
            ext_arr = []
            header.extend(merge_)
            params.append(header)
        else:
            #if len(before_arr) > 0:
            #    params.append(before_arr)
            print('---- just append -----')
            params.append(txt_arr)
            
        before_arr = txt_arr
    else:
        #print('before array len : ' + str(len(before_arr)) + ',' + str(before_arr))
        #print('now array len : ' + str(len(txt_arr)) + ',' + str(txt_arr))
        #print(txt_arr)
        if len(txt_arr) == 2: #formular 갯수와 같을 때는 그냥 array 에 담는다.
            ext_arr.append(txt_arr)
        else:
            one_row = []
            for j in range(0, len(txt_arr), 2):
                print(txt_arr[j] + ' ' + txt_arr[j+1])
                one_row.append(txt_arr[j] + ' ' + txt_arr[j+1])
            ext_arr.append(one_row)

params
[['Parameter', 'Default', 'Unit', 'Formula'],
 ['Value\n\n', 'Eng\n\n', 'M9282\nTo\nMMS', 'M888\nTo\nAOS'],
 ['□', 'Temperature', '232.2', 'L/h', '323', '324'],
 ['□', 'Pressure', '55', 'barg', 'CIP_5', 'CIP_6'],
 ['□',
  'Pressure',
  '55',
  'barg',
  'CIP_5\n(CIP 4023\nTo 1140)',
  'CIP_6\n(CIP 4023\nTo 3455)'],
 ['□', 'Param2', '4444', 'L', '5959', '4343'],
 ['□', 'Param3', '555', 'N/A', '434', '3434'],
 ['□', 'Param4', '777', 'N/A', '3232', '444']]     
```
역곡에서 
```
def param_redef(params):
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

        print(max_column)

        # parameter line
        one_row = []
        one_row.extend(params[0])
        for i in range(max_column):
            one_row.append('')

        redefined_params.append(one_row)
        # value, unit line
        one_row = []
        one_row.append('') # parameter 
        one_row.extend(params[1])
        for j in range(max_column):
            one_row.append('')
            
        redefined_params.append(one_row)

        # formula ..
        for i in range(2, len(params),1):
            print('formalar val : ' + str(params[i]))
            one_row = []
            for j in range(formula_loc):
                one_row.append('')
                
            one_row.extend(params[i])
            redefined_params.append(one_row)

    return redefined_params

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
