# 贡献指南

本项目采用宽松的开源协议 MIT，欢迎大家贡献代码。

## 运行代码

```bash
$ virtualenv venv
$ source venv/Scripts/activate
(venv) $ pip install -r requirements.txt
(venv) $ python main.py
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
