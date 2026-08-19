from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "DevSecOps Pipeline Built Successfully!"

@app.route('/health')
def health():
    # Returns 200 OK for the pipeline health check
    return jsonify(status="healthy"), 200

if __name__ == '__main__':
    # Running on 0.0.0.0 to make it accessible inside the container
    app.run(host='0.0.0.0', port=5000)
