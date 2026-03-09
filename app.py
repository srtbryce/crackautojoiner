from flask import Flask, request, jsonify
import time

app = Flask(__name__)
job_ids = {}  # In-memory — resets on reload/restart, ok for your use

@app.route('/update', methods=['POST'])
def update_job():
    data = request.json
    user = data.get('user')
    if not user:
        return jsonify({'error': 'Missing user'}), 400
    job_ids[user] = {
        'jobId': data.get('jobId'),
        'placeId': data.get('placeId'),
        'timestamp': data.get('timestamp', time.time())
    }
    return jsonify({'status': 'updated'})

@app.route('/getjob', methods=['GET'])
def get_job():
    user = request.args.get('user')
    if user in job_ids:
        info = job_ids[user]
        if time.time() - info['timestamp'] > 300:  # 5 min expire
            del job_ids[user]
            return jsonify({'error': 'Expired'}), 404
        return jsonify(info)
    return jsonify({'error': 'User not found'}), 404
