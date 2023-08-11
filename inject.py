import json
from mitmproxy import ctx
from urllib.parse import urlparse, parse_qs, urlunparse
import logging

payloads = []
response_data_list = []

with open('inject_config.json', 'r') as config_file:
    config = json.load(config_file)

# Load all headers from the file and append to the list
with open(config["payload_file"], 'r') as f:
    lines = f.readlines()  # Read lines instead of the whole content
    payloads.extend(lines)  # Use extend to add lines to the list

def request(flow):
    # Check if the request's hostname is example.com
    if flow.request.host.endswith(config["hostname"]):
        # Avoid an infinite loop by not replaying already replayed requests
        if flow.is_replay:
            return

        parsed_url = urlparse(flow.request.url)
        base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))

        logging.info(base_url)
        query_params = parse_qs(parsed_url.query)

        if "view" in ctx.master.addons:
            ctx.master.commands.call("view.flows.duplicate", [flow])

        for payload in payloads:
            modified_query_params = query_params.copy()  # Create a copy to modify
            for param in modified_query_params:
                modified_query_params[param] = [payload]

            modified_query_string = "&".join([f"{param}={value[0]}" for param, value in modified_query_params.items()])
            final_url = base_url + "?" + modified_query_string

            modified_flow = flow.copy()
            modified_flow.request.headers['user-agent'] = config['user_agent']
            modified_flow.request.url = final_url
            logging.info(modified_flow)
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
    with open("inject_response.json", "w") as f:
        json.dump(response_data_list, f, indent=4)

def done():
    save_to_file()

addons = [
    # Register the above functions as event handlers
    request, response, done
]
