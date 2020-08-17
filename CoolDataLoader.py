import pandas as pd
from config import *
from CoolDataLoader_helper import load_data_helper, filter_id_helper, slice_time_helper, set_date_index, to_datetime


'''ALL PUBLIC METHODS RETURN A LIST'''


class CoolDataLoader():
    TABLENAMES = ["course table", "videos table",
                  "students table", "viewing records table"]

    def __init__(self, path, table_names=[]):
        self._path = path
        self._course_table = None
        self._videos_table = None
        self._studs_table = None
        self._view_records_table = None
        if (table_names != []):
            CoolDataLoader.TABLENAMES = table_names
        self._load_data()

    def _load_data(self):
        tables = load_data_helper(self._path, CoolDataLoader.TABLENAMES)
        for table_name in tables.keys():
            if ("course" in table_name.lower()):
                self._course_table = tables[table_name]
            elif ("videos" in table_name.lower()):
                self._videos_table = tables[table_name]
            elif ("students" in table_name.lower()):
                self._studs_table = tables[table_name]
            elif ("records" in table_name.lower()):
                self._view_records_table = tables[table_name]
        # preprocess
        self._studs_table[COLNAME_STUD_NTU_IDS] = self._studs_table["email"].apply(
            lambda x: x.split("@")[0])
        self._view_records_table["end"] = self._view_records_table["end"].astype(
            int)
        self._view_records_table["start"] = self._view_records_table["start"].astype(
            int)
        self._view_records_table["playback_rate"] = self._view_records_table["playback_rate"].astype(
            float)
        self._view_records_table
        self._view_records_table['created_at'] = list(
            map(to_datetime, self._view_records_table['created_at']))

    def get_course(self):
        return self._course_table

    def get_videos(self):
        return self._videos_table

    def get_students(self):
        return self._studs_table

    def get_records(self):
        return self._view_records_table

    def filter_select(self, student_ntu_ids, video_ids, slice_start="", slice_end=""):
        student_ntu_ids_lower = [id.lower() for id in student_ntu_ids]
        # lookup stud ids
        student_ids = self._studs_table[self._studs_table[COLNAME_STUD_NTU_IDS].isin(
            student_ntu_ids_lower)]["id"].tolist()

        records = self._view_records_table
        fltr_records = filter_id_helper(
            records, "student_id", student_ids)
        fltr_records = filter_id_helper(
            fltr_records, "video_id", video_ids)
        fltr_records = slice_time_helper(
            fltr_records, "created_at", slice_start, slice_end)
        return fltr_records
