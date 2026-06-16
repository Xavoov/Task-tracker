import argparse
import json
import datetime as dt
import os

def open_file():
    with open("data.json", "r") as file_reader:
        data = json.load(file_reader)
        return data

def add(task):
    with open("data.json", "r") as f:
        try:
            data = json.load(f)
            ids = []

            for keys, values in data.items():
                ids.append(values["id"])

            max_id = max(ids) 

        except json.decoder.JSONDecodeError:
            data = {}
            max_id = 0

        tab = {
            task: {
                "id": max_id + 1,
                "description": task,
                "status": "todo",
                "createdAt": dt.datetime.now().strftime("%d/%m/%Y"),
                "updatedAt": dt.datetime.now().strftime("%d/%m/%Y")
            }
        }  

        data.update(tab)

    with open("data.json", "w") as f_write:
        json.dump(data, f_write, indent=2)

    print(f"Task added successfully (ID: {max_id + 1})")

def update(id, name):
    with open("data.json", "r") as file_read:
        data = json.load(file_read)
    
    with open("data.json", "w") as file_write:
        for keys, values in data.items():
            if values['id'] == id:
                key = data[keys]
                old_key = keys
                values['description'] = name
                values['updatedAt'] = dt.datetime.now().strftime("%d/%m/%Y")

        data[name] = key
        del data[old_key]

        json.dump(data, file_write, indent=2)

def delete(id):
    data = open_file()
    with open('data.json', "w") as file_writer:
        for keys, values in data.items():
            if values['id'] == id:
                old_key = keys

        del data[old_key]
        
        json.dump(data, file_writer, indent=2)

def progress(id):
    data = open_file()
    with open('data.json', 'w') as file_write:
        for key, value in data.items():
            if value['id'] == id:
                value['status'] = 'in-progress'

        json.dump(data, file_write, indent=2)

def done(id):
    data = open_file()
    with open('data.json', 'w') as file_write:
        for key, value in data.items():
            if value['id'] == id:
                value['status'] = 'done'
        
        json.dump(data, file_write, indent=2)

def list():
    data = open_file()
    for index, (key, values) in enumerate(data.items(), 1):
        print(f"{index}. {key}\n")
        for x, y in values.items():
            print(f"{x}: {y}")
        print("\n")

def list_done():
    data = open_file()
    counter = 1
    for key, values in data.items():
        if values['status'] == 'done':
            print(f"{counter}. {key}\n")
            for x, y in values.items():
                print(f"{x}: {y}")
            print("\n")
            counter += 1

def list_todo():
    data = open_file()
    counter = 1
    for key, values in data.items():
        if values['status'] == 'todo':
            print(f"{counter}. {key}\n")
            for x, y in values.items():
                print(f"{x}: {y}")
            print("\n")
            counter += 1

def list_progress():
    data = open_file()
    counter = 1
    for key, values in data.items():
        if values['status'] == 'in-progress':
            print(f"{counter}. {key}\n")
            for x, y in values.items():
                print(f"{x}: {y}")
            print("\n")
            counter += 1

def main():
    if "data.json" not in os.listdir(os.getcwd()):
        with open("data.json", "w"):
            pass

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="operation")
    parser_add = subparser.add_parser("add")
    parser_add.add_argument("name", type=str)
    parser_update = subparser.add_parser("update")
    parser_update.add_argument("id", type=int)
    parser_update.add_argument("name_u", type=str)
    parser_delete = subparser.add_parser("delete")
    parser_delete.add_argument("id_del", type=int)
    parser_progress = subparser.add_parser("mark-in-progress")
    parser_progress.add_argument("id_prog", type=int)
    parser_done = subparser.add_parser("mark-done")
    parser_done.add_argument("id_done", type=int)
    parser_list = subparser.add_parser("list")
    parser_list.add_argument("status", nargs='?')

    args = parser.parse_args()

    if args.operation == "add":
        add(args.name)
    if args.operation == "update":
        update(args.id, args.name_u)
    if args.operation == "delete":
        delete(args.id_del)
    if args.operation == "mark-in-progress":
        progress(args.id_prog) 
    if args.operation == "mark-done":
        done(args.id_done) 
    if args.operation == "list":
        if args.status == "done":
            list_done()
        elif args.status == 'todo':
            list_todo()
        elif args.status == 'in-progress':
            list_progress()
        else:
            list()

main()

