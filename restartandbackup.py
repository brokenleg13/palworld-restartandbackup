import psutil
import time
from datetime import datetime
import subprocess
import os
import shutil
import schedule

# [重启功能设置]
PROCESS_NAME = "PalServer-Win64-Test-Cmd.exe"  # server进程
MEN_THRESHOLD = 13*1024  # 重启内存阈值(MB)
RESTART_TIME = ["04:00", "11:00", "18:00"]  # 定时重启
SERVER_PATH = r"C:\Users\Administrator\Desktop\Server\palworld\steamcmd\steamapps\common\PalServer\PalServer.exe"  # server路径

# [备份功能设置]
BACKUP_SOURSE_FOLDER = r'C:\Users\Administrator\Desktop\Server\palworld\steamcmd\steamapps\common\PalServer\Pal\Saved\SaveGames\0'  # 存档源文件夹路径
BACKUP_BASE_FOLDER = r'C:\Backups'  # 备份文件夹的基础路径
BACKUP_INTERVAL = 15*60  # 备份间隔时长(seconds)


# 通过进程名查找进程
def find_process_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc
    return None


# 获取进程的内存信息（以MB为单位）
def get_process_memory_info(process):
    memory_info = process.memory_info()
    memory_usage = memory_info.rss / (1024 * 1024)  # 内存占用转换为MB单位
    memory_usage_mb = round(memory_usage, 2)  #
    memory_percent = round(process.memory_percent(), 2)
    return {
        'pid': process.pid,
        'name': process.name(),
        'memory_usage': memory_usage_mb,
        'memory_percent': memory_percent
    }


# 监控特定进程的内存信息
def monitor_process_memory(process_name):
    while True:
        process = find_process_by_name(process_name)
        if process is None:
            print("未找到进程：", process_name)
            return None
        else:
            memory_info = get_process_memory_info(process)
            memory_info_format = {
                'pid': memory_info['pid'],
                'name': memory_info['name'],
                'memory_usage': memory_info['memory_usage'],
                'memory_percent': memory_info['memory_percent']
            }
            return memory_info_format


def terminate_process_by_name(process_name):
    # todo 添加机器人
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            proc.terminate()


def backup_archive():
    print("任务执行中...备份存档")
    # 检查备份基础文件夹是否存在，如果不存在，则创建它
    if not os.path.exists(BACKUP_BASE_FOLDER):
        os.makedirs(BACKUP_BASE_FOLDER)
        print(f'备份文件夹{BACKUP_BASE_FOLDER}已创建.')

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_folder = os.path.join(BACKUP_BASE_FOLDER, f'Backup_{timestamp}')
    try:
        # 复制整个文件夹
        shutil.copytree(BACKUP_SOURSE_FOLDER, backup_folder)
        print(f'成功于{backup_folder}完成备份')
    except Exception as e:
        # 如果发生任何错误，打印错误信息
        print(f'备份错误: {e}')


def restart_server():
    print("任务执行中...重启服务器")
    subprocess.Popen([SERVER_PATH, f'--port=8211'])
    time.sleep(2)
    terminate_process_by_name(PROCESS_NAME)


def bind_schedule():
    print("------------绑定重启和备份任务-------------")
    schedule.every(BACKUP_INTERVAL).seconds.do(backup_archive)
    for time in RESTART_TIME:
        schedule.every().day.at(time).do(restart_server)


def main():
    backup_archive()  # 启动时备份一次
    while True:
        schedule.run_pending()
        mem_msg = monitor_process_memory(PROCESS_NAME)
        if mem_msg:
            # 内存超过阈值终止进程
            if mem_msg["memory_usage"] > MEN_THRESHOLD:
                print(f"当前内存占用{mem_msg['memory_usage']}已超过阈值，重启服务器")
                terminate_process_by_name(PROCESS_NAME)
            else:
                time.sleep(10)
        else:
            print("-------------启动服务器-----------------")
            subprocess.Popen([SERVER_PATH, f'--port=8211'])
            time.sleep(2)


# 调用主函数
if __name__ == "__main__":
    bind_schedule()
    main()
