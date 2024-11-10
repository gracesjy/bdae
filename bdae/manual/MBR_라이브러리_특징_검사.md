### 1) 읽기
```
import pandas as pd

excel_dir = r'G:\DeepLearning\MBR_LIB_RAW.xlsx'
df = pd.read_excel(excel_dir, sheet_name='시트1', header=0)
```
### 2) 추출
```
key = []
diction = {}
diction_code = {}
# 1) Key 컬럼을 먼저 정의한다.
key_columns = df[['A','B','C','D']].columns.tolist()
print(key_columns)

# 2) 데이터를 정렬한다. - 과연 될까 ?
for i in range(len(df)):
    x = df.loc[i, df.columns.tolist()].values.tolist()
    print(x)
    d = '^'.join(x[:4])
    if d in diction.keys():
        p = diction.get(d)
        p.append(x[5])
        z = diction_code.get(d)
        z.append({ x[5] : x[4]})
    else:
        diction.setdefault(d, [x[5]])
        diction_code.setdefault(d, [{ x[5] : x[4]}])

# 3) 최대 길이를 계산 하면서 소팅 한다.
max_len = 0
for x in diction.keys():
    data = diction.get(x)
    print(data)
    data = sorted(data)
    #print(data)
    diction.update({x: data})
    if max_len < len(data):
        max_len = len(data)

# 4) pandas 를 위해서  컬럼을 add column
for i in range(max_len):
    key_columns.append('VAR' + str(i + 1))

# 5) pandas 를 위해서 리스트 길이를 맞춘다.
for x in diction.keys():
    data = diction.get(x)
    if len(data) < max_len:
        len_ = len(data)
        for i in range(max_len - len_):
            data.append('')

# 6) pandas 를 위해서 전체 리스트를 정렬 해 준다.
total_list = []
for x in diction.keys():
    y = x.split('^')
    data = diction.get(x)
    if data == None:
        continue
    y.extend(data)
    #print(data)
    #y =y.sort()
    total_list.append(y)

# 7) 출력을 위해서 pandas 를 만들어 준다.
df_out = pd.DataFrame(total_list, columns=key_columns)
# 이것 안하면 오류가 났었다. 확인
df_out = df_out.reindex(columns=df_out.columns.tolist())
```
### 3) 유사도
```
from difflib import SequenceMatcher
import pandas as pd
 
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def similarity_idx(lib, mydata):
    similarity = []
    for ref_val in lib:
        sim = similar(ref_val, mydata)
        similarity.append(sim)

    return similarity.index(max(similarity)), similarity[similarity.index(max(similarity))]

def bagofwords(vocaList, inputSet):
    returnVec = []
    if len(vocaList) > len(inputSet):
        returnVec = [0]*len(vocaList)
        for word in inputSet:
            if word in vocaList:
                returnVec[vocaList.index(word)] += 1
            else:
                sim_arr = []
                for x in vocaList:
                    sim = similar(x, word)
                    sim_arr.append(sim)
    
                idx = sim_arr.index(max(sim_arr))
                returnVec[idx] = sim_arr[idx]
    else:
        returnVec = [0]*len(inputSet)
        for word in vocaList:
            if word in inputSet:
                returnVec[inputSet.index(word)] += 1
            else:
                sim_arr = []
                for x in inputSet:
                    sim = similar(x, word)
                    sim_arr.append(sim)
    
                idx = sim_arr.index(max(sim_arr))
                returnVec[idx] = sim_arr[idx]
    sum = 0
    for a in returnVec:
        sum += a
    similarity = sum/len(returnVec)
    return similarity
```

### 4) 공백 등으로 대체
```
df_out = df_out.fillna('')

```

### 5) 유사도
```
diction = {}
for i in range(len(df_out)):
    x = df_out.loc[i, ['A', 'B', 'C', 'D', 'VAR1', 'VAR2', 'VAR3', 'VAR4']].values.tolist()
    print(x)
    d = '^'.join(x[:4])
    val = x[4:]
    print(val)
    val = list(filter(None, val))
    if d in diction.keys():
        continue
    else:
        diction.setdefault(d, val)

print(diction)

dic_result = {}
for x in diction.keys():
    data_x = diction.get(x)
    ## 귀찮아서..
    similarity = []
    keys = []
    for y in diction.keys():
        if x != y:
            data_y = diction.get(y)
            print('x : ' + str(data_x))
            print('y : ' + str(data_y))
            if belongToNan(data_y):
                print('none detected ...')
                continue
            if belongToNan(data_x):
                print('none detected ..')
                continue
            sim = bagofwords(data_x,data_y)
            print(str(data_x) + ' ... vs ...' + str(data_y) + '===> ' + str(sim))
            similarity.append(sim)
            keys.append(y)
        else:
            continue
            
    max_idx = similarity.index(max(similarity))
    max_similar_key = keys[max_idx]
    max_similarity = similarity[max_idx]

    if x in dic_result.keys():
        continue
    else:
        dic_result.setdefault(x, [max_similar_key, max_similarity])
        
    print('input : ' + x + '.. max sim key : ' + max_similar_key + ',' + str(max_similarity))
        
dic_result

```

### 5) 차이가 나는 컬럼
```
for x in dic_result.keys():
    data = dic_result.get(x)
    #print(data)
    print(x + ' .. vs .. ' + data[0])
    ref_data = diction.get(data[0])
    data_data = diction.get(x)
    set_data = set(data_data)
    set_ref = set(ref_data)
    print(len(set_ref))
    if len(set_ref) > len(set_data):
        print('data (' + str(data_data) + ')' + 'ref data (' + str(ref_data) + ' .... differ : ' + str(set_ref.difference(set_data)))
    else:
        print('data (' + str(data_data) + ')' + 'ref data (' + str(ref_data) + ' .... differ : ' + str(set_data.difference(set_ref)))

```
