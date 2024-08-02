import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.properties import StringProperty

Builder.load_file('timer.kv')  # Load the kv file

class TimerLabel(Label):
    text = StringProperty("Timer App")
    font_size = '40sp'
    color = (1, 1, 1, 1)
    bold = True

class TimerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remaining_time = 0
        self.timer_event = None
        self.sound = SoundLoader.load('ringtone.mp3')  # Make sure to have a ringtone file

    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Set a dark background color for the window
        return self.root

    def start_timer(self):
        try:
            input_str = self.root.ids.time_input.text
            if len(input_str) < 4:
                raise ValueError('Please enter a valid time.')
            hours = int(input_str[:2])
            minutes = int(input_str[2:])
        except ValueError:
            self.root.ids.timer_label.text = 'Please enter a valid time in HHMM format (e.g., 0330)'
            return

        interval_seconds = (hours * 3600) + (minutes * 60)
        self.remaining_time = interval_seconds
        self.root.ids.timer_label.text = 'Timer Started'
        self.update_remaining_time()

        if self.timer_event:
            self.timer_event.cancel()

        self.timer_event = Clock.schedule_interval(self.update, 1)

    def stop_timer(self):
        self.root.ids.timer_label.text = 'Timer Stopped'
        if self.timer_event:
            self.timer_event.cancel()
        self.remaining_time = 0
        self.update_remaining_time()

    def update(self, dt):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_remaining_time()
        else:
            self.root.ids.timer_label.text = 'Time up!'
            if self.timer_event:
                self.timer_event.cancel()
            if self.sound:
                self.sound.play()

    def update_remaining_time(self):
        hours, remainder = divmod(self.remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.root.ids.remaining_label.text = f'Time remaining: {hours:02}:{minutes:02}:{seconds:02}'

if __name__ == '__main__':
    TimerApp().run()

