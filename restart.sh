#!/bin/bash


# 激活conda虚拟环境
source activate freqtrade

# 查找名为freq的进程
pid=$(pgrep -f freq)

# 如果找到进程，则重启进程
if [ -n "$pid" ]; then
  echo "Found process with PID $pid. Restarting..."
  sudo kill $pid
  nohup freqtrade trade --config user_data/config_future.json --strategy SampleStrategy &
else
  echo "No freq process found. Starting freqtrade..."
  nohup freqtrade trade --config user_data/config_future.json --strategy SampleStrategy &
fi
