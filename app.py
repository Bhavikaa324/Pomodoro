from flask import Flask, render_template, jsonify, request
from timer import PomodoroTimer

app = Flask(__name__)
timer = PomodoroTimer()
user_started = False  # Track if user manually started work

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start')
def start_timer():
    global user_started
    timer.start()
    user_started = True
    return jsonify(status='started')  # Only for user-triggered start

@app.route('/stop')
def stop_timer():
    global user_started
    timer.stop()
    user_started = False
    return jsonify(status='stopped')

@app.route('/reset')
def reset_timer():
    global user_started
    timer.reset()
    user_started = False
    h, m, s = 0, 25, 0
    return jsonify(status='reset', duration=f'{h:02d}:{m:02d}:{s:02d}')

@app.route('/set_total_sessions')
def set_total_sessions():
    total_sessions = request.args.get('total', default=0, type=int)
    if total_sessions < 1:
        return jsonify(status='Error: Total sessions must be at least 1'), 400
    timer.set_total_work_sessions(total_sessions)
    return jsonify(status=f'Total work sessions set to {total_sessions}')

@app.route('/time')
def get_time():
    mode = timer.get_mode()
    # Only report "started" status for work if user actually started
    status = 'running' if timer.is_running() else 'stopped'
    return jsonify({
        'time_left': timer.get_time_left(),
        'total_duration': timer.duration,
        'is_running': timer.is_running(),
        'mode': mode,
        'work_sessions_completed': timer.work_sessions_completed,
        'user_started': user_started,
        'status': status
    })

if __name__ == '__main__':
    app.run(debug=True)
