
import os

# 基础路径
BASE_DIR = "/mnt/nvme1/fmy/LiveVQApro"
DATA_DIR = os.path.join(BASE_DIR, "data/raw_data")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# API配置
CONFIG = {
    "api_key": "",
    "model": "gpt-4.1",
    "max_workers": 8, 
    "temperature": 0.7,  
    "max_tokens": 2000
}
