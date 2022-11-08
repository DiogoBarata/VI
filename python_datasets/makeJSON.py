import json
from datetime import datetime
import operator

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
SKILLS = []
FEATS = []

filename = "python_datasets/cleaned/dnd_chars_all_cleaned.json"

# relations |race   |class  |align  |combo  |skill  |feats  |
# race      |   \   |   x   |   x   |   \   |   x   |   x   |
# class     |   x   |   \   |   x   |   \   |   x   |   x   |
# align     |   \   |   \   |   \   |   \   |   \   |   \   |
# combo     |   \   |   \   |   x   |   \   |   x   |   x   |
# skill     |   x   |   x   |   x   |   x   |   \   |   \   |
# feats     |   \   |   \   |   \   |   \   |   \   |   \   |

race_class_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
class_race_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}

race_skill_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
skill_race_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}

class_skill_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
skill_class_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}

combo_skill_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
skill_combo_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}

class_align_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
race_align_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
combo_align_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
skill_align_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}

race_feat_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
class_feat_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
combo_feat_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
skill_feat_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}


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
    skills = char['skills']
    feats = char['feats']
    if race not in RACES: race = 'Custom'
    if country not in COUNTRIES: country = 'Other'
    if align not in ALIGNS: align_continue = False
    for char_class in char['class']:
        if race in RACES:
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
            #combo_align
            attr_sctructure(combo_name,align,combo_align_count,'All','All')
            attr_sctructure(combo_name,align,combo_align_count,'All',country)
            attr_sctructure(combo_name,align,combo_align_count,year,'All')
            attr_sctructure(combo_name,align,combo_align_count,year,country)
        
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
        
        #skills
        for skill in skills:
            if skill != 'None':
                #class_skill
                attr_sctructure(char_class,skill,class_skill_count,'All','All')
                attr_sctructure(char_class,skill,class_skill_count,'All',country)
                attr_sctructure(char_class,skill,class_skill_count,year,'All')
                attr_sctructure(char_class,skill,class_skill_count,year,country)
                #skill_class
                attr_sctructure(skill,char_class,skill_class_count,'All','All')
                attr_sctructure(skill,char_class,skill_class_count,'All',country)
                attr_sctructure(skill,char_class,skill_class_count,year,'All')
                attr_sctructure(skill,char_class,skill_class_count,year,country)
                #combo_skill
                attr_sctructure(combo_name,skill,combo_skill_count,'All','All')
                attr_sctructure(combo_name,skill,combo_skill_count,'All',country)
                attr_sctructure(combo_name,skill,combo_skill_count,year,'All')
                attr_sctructure(combo_name,skill,combo_skill_count,year,country)
                #skill_combo
                attr_sctructure(skill,combo_name,skill_combo_count,'All','All')
                attr_sctructure(skill,combo_name,skill_combo_count,'All',country)
                attr_sctructure(skill,combo_name,skill_combo_count,year,'All')
                attr_sctructure(skill,combo_name,skill_combo_count,year,country)
        
        #feats
        for feat in feats:
            if feat != 'None':
                #class_feat
                attr_sctructure(char_class,feat,class_feat_count,'All','All')
                attr_sctructure(char_class,feat,class_feat_count,'All',country)
                attr_sctructure(char_class,feat,class_feat_count,year,'All')
                attr_sctructure(char_class,feat,class_feat_count,year,country)
                #combo_feat
                attr_sctructure(combo_name,feat,combo_feat_count,'All','All')
                attr_sctructure(combo_name,feat,combo_feat_count,'All',country)
                attr_sctructure(combo_name,feat,combo_feat_count,year,'All')
                attr_sctructure(combo_name,feat,combo_feat_count,year,country)

    #skills
    for skill in skills:
        if skill != 'None':
            if skill not in SKILLS:
                SKILLS.append(skill)
            #skill_race
            attr_sctructure(skill,race,skill_race_count,'All','All')
            attr_sctructure(skill,race,skill_race_count,'All',country)
            attr_sctructure(skill,race,skill_race_count,year,'All')
            attr_sctructure(skill,race,skill_race_count,year,country)
            #race_skill
            attr_sctructure(race,skill,race_skill_count,'All','All')
            attr_sctructure(race,skill,race_skill_count,'All',country)
            attr_sctructure(race,skill,race_skill_count,year,'All')
            attr_sctructure(race,skill,race_skill_count,year,country)

    
    #feats
    for feat in feats:
        if feat != 'None':
            if feat not in FEATS:
                FEATS.append(feat)
            #race_feat
            attr_sctructure(race,feat,race_feat_count,'All','All')
            attr_sctructure(race,feat,race_feat_count,'All',country)
            attr_sctructure(race,feat,race_feat_count,year,'All')
            attr_sctructure(race,feat,race_feat_count,year,country)
            for skill in skills:
                if skill != 'None':
                    attr_sctructure(skill,feat,skill_feat_count,'All','All')
                    attr_sctructure(skill,feat,skill_feat_count,'All',country)
                    attr_sctructure(skill,feat,skill_feat_count,year,'All')
                    attr_sctructure(skill,feat,skill_feat_count,year,country)
    
    if align_continue:
        for skill in skills:
            if skill != 'None':
                #skill_align
                attr_sctructure(skill,align,skill_align_count,'All','All')
                attr_sctructure(skill,align,skill_align_count,'All',country)
                attr_sctructure(skill,align,skill_align_count,year,'All')
                attr_sctructure(skill,align,skill_align_count,year,country)

        #race_align
        attr_sctructure(race,align,race_align_count,'All','All')
        attr_sctructure(race,align,race_align_count,'All',country)
        attr_sctructure(race,align,race_align_count,year,'All')
        attr_sctructure(race,align,race_align_count,year,country)

