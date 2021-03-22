from json import dump

RZYMSKIE = [
    'I.',
    'II.',
    'III.',
    'IV.',
    'V.',
    'VI.',
    'VII.',
    'VIII.',
    'IX.',
    'X.',
    'XI.',
    'XII.',
    'XIII.',
]

edu_idx = 0
f = open('podstawa.txt').read().split('\n')
edu_dir = {}

for line in f:
    
    if(line.startswith('Edukacja') or line.startswith('Wychowanie') or line.startswith('Etyka')):
        edu = RZYMSKIE[edu_idx]
        edu_idx += 1
        edu_dir[edu] = {}
        edu_dir[edu]['nazwa'] = line

        zakres_idx = 1
        osiagniecia_idx = 1

    elif(line.endswith('Uczeń:') or line.endswith('tematów:') or line.endswith('tematycznych:') or line.endswith('uczeń:') or line.endswith('czytania:') or line.endswith('Lektury:')):
        zakres = str(zakres_idx) + '.'
        zakres_idx += 1

        edu_dir[edu][zakres] = {}
        edu_dir[edu][zakres]['nazwa'] = line

        osiagniecia_idx = 1
    
    else:
        osiagniecie = str(osiagniecia_idx) + ')'
        osiagniecia_idx += 1

        edu_dir[edu][zakres][osiagniecie] = line


with open('podstawy_programowe.json', 'w+') as jsonf:
    dump(edu_dir, jsonf, ensure_ascii=False)