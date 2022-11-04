import json
from datetime import datetime
import copy

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

COUNTRIES = ['CA','US','BR','AU','GB','IT','DE']
ALIGNS = ['CG','CN','LG','NG','LN','LE','CE','NN','NE']
ATTRIBUTES = ['HP','AC','Str','Dex','Con','Int','Wis','Cha']
YEARS = ['2018','2019','2020','2021','2022','All']
SKILLS = []

filename = "python_datasets/cleaned/dnd_chars_all_cleaned.json"

class_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
race_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
skill_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
combo_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}


def attr_sctructure(item,item_count,year,hp,ac,stre,dex,con,inte,wis,cha,country):
    if item not in item_count[year][country]:
        item_count[year][country][item] = {'HP':hp,'AC':ac,'Str':stre,'Dex':dex,'Con':con,'Int':inte,'Wis':wis,'Cha':cha,'Total':1}
    else:
        item_count[year][country][item]['HP'] += hp
        item_count[year][country][item]['AC'] += ac
        item_count[year][country][item]['Str'] += stre
        item_count[year][country][item]['Dex'] += dex
        item_count[year][country][item]['Con'] += con
        item_count[year][country][item]['Int'] += inte
        item_count[year][country][item]['Wis'] += wis
        item_count[year][country][item]['Cha'] += cha
        item_count[year][country][item]['Total'] += 1
        
# Generate dicts to use for the JSON
def data_to_radar(data,char,year):
    a,b,c,d,e,f = data[char]['attributes'].values()
    stre = a[0]
    dex = b[0]
    con = c[0]
    inte = d[0]
    wis = e[0]
    cha = f[0]
    hp = data[char]['HP'][0]
    ac = data[char]['AC'][0]
    race = data[char]['race'][0]
    skills = data[char]['skills']
    country = data[char]['location'][0]
    if country not in COUNTRIES: country = 'Other'

    for char_class in data[char]['class']:
        if char_class in CLASSES:
            combo_name = char_class + '_' + race
        else:
            char_class = 'Custom'
            combo_name = char_class + '_' + race

        attr_sctructure(char_class,class_count,'All',hp,ac,stre,dex,con,inte,wis,cha,country)
        attr_sctructure(char_class,class_count,'All',hp,ac,stre,dex,con,inte,wis,cha,'All')
        attr_sctructure(char_class,class_count,year,hp,ac,stre,dex,con,inte,wis,cha,country)
        attr_sctructure(char_class,class_count,year,hp,ac,stre,dex,con,inte,wis,cha,'All')       
        
        attr_sctructure(combo_name,combo_count,'All',hp,ac,stre,dex,con,inte,wis,cha,country)
        attr_sctructure(combo_name,combo_count,'All',hp,ac,stre,dex,con,inte,wis,cha,'All')
        attr_sctructure(combo_name,combo_count,year,hp,ac,stre,dex,con,inte,wis,cha,country)
        attr_sctructure(combo_name,combo_count,year,hp,ac,stre,dex,con,inte,wis,cha,'All')       

    # Just to colapse the entire race section
    if 1==1:
        attr_sctructure(race,race_count,'All',hp,ac,stre,dex,con,inte,wis,cha,country)
        attr_sctructure(race,race_count,'All',hp,ac,stre,dex,con,inte,wis,cha,'All')
        attr_sctructure(race,race_count,year,hp,ac,stre,dex,con,inte,wis,cha,country)
        attr_sctructure(race,race_count,year,hp,ac,stre,dex,con,inte,wis,cha,'All')

    for skill in skills:
        if skill != 'None':
            if skill not in SKILLS:
                SKILLS.append(skill)
            attr_sctructure(skill,skill_count,'All',hp,ac,stre,dex,con,inte,wis,cha,country)
            attr_sctructure(skill,skill_count,'All',hp,ac,stre,dex,con,inte,wis,cha,'All')
            attr_sctructure(skill,skill_count,year,hp,ac,stre,dex,con,inte,wis,cha,country)
            attr_sctructure(skill,skill_count,year,hp,ac,stre,dex,con,inte,wis,cha,'All')

