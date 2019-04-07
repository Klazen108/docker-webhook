from flask import Flask
from flask import request
from flask import jsonify
import json
import subprocess

app = Flask(__name__)
config = None

@app.route("/", methods=['POST'])
def hook_listen():
    if request.method != 'POST':
        return jsonify(success=False, error="Unsupported Method: "+request.method), 400

    token = request.args.get('token')
    if token != config['token']:
        return jsonify(success=False, error="Invalid token"), 400

    hook = request.args.get('hook')
    if not hook:
        return jsonify(success=False, error="Invalid request: missing hook"), 400

    hook_value = config['hooks'].get(hook)
    if not hook_value:
        return jsonify(success=False, error="Hook not found"), 404

    s = request.data
    data = json.loads(s)
    print("Push date: {data}".format(data=data['push_data']['pushed_at']))
    print("Push images: {data}".format(data=data['push_data']['images']))
    print("Push tag: {data}".format(data=data['push_data']['tag']))
    print("Repo url: {data}".format(data=data['repository']['repo_url']))
    print("Repo visibility: {data}".format(data=data['repository']['is_private']))
    print("Repo name: {data}".format(data=data['repository']['repo_name']))
    print("Repo status: {data}".format(data=data['repository']['status']))
    try:
        subprocess.call(['execute_remote.sh',
            config['host_user'], 
            "/root/dockerpuller/scripts/{}.sh".format(hook)
        ])
        return jsonify(success=True), 200
    except OSError as e:
        return jsonify(success=False, error=str(e)), 400

def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)

if __name__ == "__main__":
    config = load_config()
    if 'host_user' not in config:
        raise ValueError("Missing host_user in config!")
    print("")
    print("Registered hooks:")
    for key in config['hooks']:
        print (key,':',config['hooks'][key])
    #print("Found scripts:")
    print("token: {}".format(config['token']))
    app.run(host=config.get('host', 'localhost'), port=config.get('port', 8000))
