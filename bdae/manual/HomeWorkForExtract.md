### Database Query Ordering
```
select  A,B,C,D,E,F,G,H, trim(D) as version_number,
        nvl(LPAD(trim(regexp_substr(D, '[^.]+', 1, 1)),3,'0'),'000') AS Major,
        nvl(LPAD(trim(regexp_substr(D, '[^.]+', 1, 2)),3,'0'),'000') AS Minor, 
        nvl(LPAD(trim(regexp_substr(D, '[^.]+', 1, 3)),3,'0'),'000') AS Revision
        from TEST_RETURN
        ORDER BY Major asc, Minor asc, Revision ASC
```

### Basic 
```
x = df.loc[7, ['Procedures', 'REF_VAR1', 'REF_VAR2']].values.tolist()
```

#### Extrace from sentence
```
all_calc = []
before_step = ''
# ['MBR', 'ProcessFlow', 'SEQ', 'Step', 'Procedures', 'REF_VAR1', 'REF_VAR2', 'REF_VAR3']
for i in range(0, len(df)):
    mbr = df.loc[i]['MBR']
    pf = df.loc[i]['ProcessFlow']
    seq = df.loc[i]['SEQ']
    step = df.loc[i]['Step']
    
    if seq == 0:
        instruction = df.loc[i]['Procedures']
        print(instruction)
        if instruction.find('계산') >= 0:
            before_step = step
    else:
        if step == before_step:
            # 매우 중요한 부분이다.
            x = df.loc[i, ['MBR', 'ProcessFlow', 'SEQ', 'Step', 'Procedures', 'REF_VAR1', 'REF_VAR2']].values.tolist()
            print(type(x))
            all_calc.append(x)
        else:
            before_step = ''

print('--------------------')
all_calc
```
abve result
```
[['E2BC05',
  '3.1.',
  4,
  '3.1.2.',
  'Volume A\n= I2 in step 7.2.3 from E2BC03\nSet Point: 150\nAcceptable Range: 50.43 to 200',
  'L1',
  nan],
 ['E2BC05', '3.1.', 5, '3.1.2.', 'Volume B\n= L1 x 0.342', 'L2', nan],
 ['E2BC05', '3.1.', 6, '3.1.2.', '-----', nan, nan],
 ['E2BC05', '3.1.', 7, '3.1.2.', 'Final Weight\n= L2/0.232', 'L3', nan]]
```

### Basic Functions : Regular Expression
```
def calc_eqs(data):
    print('calc_eqs ..')
    p = re.compile('=(.+)')
    m = p.match(data)
    if m:
        return m.group(1).strip()
    else:
        return ''

print(calc_eqs('= L1 x 0.342'))
```

```
def target_data(data):
    p = re.compile('Target Range:(.+)to(.+)')
    m = p.match(data)
    if m:
        return [m.group(1).strip(), m.group(2).strip()]
    else:
        p = re.compile('Target Range: ≤ (.+)')
        m = p.match(data)
        if m:
            return ['', m.group(1).strip()]
        else:
            p = re.compile('Target Range: ≥ (.+)') 
            m = p.match(data)
            if m:
                return [m.group(1).strip(), '']

    return []

def ref_variable_simple(data):
    p = re.compile('(.+)[\s]+in step(.+)')
    m = p.match(data)
    if m:
        return list(m.groups())
    else:
        return []

def ref_variable(data):

    p = re.compile('(.+)[\s]+in step(.+)from(.+)')
    m = p.match(data)
    if m:
        return list(m.groups())

    print('another ..')
    p = re.compile('(.+)[\s]+step(.+)')
    m = p.match(data)
    if m:
        return list(m.groups())
    
    return []

ref_variable('I3 in step 7.2.3 from E2BC04')
# ['I3', ' 7.2.3 ', ' E2BC04']

acceptable_data('Acceptable Range: ≥ 100.23')
['100.23', '']
```

```
def setpoint(data):
    p = re.compile('Set Point: (.+)')
    m = p.match(data)
    if m:
        return m.group(1).strip()
    else:
        return ''

print(setpoint('Set Point: 202.23'))
print('>' + setpoint('Acceptable Range: 50.43 to 200') + '<')
```