# Generate JSONS structures
def network_json(center,count_dict):
    id = 1
    network_struct = {'nodes':[],'links':[]}
    network_struct['nodes'].append({'id':id,'name':center})
    id +=1
    sorted_d = dict( sorted(count_dict[center].items(), key=operator.itemgetter(1),reverse=True))
    for rel in sorted_d:
        if id > 11:
            break
        distance = 15 * (1/count_dict[center][rel])+1
        network_struct['nodes'].append({'id':id,'name':rel})
        network_struct['links'].append({'source':1,'target':id,'distance':distance})
        id+=1
    return network_struct

def counts_json(new_json,count_dict,rel):
    # Create and append the network JSON structure to a JSON file
    first_json = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
    for year in YEARS:
        for country in COUNTRIES:
            for fun_var in count_dict[year][country]:
                first_json[year][country][fun_var]=network_json(fun_var,count_dict[year][country])
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
    if text == 'skill':
        return SKILLS
    if text == 'feat':
        return FEATS

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
    counts_json(new_json,class_race_count,'class_race')
    counts_json(new_json,race_class_count,'race_class')
    counts_json(new_json,class_skill_count,'class_skill')
    counts_json(new_json,skill_class_count,'skill_class')
    counts_json(new_json,race_skill_count,'race_skill')
    counts_json(new_json,skill_race_count,'skill_race')
    counts_json(new_json,combo_skill_count,'combo_skill')
    counts_json(new_json,skill_combo_count,'skill_combo')
    counts_json(new_json,class_align_count,'class_alignment')
    counts_json(new_json,race_align_count,'race_alignment')
    counts_json(new_json,combo_align_count,'combo_alignment')
    counts_json(new_json,skill_align_count,'skill_alignment')
    counts_json(new_json,class_feat_count,'class_feat')
    counts_json(new_json,race_feat_count,'race_feat')
    counts_json(new_json,combo_feat_count,'combo_feat')
    counts_json(new_json,skill_feat_count,'skill_feat')
    dontExit()


with open('resources/datasets/network_data.json',"w") as f:
    json.dump(new_json,f,indent=2)