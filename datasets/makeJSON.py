import json
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

VARS = ["class","alignment"]
filename = "datasets/cleaned/dnd_chars_all_cleaned.json"

#relations  |race   |class  |align  |
# race      |   \   |   x   |   x   |
# class     |   x   |   \   |   x   |
# align     |   X   |   x   |   \   |

class_align_count = {}
align_class_count = {}

race_class_count = {}
class_race_count = {}

race_align_count = {}
align_race_count = {}

# Generate dicts to use for the JSON
def class_align(data,char):
    aux_align = data[char]['alignment'][0]
    for char_class in data[char]['class']:
        if char_class in CLASSES:
            if aux_align != 'None':
                if char_class not in class_align_count:
                    class_align_count[char_class] = {aux_align:1}
                else:
                    if aux_align not in class_align_count[char_class]:
                        class_align_count[char_class][aux_align] = 1
                    else:
                        class_align_count[char_class][aux_align] += 1

def align_class(data,char):
    aux_align = data[char]['alignment'][0]
    if aux_align != 'None':
        for char_class in data[char]['class']:
            if char_class in CLASSES:
                if aux_align not in align_class_count:
                    align_class_count[aux_align] = {char_class:1}
                else:
                    if char_class not in align_class_count[aux_align]:
                        align_class_count[aux_align][char_class] = 1
                    else:
                        align_class_count[aux_align][char_class] += 1

def class_race(data,char):
    aux_race = data[char]['race'][0]
    for char_class in data[char]['class']:
        if char_class in CLASSES:
            if aux_race != '':
                if char_class not in class_race_count:
                    class_race_count[char_class] = {aux_race:1}
                else:
                    if aux_race not in class_race_count[char_class]:
                        class_race_count[char_class][aux_race] = 1
                    else:
                        class_race_count[char_class][aux_race] += 1

def race_class(data,char):
    aux_race = data[char]['race'][0]
    if aux_race != '':
        for char_class in data[char]['class']:
            if char_class in CLASSES:
                if aux_race not in race_class_count:
                    race_class_count[aux_race] = {char_class:1}
                else:
                    if char_class not in race_class_count[aux_race]:
                        race_class_count[aux_race][char_class] = 1
                    else:
                        race_class_count[aux_race][char_class] += 1

def race_align(data,char):
    aux_race = data[char]['race'][0]
    aux_align = data[char]['alignment'][0]
    if aux_race != '':
        if aux_align != 'None':
            if aux_race not in race_align_count:
                race_align_count[aux_race] = {aux_align:1}
            else:
                if aux_align not in race_align_count[aux_race]:
                    race_align_count[aux_race][aux_align] = 1
                else:
                    race_align_count[aux_race][aux_align] += 1

def align_race(data,char):
    aux_race = data[char]['race'][0]
    aux_align = data[char]['alignment'][0]
    if aux_race != '':
        if aux_align != 'None':
            if aux_align not in align_race_count:
                align_race_count[aux_align] = {aux_race:1}
            else:
                if aux_race not in align_race_count[aux_align]:
                    align_race_count[aux_align][aux_race] = 1
                else:
                    align_race_count[aux_align][aux_race] += 1

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
        class_align(data,character)
        align_class(data,character)
        race_class(data,character)
        class_race(data,character)
        race_align(data,character)
        align_race(data,character)
    # Create and append the network JSON structure to a JSON file
    class_align_json = {}
    class_race_json = {}
    for fun_class in CLASSES:
        class_align_json[fun_class] = create_json(fun_class,class_align_count)
        class_race_json[fun_class] = create_json(fun_class,class_race_count)
    new_json['Class_Alignment'] = class_align_json
    new_json['Class_Race'] = class_race_json
    
    race_class_json = {}
    race_align_json = {}
    for fun_race in RACES:
        race_class_json[fun_race] = create_json(fun_race, race_class_count)
        race_align_json[fun_race] = create_json(fun_race, race_align_count)
    new_json['Race_Class'] = race_class_json
    new_json['Race_Alignment'] = race_align_json

    align_class_json = {}
    align_race_json = {}
    for fun_align in ALIGNS:
        align_class_json[fun_align] = create_json(fun_align,align_class_count)
        align_race_json[fun_align] = create_json(fun_align,align_race_count)
    new_json['Alignment_Class'] = align_class_json
    new_json['Alignment_Race'] = align_race_json


with open('network_all_data.json',"w") as f:
    json.dump(new_json,f,indent=2)