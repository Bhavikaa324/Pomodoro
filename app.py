from flask import Flask, render_template, jsonify, request
from timer import PomodoroTimer

app = Flask(__name__)
timer = PomodoroTimer()
timer.set_custom_duration(25 * 60)  # Default 25 minutes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start')
def start_timer():
    timer.start()
    return jsonify(status='started')

@app.route('/stop')
def stop_timer():
    timer.stop()
    return jsonify(status='stopped')

@app.route('/reset')
def reset_timer():
    timer.reset()
    # Return default 25 minutes in HH:MM:SS format
    h = 0
    m = 25
    s = 0
    return jsonify(status='reset', duration=f'{h:02d}:{m:02d}:{s:02d}')

@app.route('/set_duration')
def set_duration():
    # Accept hours, minutes, seconds separately
    hours = request.args.get('hours', default=0, type=int)
    minutes = request.args.get('minutes', default=0, type=int)
    seconds = request.args.get('seconds', default=0, type=int)

    # Convert to total seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds
    if total_seconds < 1:
        return jsonify(status='Error: Duration must be at least 1 second'), 400

    # Set custom duration
    timer.set_custom_duration(total_seconds)

    # Normalize back to H:M:S
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60

    return jsonify(status=f'Duration set to {h:02d}:{m:02d}:{s:02d}')

@app.route('/time')
def get_time():
    return jsonify({
        'time_left': timer.get_time_left(),
        'total_duration': timer.duration,
        'is_running': timer.is_running()
    })

if __name__ == '__main__':
    app.run(debug=True)
