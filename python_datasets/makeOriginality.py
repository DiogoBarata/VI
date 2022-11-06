import json
from datetime import datetime

CLASSES = ['Artificer','Barbarian','Bard','Cleric','Druid','Fighter','Monk','Paladin',
    'Ranger','Rogue','Sorcerer','Warlock','Wizard','Custom']
ALIGNS = ['CG','CN','LG','NG','LN','LE','CE','NN','NE']
RACES = ['Aarakocra', 'Aasimar', 'Bugbear', 'Centaur', 'Changeling', 'Custom', 
    'Dragonborn', 'Dwarf', 'Eladrin', 'Elf', 'Firbolg', 'Genasi', 'Gith', 'Gnome', 
    'Goblin', 'Goliath', 'Half-Elf', 'Half-Orc', 'Halfling', 'Hobgoblin', 'Human', 
    'Kalashtar', 'Kenku', 'Kobold', 'Leonin', 'Lizardfolk', 'Loxodon', 'Minotaur', 
    'Orc', 'Satyr', 'Shifter', 'Simic hybrid', 'Tabaxi', 'Tiefling', 'Triton', 
    'Turtle', 'Vedalken', 'Warforged', 'Yaun-Ti']
COMBOS = []
for tmp_class in CLASSES:
    for tmp_race in RACES:
        COMBOS.append(tmp_class+'_'+tmp_race)
YEARS = ['2018','2019','2020','2021','2022','All']
COUNTRIES = ['CA','US','BR','AU','GB','IT','DE']

filename = "python_datasets/cleaned/dnd_chars_all_cleaned.json"


original_count = {'All':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2018':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2019':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2020':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2021':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}},'2022':{'All':{},'CA':{},'US':{},'BR':{},'AU':{},'GB':{},'IT':{},'DE':{},'Other':{}}}

count_races = {}
# Generate dicts to use for the JSON
def attr_sctructure(centre,dict_count,year,country):
    if centre not in dict_count[year][country]:
        dict_count[year][country][centre] = 1
    else:
        dict_count[year][country][centre] += 1

def cal_org(count_dict,year,country):
    count = sum(count_dict[year][country].values())
    min_org = 9999999
    max_org = 0
    for elem in count_dict[year][country]:
        curr_orig = 1/(count_dict[year][country][elem]/count)
        count_dict[year][country][elem] = curr_orig
        if max_org < curr_orig:
            max_org = curr_orig
        if min_org > curr_orig:
            min_org = curr_orig
    count_dict[year][country]['Min'] = min_org
    count_dict[year][country]['Max'] = max_org

def addNotUsed(count_dict,year,country):
    for aux_combo in COMBOS:
        if aux_combo not in list(count_dict[year][country].keys()):
            count_dict[year][country][aux_combo] = count_dict[year][country]['Max']
def data_to_network(char,year):
    race = char['race'][0]
    country = char['location'][0]
    if country not in COUNTRIES: country = 'Other'
    if race not in RACES: race = 'Custom'
    for char_class in char['class']:
        if char_class in CLASSES:
            combo_name = char_class + '_' + race
        else:
            char_class = 'Custom'
            combo_name = char_class + '_' + race
        
        attr_sctructure(combo_name,original_count,'All','All')
        attr_sctructure(combo_name,original_count,'All',country)
        attr_sctructure(combo_name,original_count,year,'All')
        attr_sctructure(combo_name,original_count,year,country)

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
    for year in YEARS:
        for country in COUNTRIES:
            # cal_org(original_count,'All','All')
            # cal_org(original_count,'All',country)
            # cal_org(original_count,year,'All')
            cal_org(original_count,year,country)
            addNotUsed(original_count,year,country)
    new_json = original_count

"""
{'Human': 2137, 'Elf': 1297, 'Half-Elf': 848, 'Dwarf': 718, 'Tiefling': 654, 'Halfling': 533, 'Dragonborn': 530, 'Half-Orc': 425, 'Gnome': 407, 'Aasimar': 337, 'Tabaxi': 320, '': 231, 'Warforged': 209, 'Goliath': 198, 'Genasi': 
193, 'Goblin': 181, 'Firbolg': 169, 'Turtle': 153, 'Kenku': 106, 'Lizardfolk': 106, 'Kobold': 104, 'Triton': 103, 
'Aarakocra': 99, 'Minotaur': 98, 'Bugbear': 82, 'Eladrin': 82, 'Yaun-Ti': 74, 'Orc': 69, 'Changeling': 61, 'Custom': 53, 'Loxodon': 50, 'Shifter': 40, 'Centaur': 37, 'Kalashtar': 34, 'Hobgoblin': 34, 'Simic hybrid': 30, 'Gith': 
28, 'Leonin': 26, 'Satyr': 25, 'Vedalken': 13}
"""
with open('resources/datasets/originality_data.json',"w") as f:
    json.dump(new_json,f,indent=2)