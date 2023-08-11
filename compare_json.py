import sys
import json

def compare_fields(base_dict, other_dict, fields):
    for field in fields:
        base_value = base_dict
        other_value = other_dict
        nested_fields = field.split('.')
        for nested_field in nested_fields:
            base_value = base_value.get(nested_field)
            other_value = other_value.get(nested_field)
            if base_value is None or other_value is None:
                break
        if base_value != other_value:
            return True
    return False

if len(sys.argv) < 2:
    print("Usage: python script.py input.json")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file, 'r') as f:
    json_array = json.load(f)

if len(json_array) < 2:
    print("The JSON array must contain at least two elements for comparison.")
    sys.exit(1)

base_element = json_array[0]
fields_to_compare = ["status_code", "headers.Content-Length"]
differences_found = False

for i in range(1, len(json_array)):
    current_element = json_array[i]
    if compare_fields(base_element, current_element, fields_to_compare):
        print(f"Difference found in URL: {current_element['url']}")
        differences_found = True

if not differences_found:
    print("No differences found.")
