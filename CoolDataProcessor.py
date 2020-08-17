import pandas as pd

row_name = "student_id"
col_name = "video_id"


def watch_time(df, period=[0000, 2400]):
    valid_df = df[(df['end'] > df['start']) & (df['playback_rate'] != 0)]
    valid_df = valid_df[(valid_df["created_at"] > period[0]) &
                        (valid_df["created_at"] < period[1])]
    valid_df["elasped"] = (
        valid_df['end'] - valid_df['start'])/valid_df['playback_rate']
    table = pd.pivot_table(valid_df, values='elasped', index=[
                           row_name], columns=[col_name], aggfunc=sum)
    return table
# 學生實際總觀看時間（經播放速度矯正）


def completion_rate(df, videos_df):
    # durations of the lectures
    durations = [int(duration[duration.find(">")+1:duration.find("}")])
                 for duration in videos_df['meta']]
    videos_ids = videos_df["id"]
    table = watch_time(df)
    for duration, video_id in zip(durations, videos_ids):
        try:
            table[video_id] /= duration
        except:
            pass
    return table


def action_freq(df, action="backward"):
    if(action == "backward"):
        records = df[(df['start'] > df['end']) & (
            df['playback_rate'] == 0)]

    elif (action == "forward"):
        records = df[(df['end'] > df['start']) & (
            df['playback_rate'] == 0)]

    table = pd.pivot_table(records, values='created_at', index=[
        row_name], columns=[col_name], aggfunc=lambda x: len(x.unique()))
    return table
# 學生後退次數/快轉次數/總暫停次數
# end, start 先後判斷；playback_rate==0


def action_duration(df, action="forward"):
    if(action == "backward"):
        records = df[(df['start'] > df['end']) & (
            df['playback_rate'] == 0)]
        records["elasped"] = records["start"] - records["end"]
    elif (action == "forward"):
        records = df[(df['end'] > df['start']) & (
            df['playback_rate'] == 0)]
        records["elasped"] = records["end"] - records["start"]
    table = pd.pivot_table(records, values='elasped', index=[
        row_name], columns=[col_name], aggfunc=sum)
    return table


def pause_freq(df, pause_min=5, pause_max=300):
    # if the elasped time between next record and last record
        # is longer than 3 seconds, it counts as a pause
    counts = {}
    last_records = {}
    records = df
    for row_i in range(len(records)):
        time = records.iloc[row_i]["created_at"]
        stud_id = records.iloc[row_i]["student_id"]
        video_id = records.iloc[row_i]["video_id"]
        if (last_records.get(stud_id + video_id) and last_records.get(stud_id + video_id) != -1):
            last_time = last_records.get(stud_id + video_id)
            if ((last_time - time) > pause_min & (last_time - time) < pause_max):
                if (not counts.get(stud_id)):
                    counts[stud_id] = {}
                if (not counts[stud_id].get(video_id)):
                    counts[stud_id][video_id] = 1
                else:
                    counts[stud_id][video_id] += 1
                last_records[stud_id + video_id] = -1
        else:
            last_records[stud_id + video_id] = time
    return pd.DataFrame(counts).T
# pause_thresh 是暫停的自定義閥值，如間隔大於5秒才算暫停 and 小於300秒（離線）


def avg_play_back_rate(student_ntu_ids="", video_ids=""):
    total_spent_time = [x if x != 0 else 1 for x in total_spent_time]
    avg_playback_rate = [
        i/j for (i, j) in zip(total_watch_video_time, total_spent_time)]
    student_info['avg_playback_rate'] = avg_playback_rate
    pass
    # return avg_play_back_rate

# 學生平均播放速度
# input: 時間區間, 學生ID, 影片ID (optional)
# output: 該區間內/整學期 該學生 某/所有影片 的 平均播放速度