### Calcuation 
```
# input : ['E2BC05', '3.1.', 3, '3.1.5.', 'DO', 'Acceptable Range: ≤ 50', '']
idx_mbr = 0
idx_pf = 1
idx_seq = 2
idx_step = 3
idx_proc = 4
idx_var1 = 5
idx_var2 = 6

# 이름, 변수, Reference 변수, '다른 MBR', 수식, Set Point, AR/TR, LOWER, UPPER 순으로 잡는다.
all_arrange = []

not_in = ['--', '', None]
for one_ in all_calc:
    print(one_)
    arrange = []
    if one_ == None or one_ == []:
        print('Raw Data have problems')
        continue
        
    # 데이트를 만들 때 딱 3개만 했다.
    print ('length of list : ' + str(len(one_)))

    if one_[idx_proc] == None or one_[idx_proc] == '' or one_[idx_proc].find('---') >= 0:
        print('wrong data continue ...')
        continue

    eqs = one_[idx_proc].split('\n')
    # 아래 출력은 다음과 같은 모습이다.
    # ['Volume A', '= I2 step 7.2.3 in E2BC03', 'Set Point: 150', 'Acceptable Range: 50 to 200']
    print('=======================================')
    print(eqs)
    print('=======================================')
    len_of_eqs = len(eqs)
    if len_of_eqs == 1:
        #
        arrange.append(one_[idx_mbr])
        arrange.append(one_[idx_pf])
        arrange.append(one_[idx_seq])
        arrange.append(one_[idx_step])
        # 오직 이름만 있다.
        arrange.append(eqs[0])
        arrange.append('')
        arrange.append('')
        
    else:
        arrange.append(one_[idx_mbr])
        arrange.append(one_[idx_pf])
        arrange.append(one_[idx_seq])
        arrange.append(one_[idx_step])
        arrange.append(eqs[0]) # 이름
        arrange.append(one_[idx_var1]) # 변수
        print(calc_eqs(eqs[1]))
        arrange.append(calc_eqs(eqs[1])) # 수식
        refs = ref_variable(calc_eqs(eqs[1]))
        if refs != []:
            print(refs)
            arrange.append(refs[0])
            arrange.append(refs[1])
            arrange.append(refs[2])
        else:
            refs = ref_variable_simple(calc_eqs(eqs[1]))
            if refs == []:
                arrange.append('')
                arrange.append('')
                arrange.append('')
            else:
                print('========================')
                print(refs)
                arrange.append(refs[0])
                arrange.append('')
                arrange.append('')
        # 이제부터는 Optional
        ''' 아래 삭제
        if len_of_eqs < 3:
            arrange.append('') # Set Point
            arrange.append('') # AR/TR
            arrange.append('') # Lower
            arrange.append('') # Upper
            '''

        set_point_  = ''
        acceptable_ = []
        for option in range(2, len_of_eqs):
            print('--- option start ----')
            print(eqs[option])
            print('--- option end ---')
            a_set_point_ = setpoint(eqs[option])
            
            if len(a_set_point_) > 0:
                print('Set Point Set !!!!!!!!!!!!!!!!!!!!')
                set_point_ = a_set_point_
                print('> Set Point : >' + a_set_point_ + '< from ' + eqs[option])


            
            a_acceptable_ = acceptable_data(eqs[option])

            if a_acceptable_ != []:
                acceptable_ = a_acceptable_


        print('Final Set Point : ' + set_point_)
        arrange.append(set_point_)

        if acceptable_ == []:
            arrange.append('')
            arrange.append('')
            arrange.append('')
        else:
            arrange.append('AR')
            arrange.append(acceptable_[0])
            arrange.append(acceptable_[1])
            
        
                    
    all_arrange.append(arrange)
        
    '''
    idx = 0
    for y in x:
        print(str(idx) + ' : ' + str(y))
        idx = idx + 1

        eqs = y.split('\n')
        len_of_eqs = len(eqs)
            
        if len_of_eqs == 1:
            # 오직 이름만 있을 경우
            arrage.append(eqs[0])
        elif len_of_eqs == 2:
            # 이름, 수식, 변수, 단위 등
            arrange.append
    '''
            
print(all_arrange) 
```
above results
```
[
['E2BC05', '3.1.', 4, '3.1.2.', 'Volume A', 'L1', 'I2 in step 7.2.3 from E2BC03', 'I2', ' 7.2.3 ', ' E2BC03', '150', 'AR', '50.43', '200'],
['E2BC05', '3.1.', 5, '3.1.2.', 'Volume B', 'L2', 'L1 x 0.342', '', '', '', '', '', '', ''],
['E2BC05', '3.1.', 7, '3.1.2.', 'Final Weight', 'L3', 'L2/0.232', '', '', '', '', '', '', '']
]
```

