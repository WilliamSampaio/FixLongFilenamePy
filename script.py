import hashlib
import random
import os
import time


def append_new_line(file_name, text_to_append):
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text_to_append)
        return True


def apply(path):
    count = 0
    obj = os.scandir(path)
    for entry in obj:
        if entry.is_dir():
            count = count + apply(entry.path)
        else:
            if len(entry.name) >= 100:
                new_name = hashlib.md5((entry.name + str(random.randint(100, 999))).encode("utf-8")).hexdigest() + ".novonome"
                if(append_new_line(
                    "list-files.txt",
                    os.path.dirname(entry.path).replace(os.getcwd(), '').replace("\\", "/")
                    + "/"
                    + new_name
                    + "::"
                    + entry.name,
                )):
                    count = count + 1
                os.rename(
                    entry.path,
                    os.path.dirname(entry.path).replace(
                        "\\", "/") + "/" + new_name,
                )
    obj.close()
    return count


def revert():
    count = 0
    lines = open("list-files.txt", "r").readlines()
    for line in lines:
        data = line.split("::")
        temp_name = os.getcwd() + "/" + data[0]
        original_name = os.path.dirname(os.getcwd() + "/" + data[0]) + "/" + data[1]
        os.rename(temp_name, original_name.replace("\n", ""))
        count = count + 1
    os.rename("list-files.txt", "OK_list-files.txt")
    return count


os.system('cls')

root_path = os.getcwd()
print("Diretório: '% s'\n" % root_path)

print("1. Aplicar")
print("2. Reverter\n")

option = input()

if option == "1":
    print("Arquivos encontrados: " + str(apply(root_path)))
else:
    if option == "2":
        print("Arquivos encontrados: " + str(revert()))
    else:
        print("Opção inválida!")

input()
