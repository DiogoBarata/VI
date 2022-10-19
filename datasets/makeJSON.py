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
ALIGNS=['CG','CN','LG','NG','LN','LE','CE','NN','NE']
VARS = ["class","alignment"]
filename = "datasets/cleaned/dnd_chars_all_cleaned.json"

class_align_count = {}
align_class_count = {}


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


def class_align_json(one_class):
    relation = list(class_align_count[one_class].keys())
    id = 1
    network_json = {'nodes':[],'links':[]}
    network_json['nodes'].append({'id':id,'name':one_class})
    id +=1
    for rel in relation:
        network_json['nodes'].append({'id':id,'name':rel})
        network_json['links'].append({'source':1,'target':id,'distance':class_align_count[one_class][rel]*5})
        id+=1
    return network_json

def align_class_json(one_align):
    relation = list(align_class_count[one_align].keys())
    id = 1
    network_json = {'nodes':[],'links':[]}
    network_json['nodes'].append({'id':id,'name':one_align})
    id +=1
    for rel in relation:
        network_json['nodes'].append({'id':id,'name':rel})
        network_json['links'].append({'source':1,'target':id,'distance':align_class_count[one_align][rel]})
        id+=1
    return network_json


with open(filename,"r",encoding="utf-8") as f:
    data = json.load(f)
    new_json = {'Class_Align':None}
    
    for character in data:
        class_align(data,character)
        align_class(data,character)
    
    tmp_json = {}
    for fun_class in CLASSES:
        tmp_json[fun_class] = class_align_json(fun_class)
    new_json['Class_Align'] = tmp_json

    tmp_json = {}
    for fun_align in ALIGNS:
        tmp_json[fun_align] = align_class_json(fun_align)
    new_json['Align_Class'] = tmp_json



with open('network_all_data.json',"w") as f:
    json.dump(new_json,f, indent=3)