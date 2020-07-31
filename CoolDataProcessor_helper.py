import pandas as pd
import re
def load_data_helper(path, table_names):
    headers = {}
    data = {}
    student_sect = [name for name in table_names if "stud" in name]
    #utf-8-sig: encoding with utf-8 without BOM
    with open(path, "r",encoding="utf-8-sig") as f1:
        tmp_header = ""
        nextIsHeader = False
        isStudTable = False
        for line in f1.readlines():
            line = line.replace("\n","")
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
        tables[table_name] = (pd.DataFrame(data= data[table_name], columns = headers[table_name]))
    return tables



def _strip_en_name(user_name):
    regex = re.compile(".*?(\(.*?\))")
    result = re.findall(regex, user_name)
    try:
        return user_name.replace(result[0],"").replace(" ","")
    except:
        return user_name