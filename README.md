# 小红书自动爬取

自动爬取小红书文章/视频,可自定义爬取内容(标题/正文/评论/回复)

## 效果展示(详见使用方法中的演示视频)

![演示案例](show/动画.gif)
![txt文件](show/txt.png)
![csv文件](show/csv.png)

## 依赖

- 下载python包依赖

  ```shell
  pip install -r requirements.txt
  ```

- 安装谷歌浏览器和谷歌浏览器驱动,并配置环境变量<br>
  [安装教程](https://www.cnblogs.com/lfri/p/10542797.html)<br>
  check your Google browser's version, choose the closest version and download corresponding GoogleDriver from [position1](http://chromedriver.storage.googleapis.com/index.html) or [position2](https://npm.taobao.org/mirrors/chromedriver/).And then move `chromedriver.exe` under `C:\Program Files\Google\Chrome\Application` and the same folder with your python explainer. Then add `C:\Program Files\Google\Chrome\Application` to your `system path`.

- 安装fiddler抓包工具
  - [fiddler安装教程1](https://blog.csdn.net/ychgyyn/article/details/82154433)
  - [fiddler安装教程2](https://www.cnblogs.com/katyhudson/p/12517680.html)
  - **如果使用时界面频繁出现黄色警告 `the system proxy was changed` ,需要检查并删除更改代理的应用**
    - 火狐浏览器插件->银联(删除)
    - easyconnect(删除)
    - 关闭其他代理软件(懂的都懂)
  > 目前笔者手机(华为p30)连接尚未成功,可以连接http/https但是部分应用无法联网,诸多解决办法均已尝试但仍然失败,如果有人成功请务必与我联系,本项目不需手机连接

## 使用方法

- [使用视频介绍-2022/3/27补丁更新]
- [视频介绍](https://github.com/learner-lu/xiaohongshu-spider/releases/download/v0.0.1/2022-03-13.17-53-57.mkv) **使用前请下载观看**
- [爬虫设计与实现思路-B站视频](https://www.bilibili.com/video/BV1ob4y1H7vL?spm_id_from=333.999.0.0)
- 文字介绍
  - 打开fiddler(保证底部导航栏有图标),设置filters->show only the following host->`t.xiaohongshu.com`
  - 电脑端打开微信小程序小红书(保证底部导航栏有图标)
  - 点击fiddler->file->save->select sessions->as text: 选择默认保存路径为该项目的data文件夹下(./data)
  - 基本用法:

    ```python
    python main.py 文字(中/英)
    ```

  - 参数介绍

    - **添加默认缩放比例(前提)**
      > 由于笔记本可能采用屏幕缩放(100% 150%),**不修改此项会导致图像匹配失败**
      >
      > pyautogui作者亲自回答了这个问题: [pyautogui图像匹配失败,分辨率?](https://stackoverflow.com/questions/45302681/running-pyautogui-on-a-different-computer-with-different-resolution),作者推荐重新截图,但是我使用了一种其他的方式解决这个问题,目前看来是可行的

      桌面右键 -> 显示设置 -> 缩放, 可以找到您当前屏幕的缩放尺寸.笔记本可能采用屏幕缩放(100% 150% 200%)

      scale后修改为您屏幕的缩放大小(默认100),该项只需再运行前修改一次,将全局保存您的修改,此后均不需执行此项,如果更换显示设备需重新配置.

      ```python
      python main.py --scale 150
      ```

      > 由于多次resize会导致图片匹配效果较差,故不支持恢复操作. 我备份了所有图片(image_folder_copy),如果需要可以删除并替换

    - **加入搜索的内容(必)**,使用空格分隔,支持多个查找

      ```python
      python main.py 樱花 小鸟 鱼
      ```

    - **`--target(选)`**: 修改匹配数量,默认100个(小红书小程序搜索上限),可以调低

      ```python
      python main.py 程序员 --target 30
      ```

    - `-f`: 单独执行fiddler文件解析(不常用,需要使用时会有提示)

      ```python
      python main.py 程序员 -f
      ```

    - `--reset`: 重置配置文件,图片不会恢复原尺寸

      ```python
      python main.py --reset
      ```

## 学习资料

- [pyautogui教程](https://blog.csdn.net/weixin_43430036/article/details/84650938)
- [pyautogui官网](https://pyautogui.readthedocs.io/en/latest/)
- [fiddler高级用法](https://blog.csdn.net/qq_36447759/article/details/83619944)
