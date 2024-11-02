from flask import Flask, render_template, request, jsonify
from agent import agent
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def livechat_get():#
    return render_template('agent.html')

@app.route('/agent', methods=['POST'])
def invoke_agent():
    data = request.get_json()
    text = data.get('message')
    config = data.get('config', 'default_session')  # Default value if config is not provided
    ip = request.remote_addr  # Get the IP address of the client
    response = agent(text, config=config, ip=ip)   
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=('cert.pem', 'key.pem'))
    app.run(host='0.0.0.0', port=5050, debug=True)
