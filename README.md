# palworld-restartandbackup
幻兽帕鲁自动重启服务器&amp;备份脚本

- 环境依赖:python(3.8.10测试可用)
  - 三方库:schedule psutil

# [重启功能设置]
PROCESS_NAME = "PalServer-Win64-Test-Cmd.exe"  # server进程

MEN_THRESHOLD = 13*1024  # 重启内存阈值(MB)

RESTART_TIME = ["04:00", "11:00", "18:00"]  # 定时重启

SERVER_PATH = r"C:\Users\Administrator\Desktop\Server\palworld\steamcmd\steamapps\common\PalServer\PalServer.exe"  # server路径

# [备份功能设置]

BACKUP_SOURSE_FOLDER = r'C:\Users\Administrator\Desktop\Server\palworld\steamcmd\steamapps\common\PalServer\Pal\Saved\SaveGames\0'  # 存档源文件夹路径

BACKUP_BASE_FOLDER = r'C:\Backups'  # 备份文件夹的基础路径

BACKUP_INTERVAL = 15*60  # 备份间隔时长(seconds)

# [运行]

命令行执行`python restartandbackup.py`直接运行即可
