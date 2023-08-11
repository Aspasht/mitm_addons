import json
from mitmproxy import ctx
from urllib.parse import urlparse

# Load configuration from the JSON file
with open('waf_config.json', 'r') as config_file:
    config = json.load(config_file)

all_headers = []
response_data_list = []

# Load all headers from the file and append to the list
with open('waf_headers.txt', 'r') as f:
    lines = f.readlines()  
    all_headers.extend(lines)  

def request(flow):
    # Get the hostname from the request URL using urlparse
    parsed_url = urlparse(flow.request.url)
    hostname = parsed_url.hostname
    
    # Check if the hostname matches the one from the configuration
    if hostname and hostname == config["hostname"]:
        # Avoid an infinite loop by not replaying already replayed requests
        if flow.is_replay:
            return

        if "view" in ctx.master.addons:
            ctx.master.commands.call("view.flows.duplicate", [flow])

        for header in all_headers:
            header = header.strip().lower()
            modified_flow = flow.copy()
            modified_flow.request.headers['user-agent'] = config["user_agent"]
            modified_flow.request.headers[header] = "127.0.0.1"
            ctx.master.commands.call("replay.client", [modified_flow])

def response(flow):
    # Get the hostname from the request URL using urlparse
    parsed_url = urlparse(flow.request.url)
    hostname = parsed_url.hostname
    
    # Check if the hostname matches the one from the configuration
    if hostname and hostname == config["hostname"]:
        # Store the response status code, URL, headers, and modified request headers in a dictionary
        response_data = {
            "url": flow.request.url,
            "status_code": flow.response.status_code,
            "request_headers": dict(flow.request.headers),
            "response_headers": dict(flow.response.headers)
        }
        response_data_list.append(response_data)

    # Save the captured data after each response
    save_to_file()

def save_to_file():
    with open("waf_response.json", "w") as f:
        json.dump(response_data_list, f, indent=4)

addons = [
    # Register the above functions as event handlers
    request, response
]
