import threading
import time

class PomodoroTimer:
    def __init__(self):
        # Default durations
        self.work_duration = 25 * 60    # 25 min
        self.short_break = 5 * 60       # 5 min
        self.long_break = 15 * 60       # 15 min

        # Session tracking
        self.work_sessions_completed = 0
        self.sessions_before_long_break = 4
        self.total_work_sessions = None  # User-defined

        # Timer state
        self.duration = self.work_duration
        self.time_left = self.duration
        self.timer_thread = None
        self.running = False
        self.lock = threading.Lock()
        self.mode = 'work'  # 'work', 'short_break', 'long_break', 'done'

    def _run_timer(self):
        while True:
            with self.lock:
                if not self.running or self.mode == 'done':
                    break

                # Count down if time left
                if self.time_left > 0:
                    self.time_left -= 1
                else:
                    # Transition to next mode
                    if self.mode == 'work':
                        self.work_sessions_completed += 1
                        if self.total_work_sessions and self.work_sessions_completed >= self.total_work_sessions:
                            self.mode = 'done'
                            self.running = False
                            break
                        # Choose break type
                        if self.work_sessions_completed % self.sessions_before_long_break == 0:
                            self.mode = 'long_break'
                            self.duration = self.long_break
                        else:
                            self.mode = 'short_break'
                            self.duration = self.short_break
                        self.time_left = self.duration
                    elif self.mode in ['short_break', 'long_break']:
                        self.mode = 'work'
                        self.duration = self.work_duration
                        self.time_left = self.duration

            time.sleep(1)

    def start(self):
        with self.lock:
            if not self.running and self.mode != 'done':
                self.running = True
                if self.timer_thread is None or not self.timer_thread.is_alive():
                    self.timer_thread = threading.Thread(target=self._run_timer, daemon=True)
                    self.timer_thread.start()

    def stop(self):
        with self.lock:
            self.running = False

    def reset(self):
        with self.lock:
            self.mode = 'work'
            self.duration = self.work_duration
            self.time_left = self.duration
            self.running = False
            self.work_sessions_completed = 0
            self.total_work_sessions = None

    def set_total_work_sessions(self, n):
        with self.lock:
            if n > 0:
                self.total_work_sessions = n

    def get_time_left(self):
        with self.lock:
            return self.time_left

    def is_running(self):
        with self.lock:
            return self.running

    def get_mode(self):
        with self.lock:
            return self.mode
