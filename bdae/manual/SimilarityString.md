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
