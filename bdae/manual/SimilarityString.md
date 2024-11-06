### Simple String Similarity 

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

lib = ['Process Parameter', 'Parameter Value', 'Agitation(rpm)', 'SKSKS']
my_data = ['Parameter', 'Agitation']
similarity = []
lib_selected = []

for a_data in my_data:
    sim_max_idx, sim = similarity_idx(lib, a_data)
    lib_selected.append(lib[sim_max_idx])
    similarity.append(sim)

lib_selected

dic_data = {'my_data': my_data, 'lib_selected': lib_selected, 'similarity' : similarity}
df = pd.DataFrame(dic_data)
df


```

### 한글 제거 하자.
```
not_kor_str = re.sub(r"[ㄱ-ㅣ가-힣]", "", data1).strip()
```

### 실전
```
def similarity_idx(lib, mydata):
    similarity = []
    for ref_val in lib:
        sim = similar(ref_val, mydata)
        print('lib_data: ' + ref_val + " vs " + mydata + '...' + str(sim))
        similarity.append(sim)

    return similarity.index(max(similarity)), similarity[similarity.index(max(similarity))]

library = ['Filter', 'Media Regin', 'pH s', 'CO2', 'Agitation', 'Mixed']

mbr = []
pf = []
seq = []
step = []
procedures = []

similarity = []
lib_selected = []

for i in range(0, len(df)):
    a_mbr = df.loc[i]['MBR']
    a_pf = df.loc[i]['ProcessFlow']
    a_seq = df.loc[i]['SEQ']
    a_step = df.loc[i]['Step']
    a_procedures = df.loc[i]['Procedures']
    if a_procedures == None or len(a_procedures) == 0 or len(a_procedures) > 30:
        mbr.append(a_mbr)
        pf.append(a_pf)
        seq.append(a_seq)
        step.append(a_step)
        procedures.append(a_procedures)
        similarity.append(None)
        lib_selected.append('')
        continue
    else:
        sim_max_idx, sim = similarity_idx(library, a_procedures)
        mbr.append(a_mbr)
        pf.append(a_pf)
        seq.append(a_seq)
        step.append(a_step)
        procedures.append(a_procedures)
        lib_selected.append(library[sim_max_idx])
        similarity.append(sim)

dic_data = {'MBR': mbr, 'ProcessFlow' : pf, 'SEQ' : seq, 'Step' : step, 'Procedures' : procedures, 'lib_selected': lib_selected, 'similarity': similarity}
dfx = pd.DataFrame(dic_data)
dfx
```

