import pandas as pd
import re
import datetime


def load_data_helper(path, table_names):
    headers = {}
    data = {}
    student_sect = [name for name in table_names if "stud" in name]
    # utf-8-sig: encoding with utf-8 without BOM
    with open(path, "r", encoding="utf-8-sig") as f1:
        tmp_header = ""
        nextIsHeader = False
        isStudTable = False
        for line in f1.readlines():
            line = line.replace("\n", "")
            if(line in table_names):
                tmp_header = line
                data[tmp_header] = []
                nextIsHeader = True
                if(line in student_sect):
                    isStudTable = True
            elif(nextIsHeader):
                headers[tmp_header] = line.split(",")
                nextIsHeader = False
            else:
                if(isStudTable):
                    line = _strip_en_name(line)
                data[tmp_header].append(line.split(","))
    tables = {}
    for table_name in table_names:
        tables[table_name] = (pd.DataFrame(
            data=data[table_name], columns=headers[table_name]))
    del data
    return tables


def _strip_en_name(user_name):
    regex = re.compile(".*?(\(.*?\))")
    result = re.findall(regex, user_name)
    try:
        return user_name.replace(result[0], "").replace(" ", "").replace("\"", "")
    except:
        return user_name.replace("\"", "")


def to_datetime(x):
    tempt = datetime.datetime.strptime(
        x, '%Y-%m-%d %H:%M:%S %Z') + datetime.timedelta(hours=8)
    return tempt.hour*100 + tempt.minute


def set_date_index(df, col):
    df[col] = pd.to_datetime(df[col])
    df.set_index(col, inplace=True)
    return df


def filter_id_helper(df, fltr_col, values):
    if (len(values) == 0):
        return df
    return df[df[fltr_col].isin(values)]


def slice_time_helper(df, fltr_col, start, end):
    df[fltr_col].apply(lambda x: pd.to_datetime(x))
    if (start == ""):
        start = df[fltr_col].min()
    if (end == ""):
        end = df[fltr_col].max()
    return df.loc[(df[fltr_col] >= start) & (df[fltr_col] <= end)]
