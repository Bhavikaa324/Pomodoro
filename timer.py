import threading
import time

class PomodoroTimer:
    def __init__(self):
        self.default_duration = 25 * 60  # Default 25 minutes in seconds
        self.duration = self.default_duration  # Current duration (can be customized)
        self.time_left = self.duration
        self.timer_thread = None
        self.running = False
        self.lock = threading.Lock()
        self.reset_mode = False

    def _run_timer(self):
        while True:
            with self.lock:
                if not self.running or self.time_left <= 0:
                    break
                self.time_left -= 1
            time.sleep(1)

        with self.lock:
            if self.time_left <= 0:
                self.running = False

    def start(self):
        with self.lock:
            if not self.running:
                self.running = True
                self.reset_mode = False
                if self.timer_thread is None or not self.timer_thread.is_alive():
                    self.timer_thread = threading.Thread(target=self._run_timer)
                    self.timer_thread.start()

    def stop(self):
        with self.lock:
            if not self.reset_mode:
                self.running = False

    def reset(self):
        with self.lock:
            self.duration = self.default_duration  # Always reset to default 25 minutes
            self.time_left = self.duration
            self.running = False
            self.reset_mode = True

    def set_custom_duration(self, seconds=None):
        with self.lock:
            if seconds and seconds > 0:
                self.duration = seconds
            else:
                self.duration = self.default_duration
            self.time_left = self.duration
            self.running = False
            self.reset_mode = False

    def get_time_left(self):
        with self.lock:
            return self.time_left

    def is_running(self):
        with self.lock:
            return self.running
