from docx import Document
from json import load
from docx.shared import Pt
from sys import platform
try:
    from os import startfile
except ImportError as e:
    pass


# get the input
## Sample input:
# I. 1. 1) 2) 3) 5) 2. 1) 2) 3) 4) 7) 3. 1) 2) 3) 4) 4. 1) 4) 5) 7) 8) 5. 2) 4) 5) 6)
# II. 4. 2), 6. 8) 9)
# III. 1. 1) 3) 4)
def getLines():
    lines = []
    print('Wklej indeksy rozdzialow tutaj: ')
    while True:
        line = input()
        if(line):
            lines.append(line)
        else:
            break

    return lines

# parse input into dictionary calls
# edu
## zakres
### osiagniecia
def parseInput(lines):
    calls = [] # list of dictionaries

    for line in lines:
        line = line.split(' ')
        edu = line[0]
        for index in line[1:]:
            if(not index.endswith(')')):
                zakres = index
                continue
            else:
                osiagniecie = index

            tmp = {
                'edu': edu,
                'zakres': zakres,
                'osiagniecie': osiagniecie
            }
            # print(tmp)
            calls.append(tmp)
    
    return calls


#create .docx document
def createDocument(data, lines):
    # header: wklejony input, Times New Roman, 10
    # edu: Times New Roman, 12, pogrubione
    # zakres: Times New Roman, 12, podkreslenie
    # osiagniecie: Times New Roman, 12, zwykly

    calls = parseInput(lines)
    d = Document()
    font = d.styles['Normal'].font
    font.name = 'Times New Roman'
    font.size = Pt(10)

    # create header
    for line in lines:
        p = d.add_paragraph(line)

    p.add_run('\n') # newline
    font.size = Pt(12)
    last_edu = ''
    last_zakres = ''
    for call in calls:
        # create edu section
        edu = call['edu']
        if(last_edu != edu):
            p.add_run('\n')
            text = edu + ' ' + data[edu]['nazwa'] + '\n'
            p.add_run(text).bold = True

        # create zakres section
        zakres = call['zakres']
        if(last_zakres != zakres):
            p.add_run('\n')
            text = zakres + ' ' + data[edu][zakres]['nazwa'] + '\n'
            p.add_run(text).underline = True

        # create osiagniecie section
        osiagniecie = call['osiagniecie']
        text = osiagniecie + ' ' + data[edu][zakres][osiagniecie] + '\n'
        # d.add_paragraph(text)
        p.add_run(text)

        last_edu = edu
        last_zakres = zakres

    filename = 'podstawy_programowe.docx'
    d.save(filename)
    if(platform == 'win32'):
        startfile(filename)
    
# load json file
with open('podstawy_programowe.json') as f:
    data = load(f)

lines = getLines()
createDocument(data, lines)