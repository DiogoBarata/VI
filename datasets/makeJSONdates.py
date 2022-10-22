import json
from datetime import datetime
""""
{"thirsty_davinci Sorcerer 13|Cleric 1": {
    "name": ["thirsty_davinci"], 
    "race": ["Dwarf"], 
    "date": ["2022-08-23 13:02:11"], 
    "class": {
        "Sorcerer": {
            "class": ["Sorcerer"], 
            "subclass": ["Clockwork Soul"], 
            "level": [13], 
            "originality": 0.00409695849270464
        }, 
        "Cleric": {
            "class": ["Cleric"], 
            "subclass": ["Order Domain"], 
            "level": [1], 
            "originality": 0.005964356700705374}
        }
    }
    "level": [14], 
    "feats": ["Fey Touched", "War Caster", "Metamagic Adept"], 
    "HP": [146], "AC": [10], "attributes": {"Str": [9], "Dex": [11], "Con": [20], "Int": [14], "Wis": [14], "Cha": [20]}, 
    "alignment": ["None"], 
    "skills": ["Arcana", "Religion", "Intimidation"], 
    "choices": {"metamagic": ["Twinned Spell", "Subtle Spell", "Quickened Spell", "Extended Spell"]}, 
    "location": ["CA"]},
"""


CLASSES = ['Artificer','Barbarian','Bard','Cleric','Druid','Fighter','Monk','Paladin',
'Ranger','Rogue','Sorcerer','Warlock','Wizard']
ALIGNS = ['CG','CN','LG','NG','LN','LE','CE','NN','NE']
RACES = ['Aarakocra', 'Aasimar', 'Bugbear', 'Centaur', 'Changeling', 'Custom', 
        'Dragonborn', 'Dwarf', 'Eladrin', 'Elf', 'Firbolg', 'Genasi', 'Gith', 'Gnome', 
        'Goblin', 'Goliath', 'Half-Elf', 'Half-Orc', 'Halfling', 'Hobgoblin', 'Human', 
        'Kalashtar', 'Kenku', 'Kobold', 'Leonin', 'Lizardfolk', 'Loxodon', 'Minotaur', 
        'Orc', 'Satyr', 'Shifter', 'Simic hybrid', 'Tabaxi', 'Tiefling', 'Triton', 
        'Turtle', 'Vedalken', 'Warforged', 'Yaun-Ti']
YEARS = ['18','19','20','21','22','All']
VARS = ["class","alignment"]
filename = "datasets/cleaned/dnd_chars_all_cleaned.json"

#relations  |race   |class  |align  |
# race      |   \   |   x   |   x   |
# class     |   x   |   \   |   x   |
# align     |   X   |   x   |   \   |

class_align_count = {'All':{},'18':{},'19':{},'20':{},'21':{},'22':{}}
align_class_count = {'All':{},'18':{},'19':{},'20':{},'21':{},'22':{}}

race_class_count = {'All':{},'18':{},'19':{},'20':{},'21':{},'22':{}}
class_race_count = {'All':{},'18':{},'19':{},'20':{},'21':{},'22':{}}

race_align_count = {'All':{},'18':{},'19':{},'20':{},'21':{},'22':{}}
align_race_count = {'All':{},'18':{},'19':{},'20':{},'21':{},'22':{}}


def checkYear(year):
    return year[-2:]

# Generate dicts to use for the JSON
def class_align(data,char,year):
    aux_align = data[char]['alignment'][0]
    for char_class in data[char]['class']:
        if char_class in CLASSES:
            if aux_align != 'None':
                if char_class not in class_align_count['All']:
                    class_align_count['All'][char_class] = {aux_align:1}
                else:
                    if aux_align not in class_align_count['All'][char_class]:
                        class_align_count['All'][char_class][aux_align] = 1
                    else:
                        class_align_count['All'][char_class][aux_align] += 1
                
                if char_class not in class_align_count[year]:
                    class_align_count[year][char_class] = {aux_align:1}
                else:
                    if aux_align not in class_align_count[year][char_class]:
                        class_align_count[year][char_class][aux_align] = 1
                    else:
                        class_align_count[year][char_class][aux_align] += 1

def align_class(data,char,year):
    aux_align = data[char]['alignment'][0]
    if aux_align != 'None':
        for char_class in data[char]['class']:
            if char_class in CLASSES:
                if aux_align not in align_class_count['All']:
                    align_class_count['All'][aux_align] = {char_class:1}
                else:
                    if char_class not in align_class_count['All'][aux_align]:
                        align_class_count['All'][aux_align][char_class] = 1
                    else:
                        align_class_count['All'][aux_align][char_class] += 1

                if aux_align not in align_class_count[year]:
                    align_class_count[year][aux_align] = {char_class:1}
                else:
                    if char_class not in align_class_count[year][aux_align]:
                        align_class_count[year][aux_align][char_class] = 1
                    else:
                        align_class_count[year][aux_align][char_class] += 1

def class_race(data,char,year):
    aux_race = data[char]['race'][0]
    for char_class in data[char]['class']:
        if char_class in CLASSES:
            if aux_race != '':
                if char_class not in class_race_count['All']:
                    class_race_count['All'][char_class] = {aux_race:1}
                else:
                    if aux_race not in class_race_count['All'][char_class]:
                        class_race_count['All'][char_class][aux_race] = 1
                    else:
                        class_race_count['All'][char_class][aux_race] += 1
                
                if char_class not in class_race_count[year]:
                    class_race_count[year][char_class] = {aux_race:1}
                else:
                    if aux_race not in class_race_count[year][char_class]:
                        class_race_count[year][char_class][aux_race] = 1
                    else:
                        class_race_count[year][char_class][aux_race] += 1

