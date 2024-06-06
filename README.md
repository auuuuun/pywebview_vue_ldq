
<div align="center">
    <h1>pywebview_vue_ldq</h1>
    <h4>使用pywebview制作的桌面端(vue+element ui)连点器工具</h4>
</div>

#### github pywebview原主页
    https://github.com/r0x0r/pywebview
#### pywebview官方文档
    https://pywebview.flowrl.com/
#### 程序入口
    main.py
#### 安装
    pip install -r requirements.txt
#### 打包指令，没有黑窗口，并且把静态文件打包进去
    pyinstaller -F -w --add-data="static;static" -n="鼠标连点器v1.0" -i my.ico main.py
#### 参数解释 
    -F = --onefile 单文件打包
    -w = --noconsole 打包时指定不生成控制台窗口。
    --add-data="static;static" 打包静态文件
