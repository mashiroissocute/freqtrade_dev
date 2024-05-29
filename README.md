# 币安价格提醒程序

当前价格/时段内最高价格<指定百分比A

当前价格/时段内最低价格>指定百分比A百分比A

发出通知到叮叮机器人

<img width="420" alt="image" src="https://github.com/mashiroissocute/freqtrade_dev/assets/22027940/a0951db0-0b3d-4158-8a44-62ba13d12b5f">


## 程序启动方法

- 1.登录云服务器
- 2.进入程序目录 `cd /usr/local/service/freqtrade_dev`
- 3.启动程序 `./restart.sh`

## 如何修改参数

程序代码参数如图所示:

<img width="511" alt="image" src="https://github.com/mashiroissocute/freqtrade_dev/assets/22027940/3f9ee339-739a-4639-9102-f22d5de6af60">

### 修改时间段

- 1.进入程序目录 `cd /usr/local/service/freqtrade_dev`
- 2.编辑文件`vim user_data/strategies/sample_strategy.py`
- 3.修改`period = IntParameter(5, 205, default=48, space="buy")`这一行的default值，该值单位为5分钟。（例如要设置4小时，那么 4小时 = 5分钟 * 48，我们需要将default修改为48）
- 4.保存文件后重启程序 `./restart.sh`

### 修改百分比A

- 1.进入程序目录 `cd /usr/local/service/freqtrade_dev`
- 2.编辑文件`vim user_data/strategies/sample_strategy.py`
- 3.修改`highThr = IntParameter(0, 1, default=0.95, space="buy")`这一行的default值。
- 4.保存文件后重启程序 `./restart.sh`

### 修改百分比B

- 1.进入程序目录 `cd /usr/local/service/freqtrade_dev`
- 2.编辑文件`vim user_data/strategies/sample_strategy.py`
- 3.修改`lowThr = IntParameter(0, 1, default=1.05, space="buy")`这一行的default值。
- 4.保存文件后重启程序 `./restart.sh`



This software is for educational purposes only. Do not risk money which
you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS
AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.

We strongly recommend you to have coding and Python knowledge. Do not
hesitate to read the source code and understand the mechanism of this bot.


