## step

- 执行main.py文件，会同时爬取四大大坝的内容。。。在/spiders/gezhouba.py文件122 line左右修改爬取时间
- 数据在data目录下

- 由于每台机器写入速度不同，可能会出现乱序的情况，解决办法如下两点

- 方法１：进入spider目录下的各个py文件，以gezhouba.py为例，增加line 138 休眠时间

- 方法２：每次只爬一个大坝数据，具体做法：注释main.py里面关于其他大坝的line，注释settings.py里面对应的其他大坝的pipeline(具体在69line左右)

  ​