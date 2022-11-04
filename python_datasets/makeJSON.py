import json
from datetime import datetime

CLASSES = ['Artificer','Barbarian','Bard','Cleric','Druid','Fighter','Monk','Paladin',
    'Ranger','Rogue','Sorcerer','Warlock','Wizard']
RACES = ['Aarakocra', 'Aasimar', 'Bugbear', 'Centaur', 'Changeling', 'Custom', 
    'Dragonborn', 'Dwarf', 'Eladrin', 'Elf', 'Firbolg', 'Genasi', 'Gith', 'Gnome', 
    'Goblin', 'Goliath', 'Half-Elf', 'Half-Orc', 'Halfling', 'Hobgoblin', 'Human', 
    'Kalashtar', 'Kenku', 'Kobold', 'Leonin', 'Lizardfolk', 'Loxodon', 'Minotaur', 
    'Orc', 'Satyr', 'Shifter', 'Simic hybrid', 'Tabaxi', 'Tiefling', 'Triton', 
    'Turtle', 'Vedalken', 'Warforged', 'Yaun-Ti']
COMBOS = []
for c in CLASSES:
    for r in RACES:
        COMBOS.append(c+'_'+r)

ALIGNS = ['CG','CN','LG','NG','LN','LE','CE','NN','NE']
YEARS = ['2018','2019','2020','2021','2022','All']
COUNTRIES = ['CA','US','BR','AU','GB','IT','DE']

filename = "python_datasets/cleaned/dnd_chars_all_cleaned.json"

# relations |race   |class  |align  |combo  |
# race      |   \   |   x   |   x   |   \   |
# class     |   x   |   \   |   x   |   \   |
# align     |   X   |   x   |   \   |       |
# combo     |   \   |   \   |       |   \   |

class_align_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
align_class_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}

race_class_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
class_race_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}

race_align_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
align_race_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}

combo_align_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
align_combo_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}

DICTS = [class_align_count,align_class_count,race_class_count,class_race_count,race_align_count,
align_race_count,combo_align_count,align_combo_count]
# Generate dicts to use for the JSON
def attr_sctructure(centre,rel,dict_count,year,country):
    if centre not in dict_count[year][country]:
        dict_count[year][country][centre] = {rel:1}
    else:
        if rel not in dict_count[year][country][centre]:
            dict_count[year][country][centre][rel] = 1
        else:
            dict_count[year][country][centre][rel] += 1

def data_to_network(char,year):
    align = char['alignment'][0]
    align_continue = True
    race = char['race'][0]
    country = char['location'][0]
    if country not in COUNTRIES: country = 'Other'
    if align not in ALIGNS: align_continue = False
    for char_class in char['class']:
        if char_class in CLASSES:
            combo_name = char_class + '_' + race
        else:
            char_class = 'Custom'
            combo_name = char_class + '_' + race
        
        if align_continue:
            #class_align
            attr_sctructure(char_class,align,class_align_count,'All','All')
            attr_sctructure(char_class,align,class_align_count,'All',country)
            attr_sctructure(char_class,align,class_align_count,year,'All')
            attr_sctructure(char_class,align,class_align_count,year,country)
            #align_class
            attr_sctructure(align,char_class,align_class_count,'All','All')
            attr_sctructure(align,char_class,align_class_count,'All',country)
            attr_sctructure(align,char_class,align_class_count,year,'All')
            attr_sctructure(align,char_class,align_class_count,year,country)
            #combo_align
            attr_sctructure(combo_name,align,combo_align_count,'All','All')
            attr_sctructure(combo_name,align,combo_align_count,'All',country)
            attr_sctructure(combo_name,align,combo_align_count,year,'All')
            attr_sctructure(combo_name,align,combo_align_count,year,country)
            #align_combo
            attr_sctructure(align,combo_name,align_combo_count,'All','All')
            attr_sctructure(align,combo_name,align_combo_count,'All',country)
            attr_sctructure(align,combo_name,align_combo_count,year,'All')
            attr_sctructure(align,combo_name,align_combo_count,year,country)
        
        #class_race
        attr_sctructure(char_class,race,class_race_count,'All','All')
        attr_sctructure(char_class,race,class_race_count,'All',country)
        attr_sctructure(char_class,race,class_race_count,year,'All')
        attr_sctructure(char_class,race,class_race_count,year,country)
        #race_class
        attr_sctructure(race,char_class,race_class_count,'All','All')
        attr_sctructure(race,char_class,race_class_count,'All',country)
        attr_sctructure(race,char_class,race_class_count,year,'All')
        attr_sctructure(race,char_class,race_class_count,year,country)

    if align_continue:
        #align_race
        attr_sctructure(align,race,align_race_count,'All','All')
        attr_sctructure(align,race,align_race_count,'All',country)
        attr_sctructure(align,race,align_race_count,year,'All')
        attr_sctructure(align,race,align_race_count,year,country)
        #race_align
        attr_sctructure(race,align,race_align_count,'All','All')
        attr_sctructure(race,align,race_align_count,'All',country)
        attr_sctructure(race,align,race_align_count,year,'All')
        attr_sctructure(race,align,race_align_count,year,country)

# Generate JSONS structures
def network_json(center,count_dict):
    relation = list(count_dict[center].keys())
    id = 1
    network_struct = {'nodes':[],'links':[]}
    network_struct['nodes'].append({'id':id,'name':center})
    id +=1
    for rel in relation:
        network_struct['nodes'].append({'id':id,'name':rel})
        network_struct['links'].append({'source':1,'target':id,'distance':count_dict[center][rel]})
        id+=1
    return network_struct

def counts_json(new_json,count1,rel):
    # Create and append the network JSON structure to a JSON file
    first_json = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
    for year in YEARS:
        for country in COUNTRIES:
            for fun_var in count1[year][country]:
                first_json[year][country][fun_var]=network_json(fun_var,count1[year][country])
    new_json[rel] = first_json

def getGlobalVar(text):
    if text == 'class':
        return CLASSES
    if text == 'alignment':
        return ALIGNS
    if text == 'race':
        return RACES
    if text == 'combo':
        return COMBOS

def dontExit():
    for aux in new_json:
        main_key = aux.split('_')[0]
        global_var = getGlobalVar(main_key)
        for year in YEARS:
            for country in COUNTRIES:
                keys_list = list(new_json[aux][year][country].keys())
                for ind_key in global_var:
                    if ind_key not in keys_list:
                        network_struct = {'nodes':[{'id':1,'name':ind_key}],'links':[{'source':1,'target':1,'distance':1}]}
                        new_json[aux][year][country][ind_key] = network_struct

#----------Main------------
with open(filename,"r",encoding="utf-8") as f:
    data = json.load(f)
    new_json = {}
    for character in data:
        year = (str((datetime.strptime(data[character]['date'][0], '%Y-%m-%d %H:%M:%S')).year))
        data_to_network(data[character],year)

    # Create and append the network JSON structure to a JSON file
    COUNTRIES.append('All')
    COUNTRIES.append('Other')
    CLASSES.append('Custom')
    counts_json(new_json,class_align_count,'class_alignment')
    counts_json(new_json,align_class_count,'alignment_class')
    counts_json(new_json,class_race_count,'class_race')
    counts_json(new_json,race_class_count,'race_class')
    counts_json(new_json,align_race_count,'alignment_race')
    counts_json(new_json,race_align_count,'race_alignment')
    counts_json(new_json,align_combo_count,'alignment_combo')
    counts_json(new_json,combo_align_count,'combo_alignment')
    dontExit()


with open('resources/datasets/network_data.json',"w") as f:
    json.dump(new_json,f,indent=2)