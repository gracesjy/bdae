## How to manage Style

```
from spire.doc import *
from spire.doc.common import *

# Create a Document object
document = Document()
# Load a Word document

input = r'G:\DeepLearning\MultilevelMixedList.docx'

document.LoadFromFile(input)

for i in range(len(document.ListStyles)):
    print(document.ListStyles[i].Name)
    
print(len(document.ListStyles))
print(document.ListStyles[0].Name)
# Get the first section in the document
section = document.Sections[0]

# Create a list to store the extracted text
section_text = []

# Iterate through the paragraphs in the section
for i in range(section.Paragraphs.Count):
    paragraph = section.Paragraphs[i]
    lf = paragraph.ListFormat.ListLevelNumber
    print(str(lf) + ' : ' + paragraph.Text)
    # Extract the text of each paragraph and append it to the list
    section_text.append(paragraph.Text)

# print(section_text)
# Write the extracted text into a text file
#with open("Output/SectionText.txt", "w", encoding="utf-8") as file:
#    file.write("\n".join(section_text))

document.Close()
```
