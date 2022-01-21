import sys
import clipboard
import json
import os


def save_data(filepath, data):
    with open(filepath, "w")as f:
        json.dump(data, f)


def load_data(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except:
        return {}


def clear_data(filepath):
    os. remove(filepath)


if len(sys.argv) == 2:
    command = sys.argv[1]
    data = load_data("clipboard.json")

    if command == "save":
        key = input("Enter a key: ")
        data[key] = clipboard.paste()
        save_data("clipboard.json", data)
    elif command == "load":
        key = input("Enter a key: ")
        if key in data:
            clipboard.copy(data[key])
            print("Copied to the clipboard")
        else:
            print("Invalid key")
    elif command == "clear":
        clear_data("clipboard.json")
        print("Cleared data")
    elif command == "list":
        print(data)
    else:
        print("unknown command\nusable commands are =>\n save\n load\n clear\n list")
else:
    print("Give one usable command\nusable commands are =>\n save\n load\n clear\n list")
