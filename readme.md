# CUSX course report query

这是一个自动查询山西传媒学院成绩的小工具

## 安装依赖

```bash
pip3 install dotenv bs4 requests sqlalchemy pandas
cp .env.template .env
```

修改 `.env` 的内容

## 使用

> 注意！本工具会自动把评教任务完成并且都选 A

### 单人查询

单人查询会先查询本地数据库，没有再去爬取，也可以指定强制

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
- 后缀输入 --force 即可强制爬取并更新数据库
  ```
  请输入学号和密码：2020202020 password --force
  请输入学号和密码：2020202020 --force
  ```
  会自动复制到剪贴板，可以方便的粘贴给你的朋友们！

### 整班查询

整班查询会使用学号遍历查询，会先查询本地数据库，没有再去爬取

> 考虑到数据量，不支持强制爬取

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

### 统计分析

```bash
python ranking.py
```

将生成各个科目的成绩统计

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 支持我

![爱票](https://i.loli.net/2021/07/31/A45etf1sJ2ZMBHl.png)

> 微信扫码支持我创业！

## License

[MIT](./LICENSE.txt)
