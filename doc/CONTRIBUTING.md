# 贡献指南

本项目采用了GPL3开源协议，意味着如果您想对项目进行修改，做一个自己的版本的赛博小鱼缸并发布，也必须开源，并且使用GPL3协议。

之所以采用这个协议是因为此项目依赖了 pyqt5。（pyqt5 采用了 GPL3 协议，GPL3协议规定任何修改、衍生代码的发布都必须以GPL3协议开源。）

GPL3协议具有传染性。这个项目自2024年6月份之后很少再更新了。以后可能会用其他的技术栈重写。

## 运行代码

linux 下运行：

```bash
$ virtualenv venv
$ source venv/Scripts/activate
(venv) $ pip install -r requirements.txt
(venv) $ python main.py
```

windows 下运行：

```commandline
pip install virtualenv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 推荐的 git 提交规范

通常以一个英文单词+英文冒号+空格开头，后面跟上具体描述。

包括但不限于：

feat: 新功能（feature）

fix: 修复 bug

docs: 文档（documentation）

style: 格式（不影响代码运行的变动）

refactor: 重构（即不是新增功能，也不是修改 bug 的代码变动）

test: 增加测试

enhance: 优化相关代码，包括可读性和性能上的优化等

特殊情况除外，例如 “remove dead code”

## 打包

在打包时候windowsDefer可能会报警。允许一下再继续打包

windows下：

```sh
# 进入虚拟环境
venv\Scripts\activate
# 安装pyintaller
pip install pyinstaller
# 打包
pyinstaller --onefile --windowed --icon=./assets/icon.ico main.py -n cyber-life
```

windows通过配置文件进行打包：

```sh
# 进入虚拟环境
venv\Scripts\activate
# 安装pyinstaller
pip install pyinstaller
# 打包
pyinstaller main.spec
```

配置文件内容：

```
# -*- mode: python ; coding: utf-8 -*-
# 将文件放在项目根目录下，命名为 main.spec，运行 `pyinstaller main.spec` 进行打包

block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[('assets', 'assets')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='cyber-life',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='assets/icon.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')

```