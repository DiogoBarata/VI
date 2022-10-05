import json

ATTRIBUTES = ['name','race','alignment','location']
TO_DELETE_SUB = ['hash','race','alignment','country']
TO_DELETE=['ip','finger','background','levelGroup','spells','weapons','castingStat','hash']

TO_COMPACT=['name','race','location']
SUB_COMPACT=['alias','processedRace','countryCode']

MISSING_VALUES_STR=['name','race','date','feats','alignment','skills','location']
SUB_MISSING_VALUES_STR=['processedAlignment','lawful','good']

MISSING_VALUES_INT=['level','HP','AC','attributes']
SUB_MISSING_VALUES_INT=["Str","Dex","Con","Int","Wis","Cha"]


# filename = "dnd_chars_all"
filename = "dnd_chars_unique"

with open(filename + ".json","r",encoding="utf-8") as f:
    data = json.load(f)
    class_count = {}
    race_count = {}
    for character in data:
        sub_index = 0
        comp_index=0

        for to_del in TO_DELETE:
            del data[character][to_del]
        for to_del in ATTRIBUTES:
            del data[character][to_del][TO_DELETE_SUB[sub_index]]
            sub_index += 1
        
        for compact in TO_COMPACT:
            data[character][compact] = data[character][compact][SUB_COMPACT[comp_index]]
            comp_index += 1

        for missing in MISSING_VALUES_STR:
            if missing == 'alignment':
                data[character][missing] = data[character][missing]['processedAlignment']
                if ((data[character][missing][0]) in (None,'')):
                    data[character][missing] = ['None']
            if not (bool(data[character][missing])):
                data[character][missing] = ['None']
        
        for missing in MISSING_VALUES_INT:
            if missing == 'attributes':
                for sub_missing in SUB_MISSING_VALUES_INT:
                    if not (bool(data[character][missing][sub_missing])):
                        data[character][missing][sub_missing] = [-1]    
                
            if not (bool(data[character][missing])):
                data[character][missing] = [-1]
            
        for char_class in data[character]['class']:   
            for option in data[character]['class'][char_class]:
                if not (bool(data[character]['class'][char_class][option])):
                    if option != 'level':
                        data[character]['class'][char_class][option] = ['None']
                    else:
                        data[character]['class'][char_class][option] = [-1]
            
            if char_class not in class_count:
                class_count[char_class] = 1
            else:
                class_count[char_class] += 1            

        if data[character]['race'][0] not in race_count:
            race_count[data[character]['race'][0]] = 1
        else:
            race_count[data[character]['race'][0]] += 1

    total_race = sum(race_count.values())
    total_class = sum(class_count.values())
    
    for item in race_count:
        race_count[item] = race_count[item]/total_race
    
    for item in class_count:
        class_count[item] = class_count[item]/total_class

    for character in data:
        current_race = data[character]['race'][0]
        
        for char_class in data[character]['class']:
            originality = (race_count[current_race] * class_count[char_class])
            tmp = {'originality': originality}
            (data[character]['class'][char_class]).update(tmp)
            


with open(filename + "_cleaned.json","w") as f:
    json.dump(data,f)
