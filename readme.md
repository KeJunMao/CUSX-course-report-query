# 传媒成绩查询

这是一个自动查询山西传媒学院成绩的小工具

## 安装依赖

```bash
pip3 install dotenv bs4 requests
cp .env.template .env
```

修改 `.env` 的内容

## 使用

> 注意！本工具会自动把评教任务完成并且都选 A

### 单人查询

```bash
python single.py
```

- 如果没有修改过密码输入学号即可回车
  ```
  请输入学号和密码：2020202020
  ```
- 如果修改过密码，使用空格分割密码
  ```
  请输入学号和密码：2020202020 password
  ```

会自动复制到剪贴板，可以方便的粘贴给你的朋友们！

### 整班查询

整班查询会使用学号遍历查询

```bash
python group.py
```

```bash
请输入学号前8位：20202020
请输入班级人数：38
# 直接回车 密码无误
请确认学号密码(('2020202001', '2020202001'))：
# 输入字符串 修改密码
请确认学号密码(('2020202002', '2020202002'))：02020202
# 输入 -i 不再确认密码
请确认学号密码(('2020202003', '2020202003'))：-i
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](./LICENSE.txt)
