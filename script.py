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


def apply(path):
    obj = os.scandir(path)
    for entry in obj:
        if entry.is_dir():
            apply(entry.path)
        else:
            if len(entry.name) >= 100:
                new_name = str(time.time()) + str(random.randint(100, 999))
                append_new_line(
                    "list-files.txt",
                    os.path.dirname(entry.path).replace("\\", "/")
                    + "/"
                    + new_name
                    + "::"
                    + entry.name,
                )
                os.rename(
                    entry.path,
                    os.path.dirname(entry.path).replace("\\", "/") + "/" + new_name,
                )
    obj.close()
    return


def revert():
    lines = open("list-files.txt", "r").readlines()
    for line in lines:
        data = line.split("::")
        temp_name = data[0]
        original_name = os.path.dirname(data[0]) + "/" + data[1]
        os.rename(temp_name, original_name.replace("\n", ""))
    os.remove("list-files.txt")
    return


root_path = os.getcwd()
print("Diretório: '% s'\n" % root_path)

print("1. Aplicar")
print("2. Reverter\n")

option = input()

if option == "1":
    apply(root_path)
else:
    if option == "2":
        revert()
    else:
        print("Opção inválida!")

input()
