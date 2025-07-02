# читаем адресную книгу в формате CSV в список contacts_list
import csv, re, os
from Decorator_params import logger


path = 'regex.log'
if os.path.exists(path):
    os.remove(path)

@logger(path)
def split_parts_name(contacts): #Выделяем Фамилию, Имя, Отчество
    fio = " ".join(contacts[:3]).split()
    if len(fio) >= 3:
        return [fio[0], fio[1], fio[2]]
    elif len(fio) == 2:
        return [fio[0], fio[1], '']
    else:
        return [fio[0], '', '']

@logger(path)
def format_phone_number(phone): #Приводим телефонный номер к нужному формату
    pattern = r"(\+7|8)\s?[(-]?(\d{3})[-)]?\s?(\d{3})\-?(\d{2})\-?(\d{2})(.*)"
    match = re.match(pattern, phone)
    country_code, area_code, first_part, second_part, third_part, extension = match.groups()
    normalized_number = f"+7({area_code}){first_part}-{second_part}-{third_part}"
    ext_match = re.search(r"(\d{4})", extension)
    if ext_match:
        normalized_number += f" доб.{ext_match.group(1)}"
    return [normalized_number.strip()]


@logger(path)
def join_duplicate_contact(contact_list):
    unic_contact_list = []
    for i in contact_list:
        for j in contact_list:
            if i[0] == j [0] and i[1] == j[1] and j is not i:
                last = i[0]
                first = i[1]
                sur = j[2] if i[2] == "" else i[2]
                org = j[3] if i[3] == "" else i[3]
                pos = j[4] if i[4] == "" else i[4]
                phone = j[5] if i[5] == "" else i[5]
                mail = j[6] if i[6] == "" else i[6]
                rec = [last, first, sur, org, pos, phone,mail]
                contact_list.remove(j)
                contact_list.remove(i)
                if rec not in unic_contact_list:
                    unic_contact_list.append(rec)
    unic_contact_list.extend(contact_list)
    return unic_contact_list

if __name__ == "__main__":
    with open("phonebook_raw.csv", encoding="utf-8") as f: # Читаем файл из csv
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    titul = [contacts_list[0]] #Сохраняем заголовки
    contacts_list = contacts_list[1:]

    #Формируем список c правильно выделенными частями ФИО
    contacts_list = [split_parts_name(x)+x[3:] for x in contacts_list]

    #Приводим все телефоны к заданному стандарту записи
    contacts_list = [x[:5] + format_phone_number(x[5]) + x[6:] if x[5] else x for x in contacts_list]

    #Объединяем дублирующиеся записи при совпадении фамилии и имени
    contacts_list = join_duplicate_contact(contacts_list)

    #Добавляем заголовки полей
    contacts_list = titul + contacts_list

    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)