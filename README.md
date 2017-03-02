# 不用很麻烦很累就能翻译游戏
从游戏内存中抓取文本信息，通过机器翻译API或众包翻译平台获取翻译后的文本后以字幕的方式叠加在游戏画面上。免去了较为繁琐的汉化游戏的流程。

目前，本项目的主要适配目标为在Windows平台上的各类模拟器内运行的文字游戏。

# 适配游戏列表
**PSP** 

目前只支持在PPSSPP 1.3 32位版本中模拟运行的PSP游戏，不支持其它PPSSPP版本及PSP真机。

**psp.lxzs1** 流行之神1 

（备注：在启动server.py后如果无法抓取到文本，请在PPSSPP中存储一次即时存档再加载，或加载以前成功激活文本抓取后保存的即时存档）。

**psp.lxzs2** 流行之神2

# 使用方式
1、安装Python 2.7（不支持Python3）： https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi 。

2、安装需要的组件，在命令提示符中执行：python -m pip install psutil。

3、**启动游戏之后**，在命令提示符中输入：server.py 游戏列表中的游戏名（例如：server.py psp.lxzs1），开启用于抓取文本的服务。

4、在浏览器中打开 http://44670.org/fanyi ，即可在网页中查看抓取到的文本并进行翻译。

5、如果需要将结果以字幕的形式叠加显示到屏幕上，启动frontends_bin\frontend_overlay.exe（需要.NET Framework 4）。


