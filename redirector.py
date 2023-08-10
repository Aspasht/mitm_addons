import json
from mitmproxy import ctx

payloads = []
response_data_list = []

# Load all headers from the file and append to the list
with open('openredirect_payloads.txt', 'r') as f:
    lines = f.readlines()  # Read lines instead of the whole content
    payloads.extend(lines)  # Use extend to add lines to the list

def request(flow):
    # Avoid an infinite loop by not replaying already replayed requests
    if flow.is_replay:
        return
    original_path = flow.request.path

    if "view" in ctx.master.addons:
        ctx.master.commands.call("view.flows.duplicate", [flow])

    for payload in payloads:
        modified_path = original_path + payload
        modified_flow = flow.copy()
        modified_flow.request.headers['user-agent']='Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        modified_flow.request.path = modified_path
        ctx.master.commands.call("replay.client", [modified_flow])

def response(flow):
    # Store the response status code, URL, and headers in a dictionary
    response_data = {
        "url": flow.request.url,
        "status_code": flow.response.status_code,
        "headers": dict(flow.response.headers)
    }
    response_data_list.append(response_data)

def save_to_file():
    with open("response_headers.json", "w") as f:
        json.dump(response_data_list, f, indent=4)


def done():
    save_to_file()

addons = [
    # Register the above functions as event handlers
    request, response, done
]