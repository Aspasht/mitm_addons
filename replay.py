from mitmproxy import ctx

def request(flow):
    # Avoid an infinite loop by not replaying already replayed requests
    if flow.is_replay:
        return
    if "example.com" in flow.request.host:
        return
    original_path = flow.request.path

    # Only interactive tools have a view. If we have one, add a duplicate entry
    # for our flow.
    if "view" in ctx.master.addons:
        ctx.master.commands.call("view.flows.duplicate", [flow])

    for i in range(1, 11):  # Loop from 1 to 10
        modified_path = original_path + "/" + str(i)
        modified_flow = flow.copy()
        modified_flow.request.path = modified_path
        modified_flow.request.headers['user-agent']="Firefox"
        ctx.master.commands.call("replay.client", [modified_flow])
