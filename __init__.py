import os
from cudatext import *
import cudatext_cmd as cmds

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'plugins.ini')
config_section = 'splitters'
config_b = 'b'
config_s = 's'

b = SPLITTER_BOTTOM
s = SPLITTER_SIDE

class Command:
    def __init__(self):
        self.b_init = self.get_pos(b) if self.get_pos(b) > 0 else 500
        self.s_init = self.get_pos(s) if self.get_pos(s) > 150 else 250

        self.b_max = False
        self.s_max = False

        self.h = 360

    def on_start(self, ed_self):
        self.load_ops()

    def get_windows_sizes(self):
        coords = app_proc(PROC_COORD_WINDOW_GET, '')
        return coords[2] - coords[0], coords[3] - coords[1]

    def load_ops(self):
        self.b = ini_read(fn_config, config_section, config_b, str(self.b_init))
        self.s = ini_read(fn_config, config_section, config_s, str(self.s_init))
        self.save_ops()

    def save_ops(self):
        ini_write(fn_config, config_section, config_b, str(self.b))
        ini_write(fn_config, config_section, config_s, str(self.s))

    def save_curr_pos(self):
        ini_write(fn_config, config_section, config_b, str(int(self.get_pos(b) - self.h)))
        ini_write(fn_config, config_section, config_s, str(self.get_pos(s)))

    def open_config(self):
        if os.path.isfile(fn_config):
            file_open(fn_config)

    def get_pos(self, splitter):
        return app_proc(PROC_SPLITTER_GET, splitter)[2]

    def set_pos(self, splitter, p):
        return app_proc(PROC_SPLITTER_SET, [splitter, p])

    def toogle(self, splitter, p):
        self.set_pos(splitter, p)

    def toggle_b(self):
        if not self.b_max:
            p = int(self.get_windows_sizes()[1] * 0.2)
            self.b_max = True
        else:
            p = int(self.b) + self.h
            self.b_max = False
        self.toogle(b, p)

    def toggle_s(self):
        if not self.s_max:
            p = int(self.get_windows_sizes()[0] * 0.5)
            self.s_max = True
        else:
            p = int(self.s)
            self.s_max = False
        self.toogle(s, p)
