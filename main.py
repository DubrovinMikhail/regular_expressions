import re

# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# lastname, firstname, surname correction
contacts_list_correct = []
for cont in contacts_list:
    inf = " ".join(cont[0:3]).strip().split()
    for i in range(3, 7):
        inf.append(cont[i])
    contacts_list_correct.append(inf)

# creating a dictionary list
COUNT = len(contacts_list_correct)
contacts_dict_list = []
for i in range(COUNT):
    contacts_dict_list.append(dict(zip(contacts_list_correct[0], contacts_list_correct[i])))
del contacts_dict_list[0]

# correcting email
for contact in contacts_dict_list:
    if "email" not in contact.keys():
        contact["email"] = ""
    email = contact["email"]
    for key in contact:
        if "@" in contact[key] and key != "email":
            email = contact[key]
            contact[key] = ""
    contact["email"] = email

# remove duplicate
contact_last_name = contacts_dict_list[0]["lastname"]
for i in range(COUNT):
    for j in range(i+1, COUNT-1):
        if contacts_dict_list[i]["lastname"] == contacts_dict_list[j]["lastname"]:
            for key in contacts_dict_list[i].keys():
                if contacts_dict_list[i][key] == "":
                    contacts_dict_list[i][key] = contacts_dict_list[j][key]
            for key in contacts_dict_list[i].keys():
                contacts_dict_list[j][key] = ""
list_index_del = []
for i in range(len(contacts_dict_list)):
    if contacts_dict_list[i]["lastname"] == "":
        list_index_del.append(i)
count = 0
for i in list_index_del:
    del contacts_dict_list[i-count]
    count +=1

# phone number correction
pattern = r"(\+7|8)[\s-]?\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s?\(?(доб.\s\d+)\)?)?"
for contact in contacts_dict_list:
    contact['phone'] = re.sub(pattern, r"+7(\2)\3-\4-\5 \7", contact['phone'])

result = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]
for contact in contacts_dict_list:
    result.append(list(contact.values()))

# код для записи файла в формате CSV
with open("phonebook_raw.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result)
