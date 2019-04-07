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

    if not hook in config['hooks']:
        return jsonify(success=False, error="Hook not available"), 404

    s = request.data
    data = json.loads(s)
    print("Running hook: {}".format(hook))
    try:
        subprocess.call(['/root/dockerpuller/execute_remote.sh',
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
    print("Webhook Token: {}".format(config['token']))
    print("Available hooks:")
    for key in config['hooks']:
        print (key)
    print("Now standing by waiting to make your CI dreams come true!")
    app.run(host=config.get('host', 'localhost'), port=config.get('port', 8000))
