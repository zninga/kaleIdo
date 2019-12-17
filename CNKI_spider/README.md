`python+selenium` 简单获取知网硕博论文.

**Usage:**

```bash
usage: app.py [-h] [-su SUBJECT [SUBJECT ...]] [-ky KEYWORD [KEYWORD ...]]              [-s SCHOOL [SCHOOL ...]] [-fy FROM_YEAR] [-ty TO_YEAR] -o OUTPUToptional arguments:
  -h, --help            show this help message and exit
  -su SUBJECT [SUBJECT ...], --subject SUBJECT [SUBJECT ...]
                        主题
  -ky KEYWORD [KEYWORD ...], --keyword KEYWORD [KEYWORD ...]
                        关键词
  -s SCHOOL [SCHOOL ...], --school SCHOOL [SCHOOL ...]
                        学位授予单位
  -fy FROM_YEAR, --from_year FROM_YEAR
                        学位授予年度(开始范围)
  -ty TO_YEAR, --to_year TO_YEAR
                        学位授予年度(截止范围)
  -o OUTPUT, --output OUTPUT
                        输出文件名
```

**e.g.**

```bash
python app.py -su 深度学习 神经网络 -ky 深度学习 神经网络 -s 清华大学 中国科学院大学 -fy 2015 -ty 2018
```

