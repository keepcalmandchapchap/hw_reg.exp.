import csv
import re
from collections import defaultdict


def sort_full_names(data_list): 
    for data in data_list:
        field1 = data[0].split()
        if len(field1) == 2:
            data[0] = field1[0]
            data[1] = field1[1]
        elif len(field1) == 3:
            data[0] = field1[0]
            data[1] = field1[1]
            data[2] = field1[2]
        field2 = data[1].split()
        if len(field2) == 2:
            data[1] = field2[0]
            data[2] = field2[1]
    return data_list

def make_text(data_list):
    sent_list = []
    for words in data_list:
        sent_list.append('/'.join(words))
    contacts_text = '!'.join(sent_list)
    return contacts_text

def format_numbers(text):
    pattern_for_number = r'([\+7|8]+)[\-\s]*\(*(\d{3})\)*[\-\s]*(\d{3})[\-\s]*(\d{2})[\-\s]*(\d{2})' # регулярка для номеров, не учитывая добавочные
    mid_text = re.sub(pattern_for_number, r'+7(\2)\3-\4-\5', text)
    pattern_for_supplement = r'\(*доб\.*\s*(\d+)\)*' #регулярка для добавочных
    result_text = re.sub(pattern_for_supplement, r'доб.\1.', mid_text)
    return result_text

def make_data_lists(text):
    raw_list = text.split('!')
    unformatted_list = []
    for row in raw_list:
        unformatted_list.append(row.split('/'))
    tables = unformatted_list.pop(0)
    return [unformatted_list, tables]

def create_defaultdict(data_list):
    data_dict = defaultdict(list)
    for d in data_list[1:]:
        if d[2] != '':
            key = ' '.join(d[:3])
            data = d[3:]
            data_dict[key].append(data)
    return data_dict

def unite_doubles(defdict):
    for full_name, info in defdict.items():
        if len(info) > 1:
            zipped_info = zip(info[0], info[1])
            list_info = list(zipped_info)
            formatted_list = []
            # print(list_info)
            for t in list_info:
                l = list(t)
                if '' in l:
                    l.remove('')
                elif l[0] == l[1]:
                    l.pop(1)
                formatted_list.append(''.join(l))
            defdict[full_name] = [formatted_list]
    return defdict

def format_result(defdict, tables):
    final_list = []
    final_list.append(tables)
    for key, values in defdict.items():
        person_list = []
        full_name = key.split(' ')
        person_list += full_name + values[0]
        final_list.append(person_list)
    return final_list


def main():
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    data_list = sort_full_names(contacts_list)

    data_text = make_text(data_list)

    formatted_text = format_numbers(data_text)

    data_list = make_data_lists(formatted_text)

    raw_data_dict = create_defaultdict(data_list[0])

    data_dict = unite_doubles(raw_data_dict)

    result_list = format_result(data_dict, data_list[1])

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(result_list)


if __name__ == '__main__':
    main()







