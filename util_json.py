import json

def save_json_to_file(dict, file_path):
    print(f"Saving JSON to '{file_path}'")
    json_object = json.dumps(dict, indent=2)

    with open(file_path, "w") as outfile:
        outfile.write(json_object)
