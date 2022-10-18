from http.client import BAD_REQUEST
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
        }, 
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
ALIGNS=['CG''CN''LG''NG''LN', 'LE', 'CE', 'NN', 'NE']
VARS = ["class","alignment"]
filename = "datasets/cleaned/dnd_chars_all_cleaned.json"

class_align_count = {}
class_count = {'Others':0}
align_count = {}
new_json = {'nodes':[],'links':[]}

def class_align(data,char):
    for char_class in data[char]['class']:
        if char_class in CLASSES:
            if data[char]['alignment'] != ['None']:
                if char_class not in class_align_count:
                    class_align_count[char_class] = {data[char]['alignment'][0]:1}
                else:
                    if data[char]['alignment'][0] not in class_align_count[char_class]:
                        class_align_count[char_class][data[char]['alignment'][0]] = 1
                    else:
                        class_align_count[char_class][data[char]['alignment'][0]] += 1

def count(data,char):
    for char_class in data[char]['class']:
        if char_class in CLASSES:
            if char_class not in class_count:
                class_count[char_class] = 1
            else:
                class_count[char_class] += 1
        else:
            class_count['Others'] += 1
        
        if data[char]['alignment'][0] not in align_count:
            align_count[data[char]['alignment'][0]] = 1
        else:
            align_count[data[char]['alignment'][0]] += 1

    print(dict(sorted(class_count.items(), key=lambda item: item[1])))
    print(align_count)

"""
{
  "nodes": [
    {
      "id": 1,
      "name": "A"
    },
    {
      "id": 2,
      "name": "B"
    }],
  "links": [
    {
      "source": 1,
      "target": 2
    },
    {
      "source": 1,
      "target": 5
    },

"""
def class_align_json(one_class):
    relation = list(class_align_count[one_class].keys())
    id = 1
    
    new_json['nodes'].append({'id':id,'name':one_class})
    id +=1
    for rel in relation:
        new_json['nodes'].append({'id':id,'name':rel})
        print(class_align_count[one_class])
        print(class_align_count[one_class][rel])
        new_json['links'].append({'source':1,'target':id,'distance':class_align_count[one_class][rel]})
        id+=1
    
    print(new_json)

with open(filename,"r",encoding="utf-8") as f:
    data = json.load(f)
    for character in data:
        class_align(data,character)
    
    class_align_json('Fighter')

with open('network_data.json',"w") as f:
    json.dump(new_json,f)