## How to manage Style

```
from spire.doc import *
from spire.doc.common import *

# Create a Document object
document = Document()
# Load a Word document

input = r'I:\InterfaceD.doc'

document.LoadFromFile(input)
# 1) All Style Listed !
# ----------------------
for i in range(document.Sections.Count):
    section = document.Sections.get_Item(i)
    for j in range(section.Paragraphs.Count):
        paragraph = section.Paragraphs.get_Item(j)
        print(paragraph.StyleName)
# ----------------------

for i in range(len(document.ListStyles)):
    print(document.ListStyles[i].Name)

print('----')
print(len(document.ListStyles))
print(document.ListStyles[0].Name)

print('No. of Sections : ' + str(document.Sections.Count))
# Get the first section in the document
section = document.Sections[0]



# Create a list to store the extracted text
section_text = []

# Iterate through the paragraphs in the section
for j in range(document.Sections.Count):
    section_ = document.Sections[j]
    print('> section no. : ' + str(j))
    for i in range(section_.Paragraphs.Count):
        paragraph = section_.Paragraphs[i]
        lf = paragraph.ListFormat.ListLevelNumber
        print('>>> section no : ' + str(j) + ' -- ' + str(lf) + ' : ' + paragraph.Text)
        # Extract the text of each paragraph and append it to the list
        section_text.append(paragraph.Text)

# New Style -------------
listStyle = ListStyle(document, ListType.Numbered)
listStyle.Name = "levelstyle"
listStyle.Levels[0].PatternType = ListPatternType.Arabic
listStyle.Levels[0].TextPosition = 20.0
listStyle.Levels[1].NumberPrefix = "%1."
listStyle.Levels[1].PatternType = ListPatternType.Arabic
listStyle.Levels[2].NumberPrefix = "%1.%2."
listStyle.Levels[2].PatternType = ListPatternType.Arabic
document.ListStyles.Add(listStyle)

# paragraph.StyleName
paragraph = section.AddParagraph()
paragraph.AppendText("The first item")

paragraph.ListFormat.ApplyStyle("levelstyle")
paragraph.ListFormat.ListLevelNumber = 0

paragraph = section.AddParagraph()
paragraph.AppendText("The second item")
paragraph.ListFormat.ApplyStyle("levelstyle")
paragraph.ListFormat.ListLevelNumber = 0

paragraph = section.AddParagraph()
paragraph.AppendText("The first sub-item")
paragraph.ListFormat.ApplyStyle("levelstyle")
paragraph.ListFormat.ListLevelNumber = 1

paragraph = section.AddParagraph()
paragraph.AppendText("The second sub-item")
paragraph.ListFormat.ContinueListNumbering()
paragraph.ListFormat.ApplyStyle("levelstyle")

paragraph = section.AddParagraph()
paragraph.AppendText("A sub-sub-item")
paragraph.ListFormat.ApplyStyle("levelstyle")
paragraph.ListFormat.ListLevelNumber = 2

paragraph = section.AddParagraph()
paragraph.AppendText("The third item")
paragraph.ListFormat.ApplyStyle("levelstyle")
paragraph.ListFormat.ListLevelNumber = 0

#### Apply the Already Existed Style !!!
paragraph = section.AddParagraph()
paragraph.AppendText("ATLAS is Good")
paragraph.ApplyStyle("Title01")

out = r'I:\InterfaceD2.doc'
document.SaveToFile(out, FileFormat.Docx)
#print(section_text)
# Write the extracted text into a text file
#with open("Output/SectionText.txt", "w", encoding="utf-8") as file:
#    file.write("\n".join(section_text))

document.Close()
```
