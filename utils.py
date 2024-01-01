import os
import shutil

def do_copy(file, n_times=9999999999,dir_path="/tmp"):
    assert os.path.exists(dir_path)
    name, ext = os.path.splitext(file)
    filename=os.path.basename(name)
    for n in range(1, n_times+1):
        new_file = os.path.join(dir_path, f"{filename}-{n}{ext}")
        if os.path.exists(new_file):
            continue
        shutil.copy(file, new_file)
        return new_file
    
def merge_dict(bottom: dict, top: dict) -> dict:

    ret = {}

    for _tmp in (bottom, top):
        for k, v in _tmp.items():
            if isinstance(v, dict):
                if k not in ret:
                    ret[k] = v
                else:
                    ret[k] = merge_dict(ret[k], v)
            else:
                ret[k] = _tmp[k]
    return ret

def sort_by_path_length(value):
    return len(value["o"])

