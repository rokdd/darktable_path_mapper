from collections import Counter
from utils import sort_by_path_length
def clean_tasks(tasks):
    cnt_double_o=Counter([task["o"] for task in tasks])
    cnt_double_o={x: count for x, count in cnt_double_o.items() if count > 1}
    if len(cnt_double_o)>0:
        return (["The following source paths are double: "+str(cnt_double_o)],tasks)
    
    #sort the tasks by the length of the old path.. so we try to avoid the the tasks interfere and will replace each other
    tasks.sort(key=sort_by_path_length, reverse=True)
    return ([],tasks)