def race_class(data,char,year):
    aux_race = data[char]['race'][0]
    if aux_race != '':
        for char_class in data[char]['class']:
            if char_class in CLASSES:
                if aux_race not in race_class_count['All']:
                    race_class_count['All'][aux_race] = {char_class:1}
                else:
                    if char_class not in race_class_count['All'][aux_race]:
                        race_class_count['All'][aux_race][char_class] = 1
                    else:
                        race_class_count['All'][aux_race][char_class] += 1
                
                if aux_race not in race_class_count[year]:
                    race_class_count[year][aux_race] = {char_class:1}
                else:
                    if char_class not in race_class_count[year][aux_race]:
                        race_class_count[year][aux_race][char_class] = 1
                    else:
                        race_class_count[year][aux_race][char_class] += 1

def race_align(data,char,year):
    aux_race = data[char]['race'][0]
    aux_align = data[char]['alignment'][0]
    if aux_race != '':
        if aux_align != 'None':
            if aux_race not in race_align_count['All']:
                race_align_count['All'][aux_race] = {aux_align:1}
            else:
                if aux_align not in race_align_count['All'][aux_race]:
                    race_align_count['All'][aux_race][aux_align] = 1
                else:
                    race_align_count['All'][aux_race][aux_align] += 1
            
            if aux_race not in race_align_count[year]:
                race_align_count[year][aux_race] = {aux_align:1}
            else:
                if aux_align not in race_align_count[year][aux_race]:
                    race_align_count[year][aux_race][aux_align] = 1
                else:
                    race_align_count[year][aux_race][aux_align] += 1

def align_race(data,char,year):
    aux_race = data[char]['race'][0]
    aux_align = data[char]['alignment'][0]
    if aux_race != '':
        if aux_align != 'None':
            if aux_align not in align_race_count['All']:
                align_race_count['All'][aux_align] = {aux_race:1}
            else:
                if aux_race not in align_race_count['All'][aux_align]:
                    align_race_count['All'][aux_align][aux_race] = 1
                else:
                    align_race_count['All'][aux_align][aux_race] += 1

            if aux_align not in align_race_count[year]:
                align_race_count[year][aux_align] = {aux_race:1}
            else:
                if aux_race not in align_race_count[year][aux_align]:
                    align_race_count[year][aux_align][aux_race] = 1
                else:
                    align_race_count[year][aux_align][aux_race] += 1

# Generate JSONS structures
def create_json(center,count_dict):
    relation = list(count_dict[center].keys())
    id = 1
    network_json = {'nodes':[],'links':[]}
    network_json['nodes'].append({'id':id,'name':center})
    id +=1
    for rel in relation:
        network_json['nodes'].append({'id':id,'name':rel})
        network_json['links'].append({'source':1,'target':id,'distance':count_dict[center][rel]})
        id+=1
    return network_json


#----------Main------------
with open(filename,"r",encoding="utf-8") as f:
    data = json.load(f)
    new_json = {}
    for character in data:
        year = checkYear(str((datetime.strptime(data[character]['date'][0], '%Y-%m-%d %H:%M:%S')).year))
        class_align(data,character,year)
        align_class(data,character,year)
        race_class(data,character,year)
        class_race(data,character,year)
        race_align(data,character,year)
        align_race(data,character,year)

    # Create and append the network JSON structure to a JSON file
    class_align_json = {'All':{},'18':{},'19':{},'20':{},'21':{},'22':{}}
    class_race_json = {'All':{},'18':{},'19':{},'20':{},'21':{},'22':{}}
    for fun_year in class_align_count:
        for fun_class in class_align_count[fun_year]:
            class_align_json[fun_year][fun_class]=create_json(fun_class,class_align_count[fun_year])
        for fun_class in class_race_count[fun_year]:
            class_race_json[fun_year][fun_class]=create_json(fun_class,class_race_count[fun_year])
    new_json['Class_Alignment'] = class_align_json
    new_json['Class_Race'] = class_race_json
    
    race_class_json = {'All':{},'18':{},'19':{},'20':{},'21':{},'22':{}}
    race_align_json = {'All':{},'18':{},'19':{},'20':{},'21':{},'22':{}}
    for fun_year in class_align_count:
        for fun_race in race_class_count[fun_year]:
            race_class_json[fun_year][fun_race] = create_json(fun_race, race_class_count[fun_year])
        for fun_race in race_align_count[fun_year]:
            race_align_json[fun_year][fun_race] = create_json(fun_race, race_align_count[fun_year])
    new_json['Race_Class'] = race_class_json
    new_json['Race_Alignment'] = race_align_json

    align_class_json = {'All':{},'18':{},'19':{},'20':{},'21':{},'22':{}}
    align_race_json = {'All':{},'18':{},'19':{},'20':{},'21':{},'22':{}}
    for fun_year in class_align_count:
        for fun_align in align_class_count[fun_year]:
            align_class_json[fun_year][fun_align] = create_json(fun_align,align_class_count[fun_year])
        for fun_align in align_race_count[fun_year]:
            align_race_json[fun_year][fun_align] = create_json(fun_align,align_race_count[fun_year])
    new_json['Alignment_Class'] = align_class_json
    new_json['Alignment_Race'] = align_race_json


with open('network_all_data_with_dates.json',"w") as f:
    json.dump(new_json,f,indent=2)