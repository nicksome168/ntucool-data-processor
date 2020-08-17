import argparse
from CoolDataLoader import CoolDataLoader
from CoolDataProcessor import *

# Training settings
parser = argparse.ArgumentParser()
parser.add_argument('--f', type=str)
args = parser.parse_args()

Loader = CoolDataLoader(args.f)
# print(Loader.get_course())
# print(Loader.get_videos())
# print(Loader.get_students())
# print(Loader.get_records())

videos_df = Loader.get_videos()
cool_df = Loader.filter_select(["b07705016", "b07705051"], [], "", "")
# print(cool_df.head())
# print(videos_df.head())

# func 1
watch_time_df = watch_time(cool_df)
# print(watch_time_df)


# func2

complete_table = completion_rate(cool_df, videos_df)
# print(complete_table)


# func 3
action_freq_table = action_freq(cool_df, action="forward")
# print(action_freq_table)


# func 4
action_dura_table = action_duration(cool_df, action="forward")
# print(action_dura_table)

# func 5
pause_freq_table = pause_freq(cool_df)
# print(pause_freq_table)


period_watch_df = watch_time(cool_df, [0000, 600])
print(period_watch_df)
