import json
from mitmproxy import ctx

all_headers = []
response_data_list = []

# Load all headers from the file and append to the list
with open('waf_headers.txt', 'r') as f:
    lines = f.readlines()  
    all_headers.extend(lines)  

def request(flow):
    # Avoid an infinite loop by not replaying already replayed requests
    if flow.is_replay:
        return

    if "view" in ctx.master.addons:
        ctx.master.commands.call("view.flows.duplicate", [flow])

    for header in all_headers:
        header = header.strip().lower()
        modified_flow = flow.copy()
        modified_flow.request.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        modified_flow.request.headers[header] = "127.0.0.1"
        ctx.master.commands.call("replay.client", [modified_flow])

def response(flow):
    # Store the response status code, URL, headers, and modified request headers in a dictionary
    response_data = {
        "url": flow.request.url,
        "status_code": flow.response.status_code,
        "request_headers": dict(flow.request.headers),  # Capture modified request headers
        "response_headers": dict(flow.response.headers)
    }
    response_data_list.append(response_data)

def save_to_file():
    with open("waf_response.json", "w") as f:
        json.dump(response_data_list, f, indent=4)

def done():
    save_to_file()

addons = [
    # Register the above functions as event handlers
    request, response, done
]
