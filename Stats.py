import os
import shutil
from Board import *


if __name__ == '__main__':
    for i in range(4):
        my_board = Board(initial_lights_mode=i, initial_simulation_speed=8, end_after=1000, display_needed=False)
        my_board.start()
        new_name = f"stats{i}.csv"
        os.rename("stats.csv", new_name)
        shutil.move(new_name, "./res")