### Basic 
```
def ref_variable(data):
    print('another ..')
    p = re.compile('(.+)[\s]+in step(.+)from(.+)')
    m = p.match(data)
    if m:
        return list(m.groups())
    return []

def ref_variable_simple(data):
    p = re.compile('(.+)[\s]+in step (.+)')
    m = p.match(data)
    if m:
        return list(m.groups())

def ref_variable_simple(data):
    p = re.compile('(.+)[\s]+in step (.+)')
    m = p.match(data)
    if m:
        return list(m.groups())

p = re.compile('(.+)[\s]+in step (.+)')
m = p.match('I2 in step 7.2.3')
if m:
    print('OK')
    print(m.groups())

a = ref_variable_simple('I2 in step 7.2.3')
a.append('')
# ['I2', '7.2.3', '']

```

### Horizontal Extraction
```
import math
dic_parameters = ['Parameters',	'Acceptable Range',	'Set Point']


all_parameters = []
before_step = ''

one_parameters = []
searched = False
set_step = '' # 7.x.x
for i in range(0, len(df)):
    mbr = df.loc[i]['MBR']
    pf = df.loc[i]['ProcessFlow']
    seq = df.loc[i]['SEQ']
    step = df.loc[i]['Step']
    
    if seq > 0:
        instruction = df.loc[i]['Procedures'].strip()
        if instruction in dic_parameters:
            x = df.loc[i, ['Procedures', 'REF_VAR1', 'REF_VAR2']].values.tolist()
            print(type(x))
            if x == dic_parameters:
                print('OK ------------')
                set_step = step
                searched = True
            else:
                searched = False
                set_step = ''
        else:
            # 우리는 parameter 의 갯수가 3칸 이란 것을 안다.
            x = df.loc[i, ['Procedures', 'REF_VAR1', 'REF_VAR2']]
            # 길이가 바뀌면 아닌 것이다.
            
            bNotSameLength = True
            if x[1] == None and x[2] == None:
                print('===> not proper <====')
                bNotSameLength = False

            ## 이 부분은 Excel 을 읽어서이다.
            if isinstance(x[1], float) and isinstance(x[2], float):
                bNotSameLength = False

            '''
            if x[0].find('바코드') >= 0:
                print('-------------')
                print(type(x[1]))
                if math.isnan(x[1]):
                    print('1st is NaN')
                    
                print('-------------')
            '''
                
            if searched == True and set_step == step and bNotSameLength == True:
                one_parameters.append(mbr)
                one_parameters.append(pf)
                one_parameters.append(seq)
                one_parameters.append(step)
                one_parameters.append(x[0])
                one_parameters.append('Acceptable Range: ' + x[1])
                if isinstance(x[2],float):
                    one_parameters.append('')
                else: 
                    one_parameters.append('Set Point:' + str(x[2]))
                all_parameters.append(one_parameters)
                one_parameters = []
            else:
                one_parameters = []
                searched = False
                
        
all_parameters
```
above output
```
[['E2BC05',
  '3.1.',
  2,
  '3.1.5.',
  'pH',
  'Acceptable Range: 20 to 50',
  'Set Point:60'],
 ['E2BC05', '3.1.', 3, '3.1.5.', 'DO', 'Acceptable Range: ≤ 50', ''],
 ['E2BC05', '3.1.', 4, '3.1.5.', 'CO2', 'Acceptable Range: ≥ 100', '']]

```

above output
```
result = []
for a_param_array in all_parameters:
    one_row = []
    one_row.append(a_param_array[0])
    one_row.append(a_param_array[1])
    one_row.append(a_param_array[2])
    one_row.append(a_param_array[3])
    one_row.append(a_param_array[4])
    one_row.extend(acceptable_data(a_param_array[5]))
    result.append(one_row)

result

```
above result
```
[['E2BC05', '3.1.', 2, '3.1.5.', 'pH', '20', '50'],
 ['E2BC05', '3.1.', 3, '3.1.5.', 'DO', '', '50'],
 ['E2BC05', '3.1.', 4, '3.1.5.', 'CO2', '100', '']]
```
