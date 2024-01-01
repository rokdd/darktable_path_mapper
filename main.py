#for creating the cli
import click
# for logging
import logging

import sqlite3
#functions general to use
from utils import *
#function to support main functionality
from funcs import *
import json
from pathlib import Path
import shutil

@click.group()
def cli():
    pass

#configuration
HOME_DIR=os.environ["HOME"]
map={
}
#initate the logger
logger=logging.getLogger()
logger.addHandler(logging.FileHandler("log.txt"))
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
#load the mappings from the config folder
for file in Path().glob('config/mapping_*.json'):
    logger.info("Load mapping config "+str(file))
    map=merge_dict(map,json.load(open(file,"r")))

@cli.command()
@click.option('--o', prompt='Old path',default="Q:\\", help='the path you want to replace')
@click.option('--n', prompt='New path',default="/media/xyz/",  help='the path you want to map to')
def task(o,n): 
    #open the task file
    tasks_file=open("tasks.json","a+", encoding='utf-8')
    tasks=[]
    tasks_file.seek(0)
    if tasks_file.read()!="":
        tasks_file.seek(0)
        tasks=json.load(tasks_file)
        logger.info("Loaded existing tasks from tasks.json")
    tasks_file.close()
    tasks.append({"o":o,"n":n})

    tasks_file=open("tasks.json","w+", encoding='utf-8')
    json.dump(tasks, tasks_file, ensure_ascii=False, indent=4)
    logger.info("Saved tasks.json")
    tasks_file.close()

@cli.command()
def map_path(src_dir,dest_dir,replace_current=False,copy_from=HOME_DIR+"/.config/darktable/library.db"):

    tasks=json.load(open("tasks.json","r+", encoding='utf-8'))
    #tidy up for duplicates and order
    msgs,tasks=clean_tasks(tasks)
    if len(msgs)>0:
        logger.error("We cannot run because of errors")
        for m in msgs:
            logger.error(m)
        return
    
    #Start copying the database file with a backup file
    file_path=do_copy(copy_from,dir_path="backup")
    #we leave the file we copy untouched as a backup and write to the temp
    shutil.copyfile(file_path, file_path+".temp")
    file_path=file_path+".temp"
    logger.info("Database file which will be modified: {0}".format(file_path))
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    for mapping_config in map["library.db"]:
        for task in tasks:
            q="UPDATE {db} SET {field} = replace(replace({field}, '{o}', '{n}' ),'\\','/') WHERE {field} LIKE '{o}%';".format(**mapping_config,**task)
            logger.debug(q)
            cur.execute(q)
            con.commit()

    con.close()
    #nneed to be very careful...this file bight me override wthout backup
    if replace_current:
        shutil.copyfile(file_path,HOME_DIR+"/.config/darktable/library.db")
    

if __name__ == '__main__':
    cli()
