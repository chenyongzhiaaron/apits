# 常用的SQLAlchemy字段类型

## 1. 字段类型

| 类型名       | python中类型      | 说明                                                |
| :----------- | :---------------- | :-------------------------------------------------- |
| Integer      | int               | 普通整数，一般是32位                                |
| SmallInteger | int               | 取值范围小的整数，一般是16位                        |
| BigInteger   | int或long         | 不限制精度的整数                                    |
| Float        | float             | 浮点数                                              |
| Numeric      | decimal.Decimal   | 普通整数，一般是32位                                |
| String       | str               | 变长字符串                                          |
| Text         | str               | 变长字符串，对较长或不限长度的字符串做了优化        |
| Unicode      | unicode           | 变长Unicode字符串                                   |
| UnicodeText  | unicode           | 变长Unicode字符串，对较长或不限长度的字符串做了优化 |
| Boolean      | bool              | 布尔值                                              |
| Date         | datetime.date     | 时间                                                |
| Time         | datetime.datetime | 日期和时间                                          |
| LargeBinary  | str               | 二进制文件                                          |

## 2. 常用的SQLAlchemy字段选项

| 选项名       | 说明                                              |
| :----------- | :------------------------------------------------ |
| primary\_key | 如果为True，代表表的主键                          |
| unique       | 如果为True，代表这列不允许出现重复的值            |
| index        | 如果为True，为这列创建索引，提高查询效率          |
| nullable     | 如果为True，允许有空值，如果为False，不允许有空值 |
| default      | 为这列定义默认值                                  |

## 3. 常用的SQLAlchemy关系选项

| 选项名         | 说明                                                         |
| :------------- | :----------------------------------------------------------- |
| backref        | 在关系的另一模型中添加反向引用                               |
| primary join   | 明确指定两个模型之间使用的联结条件                           |
| uselist        | 如果为False，不使用列表，而使用标量值                        |
| order\_by      | 指定关系中记录的排序方式                                     |
| secondary      | 指定多对多关系中，另外一个关系表的名字                       |
| secondary join | 在SQLAlchemy中无法自行决定时，指定多对多关系中的二级联结条件 |

