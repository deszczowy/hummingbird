from PyQt5.QtCore import QTimer

class Timer:

    main_timer_interval = 1000
    scheduler_interval = 7000

    def __init__(self, parent):
        self.parent = parent
        self.tic = 0
        self.timer = QTimer(parent)
        self.schedule = QTimer(parent)
        self.prepare()

    def prepare(self):
        self.timer.timeout.connect(self.timer_tic)
        self.schedule.timeout.connect(self.schedule_tic)
        self.timer.start(self.main_timer_interval)
        self.schedule.start(self.scheduler_interval)

    def timer_tic(self):
        if self.tic > 0:
            self.tic -= 1
        if self.tic == 1:
            self.parent.clear_status()

    def schedule_tic(self):
        self.parent.action_save()