def cal_mean(dict_mean):
    for year in YEARS:
        stre,dex,con,inte,wis,cha,hp,ac,total_elements = 0,0,0,0,0,0,0,0,0
        for country in dict_mean[year]:
            for element in dict_mean[year][country]:
                total = dict_mean[year][country][element]['Total']
                dict_mean[year][country][element]['HP'] = round(dict_mean[year][country][element]['HP']/total)
                dict_mean[year][country][element]['AC'] = round(dict_mean[year][country][element]['AC']/total)
                dict_mean[year][country][element]['Str'] = round(dict_mean[year][country][element]['Str']/total)
                dict_mean[year][country][element]['Dex'] = round(dict_mean[year][country][element]['Dex']/total)
                dict_mean[year][country][element]['Con'] = round(dict_mean[year][country][element]['Con']/total)
                dict_mean[year][country][element]['Int'] = round(dict_mean[year][country][element]['Int']/total)
                dict_mean[year][country][element]['Wis'] = round(dict_mean[year][country][element]['Wis']/total)
                dict_mean[year][country][element]['Cha'] = round(dict_mean[year][country][element]['Cha']/total)
                del dict_mean[year][country][element]['Total']
                hp += dict_mean[year][country][element]['HP'] 
                ac += dict_mean[year][country][element]['AC'] 
                stre += dict_mean[year][country][element]['Str']
                dex += dict_mean[year][country][element]['Dex']
                con += dict_mean[year][country][element]['Con']
                inte += dict_mean[year][country][element]['Int']
                wis += dict_mean[year][country][element]['Wis']
                cha += dict_mean[year][country][element]['Cha']
                total_elements += 1
            dict_mean[year][country]['Mean'] = {'HP':round(hp/total_elements),
            'AC':round(ac/total_elements),'Str':round(stre/total_elements),'Dex':round(dex/total_elements),
            'Con':round(con/total_elements),'Int':round(inte/total_elements),'Wis':round(wis/total_elements),
            'Cha':round(cha/total_elements)}

# Generate JSONS structures
def dict_to_json(dictJson):
    for year in YEARS:
        for country in COUNTRIES:
            for name in dictJson[year][country]:
                aux_arr = []
                for attr in dictJson[year][country][name]:
                    aux_arr.append({'axis':attr,'value':dictJson[year][country][name][attr]})
                aux = {'name':name,'axes':aux_arr}
                dictJson[year][country][name] = aux

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

def dontExit():
    for aux in new_json:
        global_var = getGlobalVar(aux)
        for year in YEARS:
            for country in COUNTRIES:
                keys_list = list(new_json[aux][year][country].keys())
                for ind_key in global_var:
                    if ind_key not in keys_list:
                        axis = [{'axis':'HP','value':0},{'axis':'AC','value':0},
                        {'axis':'Str','value':0},
                        {'axis':'Dex','value':0},
                        {'axis':'Con','value':0},
                        {'axis':'Int','value':0},
                        {'axis':'Wis','value':0},
                        {'axis':'Cha','value':0}]
                        radar_struct = {'name':ind_key,'axes':axis}
                        new_json[aux][year][country][ind_key] = radar_struct

total_min_max = {}
copyDict = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
min_max = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}
def getMinMax():  
    for aux in new_json:
        total_min_max[aux] = copy.deepcopy(copyDict)
        for year in YEARS:
            for country in COUNTRIES:
                tmp_min = {'HP':99,'AC':99,'Str':99,'Dex':99,'Con':99,'Int':99,'Wis':99,'Cha':99}
                tmp_max = {'HP':0,'AC':0,'Str':0,'Dex':0,'Con':0,'Int':0,'Wis':0,'Cha':0}
                keys_min = {'HP':99,'AC':99,'Str':99,'Dex':99,'Con':99,'Int':99,'Wis':99,'Cha':99}
                keys_max = {'HP':0,'AC':0,'Str':0,'Dex':0,'Con':0,'Int':0,'Wis':0,'Cha':0}
                for char in new_json[aux][year][country]:
                    for attr in new_json[aux][year][country][char]['axes']:
                        attr_n = attr['axis']
                        attr_v = attr['value']
                        if tmp_min[attr_n] > attr_v:
                            tmp_min[attr_n] = attr_v
                            keys_min[attr_n] = char
                        if tmp_max[attr_n] < attr_v:
                            tmp_max[attr_n] = attr_v
                            keys_max[attr_n] = char
                total_min_max[aux][year][country] = {'min':keys_min,'max':keys_max}
                            
#----------Main------------
with open(filename,"r",encoding="utf-8") as f:
    data = json.load(f)
    new_json = {}
    for character in data:
        year = (str((datetime.strptime(data[character]['date'][0], '%Y-%m-%d %H:%M:%S')).year))
        data_to_radar(data,character,year)

    cal_mean(class_count)
    cal_mean(race_count)
    cal_mean(skill_count)
    cal_mean(combo_count)
    
    COUNTRIES.append('Other')
    COUNTRIES.append('All')

    # Create and append the network JSON structure to a JSON file
    dict_to_json(class_count)
    dict_to_json(race_count)
    dict_to_json(skill_count)
    dict_to_json(combo_count)

    new_json['class'] = class_count
    new_json['race'] = race_count
    new_json['skill'] = skill_count
    new_json['combo'] = combo_count
    dontExit()
    getMinMax()

with open('resources/datasets/radar_data.json',"w") as f:
    json.dump(new_json,f,indent=2)
with open('resources/datasets/radar_data_min_max.json',"w") as f:
    json.dump(total_min_max,f,indent=2)