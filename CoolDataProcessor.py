import pandas as pd
from CoolDataProcessor_helper import load_data_helper

'''ALL PUBLIC METHODS RETURN A LIST'''

class CoolDataProcessor():
    TABLENAMES = ["course table", "videos table","students table", "viewing records table"]
    def __init__(self, path, table_names=[]):
        self._path = path
        self._course_table = None
        self._videos_table = None
        self._studs_table = None
        self._view_records_table = None
        if (table_names!=[]):
            CoolDataProcessor.TABLENAMES = table_names

    def load_data(self):
        tables = load_data_helper(self._path, CoolDataProcessor.TABLENAMES)
        for table_name in tables.keys():
            if ("course" in table_name.lower()):
                self._course_table = tables[table_name]
            elif ("videos" in table_name.lower()):
                self._videos_table = tables[table_name]
            elif ("students" in table_name.lower()):
                self._studs_table = tables[table_name]
            elif ("records" in table_name.lower()):
                self._view_records_table = tables[table_name]
                
    def get_course(self):
        return self._course_table
    def get_videos(self):
        return self._view_records_table
    def get_students(self):
        return self._studs_table
    def get_records(self):
        return self._view_records_table

    #學生實際總觀看時間（經播放速度矯正）
    def sum_watch_time(self, student_id="", video_id="", start_time="", end_time=""):
        pass
        # return sum_watch_time
    
    def completion_rate(self, student_id="", video_id="", start_time="", end_time=""):
        pass
        # return completion_r

    #學生後退次數/快轉次數/總暫停次數
    #（ pause_thresh 是暫停的自定義閥值，如間隔小於5秒才算暫停）
    def action_freq(self, student_id="", video_id="", start_time="", end_time="", action="pause", pause_thresh=5):
        pass
        # return action_freq

    #學生後退秒數/快轉秒數
    #（ pause_thresh 是後退/快轉的自定義閥值，如間隔>=5秒才算後退/快轉
    def action_time(self, student_id="", video_id="", start_time="", end_time="", action="forward", pause_thresh=5):
        pass
        # return action_time

    #學生觀看時段累積秒數/該時段累積秒數佔比
    #（時段自定義，如23~3=period0; 3~5=period1, etc..）
    def period_sum_watch_time(self, student_id="", video_id="", start_time="", end_time="", period_def={}):
        pass
        # return period_sum_watch_time
    
    def avg_play_back_rate(self, student_id="", video_id="", start_time="", end_time=""):
        pass
        # return avg_play_back_rate


# 學生平均播放速度
# input: 時間區間, 學生ID, 影片ID (optional)
# output: 該區間內/整學期 該學生 某/所有影片 的 平均播放速度






