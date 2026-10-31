# List 列表是 Python 中的一种数据结构，可以用来存储多个元素。
#   列表是有序的，意味着元素的顺序是固定的。
#   列表是可变的，意味着可以添加、删除或修改元素。
#   列表可以存储不同类型的元素，例如整数、浮点数、字符串、列表等。

## 初始化和赋值
list_a = []
list_a.append(1)
list_a.append("a")
list_a.append(1.2)
list_a.append([10,20,30])
print(list_a)

## 插入值
### 列表尾部加入值：append(value)
### 列表里插入值：insert(index, value)
### 列表尾部追加另一个可迭代对象iterable（列表、元组、集合）： extend(iterable)
list_a.insert(2, "haha")
list_a.extend(["apple", "banana", "orange"])
print(list_a)

## 删除值
### remove(value): 按值删除，移除列表中指定内容，如果不存在，则抛出ValueError报错
list_a.remove("haha")
print(list_a)
# list_a.remove(222)  # 报错

### pop(index)：按索引删除，移除并返回index位置的元素。如果不指定index，则删除并返回末尾元素
print(list_a.pop(2)) # 输出： 1.2
print(list_a.pop()) # 输出： "orange"

### del关键字: python内置的内存删除操作，既可以根据index删除指定元素，也可以使用切片语法删除连续的子列表
del list_a[2]
print(list_a)
del list_a[1:3]
print(list_a)

### clear()：一键清空列表，但是列表对象本身还保留内存中
list_b = list_a.copy()
print(f"list_b -> {list_b}")
list_b.clear()
print(f"list_b -> {list_b}")

## 遍历和迭代
### 基础遍历：使用 for...in 循环可以按顺序提取列表中的元素，底层基于迭代器模式，无需手动维护索引。
for a in list_a:
    print(a)

### 索引和元素双提取： enumerate()
for index, a in enumerate(list_a, start=1):
    print(f"index -> {index}, value -> {a}")

### 列表推导式（List Comprehension）是 Python 中用来快速生成和过滤列表的优雅语法
#### 结构：表达式 for 变量 in 可迭代对象 if 条件
####   表达式：你要放入新列表中的元素，或者对元素进行的操作。
####   for 循环：遍历现有的序列。
####   if 条件：（可选）用于过滤，只有满足条件的元素才会被处理并放入新列表。
#### 如果需要根据if对结果进行替换，那么结构：
####    结果A if 条件 else 结果B for 变量 in 可迭代对象
#### 结构1：
tasks = ["write test case", "run", "submit bug"]
new_tasks = [task for task in tasks if task.startswith("write")]
print(new_tasks)

#### 结构2：
new_tasks_2 = [task if task.startswith("write") else print(task) for task in tasks]
print(f"new_tasts_2 -> {new_tasks_2}")

# #### 传统写法：
# new_tasks = []
# for task in tasks:
#     if(task.startswith("write")):
#         new_tasks.append(task)
# print(new_tasks)

## 模式解构（Destructuring）
### 模式解构（Destructuring）是 match-case 语法最强大的特性之一。它能够在校验数据结构的
### 同时，直接将嵌套在深层的元素按位置或键名提取为独立的变量。
### 使用通配符*，可以快速的解析长度不定的列表
event_log = ["warning", "db_timeout", "192.168.1.1", 5000]
match event_log:
    # 精确匹配仅有两个元素的列表
    case ["error", msg]:
        print(f"发生错误: {msg}")
    # 匹配以 warning 开头，并提取第 2、3 个元素，剩余元素打包给 rest
    case ["warning", issue, ip, *rest]:
        print(f"警告类型: {issue}, 来源IP: {ip}, 附加数据: {rest}")
    # 匹配至少有一个元素的列表，提取首个元素，忽略其他
    case [level, *_]:
        print(f"未知级别事件: {level}")

## 列表与字符串的相互转换
### 字符串拆分成列表： spilt(seq)
### 按照指定的分隔符对字符串进行拆分，如果没有指定分隔符，则默认按照空白符进行拆分
### 这种操作在提取一段文本中的关键词时非常有用。
### 注意，spilt()方法一次只能用一种分隔符，如果要多个分隔符，有两种办法：先替换再分割；正则表达式
text = "apple, banana orange"
result = text.replace(",", " ").split()
print(result)

import re
result_1 = re.split(r'[,\s]+', text)
print(result_1)

### 列表拼接成字符串： join(iterable)
fruits = ["apple", "banana", "orange"]
result = ", ".join(fruits)
print(result)

### 列表切片
### 列表切片的语法和字符串切片的完全一致 [start:stop:step]


## 列表排序
### sort()：列表对象的专属方法。
### 直接在原列表上排序，执行完毕返回None。 
### 默认升序，使用参数“reverse=True”执行降序
numbers = [1, 6, 3, 8, 7, 9]
print(numbers.sort())
print(f"numbers -> {numbers}")
numbers.sort(reverse=True)
print(f"numbers -> {numbers}")

### sorted(): python内置的全局方法。
### 它可以接受任何iterable对象（列表、字典、元组，甚至字符串）,并在排序后，返回一个新的对象，而不破环原始对象
oragin_score = [11, 55, 34, 99, 50]
sorted_score = sorted(oragin_score)
print(f"oragin_score -> {oragin_score}")
print(f"sorted_score -> {sorted_score}")

### 高级自定义排序：使用key参数
### 无论是sort()还是sorted()，都支持传入一个key参数。可以指定一个函数（内置方法、自定义方法、lambda匿名方法）
### python会根据每个元素在这个方法里的计算结果来进行排序

#### 示例 A：按字符串的长度进行排序，而不是按字母表先后
words = ["apple", "banana", "orage", "kiwi"]
words.sort(key = len)  # len是python内置方法
print(f"words -> {words}")

#### 示例 B：处理结构化数据（非常适合你在 AI 评测脚本中处理测试结果）
eval_results = [
    {"model": "Model_A", "score": 88},
    {"model": "Model_B", "score": 95},
    {"model": "Model_C", "score": 72}
]
# 提取字典里的 'score' 作为排序依据，并使用 reverse=True 降序排列
# lambda x: x["score"] 意思是：把每一个字典丢进去，拿出它的 score 值用来比大小
ranked_model = sorted(eval_results, key = lambda x: x["score"], reverse=True)
for item in ranked_model:
    print(f"model: {item['model']}, score: {item['score']}")


# 字典 Dictionary
# python中用于存储键值对（key-value）的数据结构；
# 字典是有序的，所以是后进先出，
# key唯一且不变，可以是字符串或者数字
# value可以是任意数据类型

## 基础操作和数据获取
### 安全读取
### 使用my_dict[key]读取数据，如果key不存在，会触发KeyError
### 推荐使用my_dict.get(key, default)方法，如果key不存在，返回default值
my_dict = {"apple": 5, "banana": 10, "orange": 15}
# print(my_dict["kiwi"])
print(my_dict.get("kiwi", 0))

### 新增与更新
### 直接使用赋值语法 my_dict[new_key] = new_value。如果该键已存在，原有的值会被覆盖更新；
### 如果不存在，则会在字典中自动创建新的键值对。
my_dict["kiwi"] = 20
print(my_dict.get("kiwi", 0))
my_dict["kiwi"] = 30
print(my_dict.get("kiwi", 0))

### 删除
### 可以使用 del my_dict[key] 直接删除指定项，
### 或者使用 my_dict.pop(key) 在删除的同时将该键对应的值提取出来赋值给其他变量。
### 使用popitem()，删除最后进入字典的键值对，注意，如果字典为空，会抛出KeyError
del my_dict["kiwi"]
print(my_dict)
dict_1 = my_dict.pop("apple")
print(dict_1)
dict_2 = my_dict.popitem()
print(dict_2)
print(my_dict)

## 字典的遍历与迭代
### 使用 .items()方法，常用语句：for key, value in dic.items()
### 如果只需要key，可以直接遍历 .keys()提取所有key
### 如果只需要values，可以遍历 .values()提取所有值
my_dict = {"apple": 5, "banana": 10, "orange": 15}
for key, value in my_dict.items():
    print(f"key -> {key}, value -> {value}")
for key in my_dict.keys():
    print(f"key -> {key}")
for value in my_dict.values():
    print(f"value -> {value}")


# 集合SET
# SET是无序、元素唯一的可变容器
# 它的底层实现是基于哈希表，所以它在“判断某个元素是否存在时”效率极高
# 注意：集合本身是可变的，但是集合内存放的元素是严格不可变的，
#   这就意味着只能把字符串、数字、元组放入集合中。
#   如果试图把列表、字典放进去，就会报错TypeError

## 初始化集合
## 必须使用set()来初始化一个集合。
## 如果直接写{}，会被初始化成空字典
set_1 = set()

## 增删元素
### add(): 增加元素
### remove(): 删除元素，不存在时会报错
### discard(): 安全的删除元素，不存在不会报错
set_1.add("apple")
set_1.add("banana")
set_1.add("orange")
print(f"set_1 -> {set_1}")
set_1.remove("banana")
# set_1.remove("kiwi") # KeyError
set_1.add("kiwi")
set_1.discard("cherry")
set_1.discard("apple")
print(f"set_1 -> {set_1}")

# set_1.add([1,2,3]) # TypeError: unhashable type: 'list'
# set_1.add({"apple": 1}) # TypeError: unhashable type: 'dict'

## 快速去重
## 将一个包含重复数据的列表，转换为集合，是python中最经典的去重方法
raw_list = ["apple", "banana", "apple", "orange", "banana"]
my_set = set(raw_list)
print(my_set)

## 高效成员测试
## 使用in()来判断某个数据是否在集合中，速度远超在列表中遍历查找。
## 使用黑名单拦截，白名单校验等场景
if "apple" in my_set:
    print("apple in set")

## 数学交并补运算
## 集合原生支持数学中的交集(&)、并集(|)、差集(-)等运算，
## 在对比两组数据的公共部分和差异部分是异常强大
group_a_users = {"Alice", "Bob", "Charlie"}
group_b_users = {"Bob", "David", "Eve"}
# 交集（&）
common_users = group_a_users & group_b_users
print(f"common_users -> {common_users}")
# 并集（|）
all_users = group_a_users | group_b_users
print(f"all_users -> {all_users}")
# 差集（-）
only_in_a = group_a_users - group_b_users
print(f"only_in_a -> {only_in_a}")



## 子集和超集
### issubset() 或者 <= ： 判断当前集合里的所有元素是不是都在另一个集合中。
### issuperset() 或者 >= : 判断当前集合是否完全包含了另一个集合的所有元素。
set_sub = {1, 2, 3}
set_super = {1, 2, 3, 4, 5}
print(set_sub.issubset(set_super))
print(set_super.issuperset(set_sub))

## 冻结集合（frozenset）
## frozenset是一种特殊的不可变集合，一旦创建，不可添加或者删除元素
### 创建方法：
# 将列表转换为冻结集合
frozen_cities = frozenset(["Beijing", "NewYork", "London"])
print(f"cities -> {frozen_cities}")  # 输出：frozenset({'London', 'Beijing', 'NewYork'})

# 将普通集合转换为冻结集合
normal_set = {1, 2, 3}
frozen_nums = frozenset(normal_set)
print(f"nums -> {frozen_nums}") # 输出：frozenset({1, 2, 3})

### frozenset的使用场景1：作为字典的key。
### 当你需要一组《唯一且无序》的元素作为字典的索引是，frozenset是唯一合法的集合类型
# 假设我们记录不同航班航线（无序）的每日班次
routes_count = {
    frozenset({"北京", "上海"}): 12,
    frozenset({"广州", "深圳"}): 8
}
# 无论查询时传入的城市先后顺序如何，只要元素相同就能匹配到
search_key = frozenset({"上海", "北京"})
print(routes_count.get(search_key))  # 输出: 12

### frozenset的使用场景2：存放在另一个集合内部。
### 如果你需要在一个 set 内部存放多个集合，内部的集合必须使用 frozenset
group_a = frozenset({1, 2})
group_b = frozenset({3, 4})
# 将这两个冻结集合放入一个普通的 set 中，这对于普通 set 是不允许的
all_groups = {group_a, group_b}
print(all_groups)


# 元组TUPLE
# 元组是有序、不可变的数据容器，一旦创建，内部元素不可增删改
# 注意：元组一旦定义，那么每个位置的数据就不能变了，但是如果是某个位置的数据本身是列表之类的容器，那么容器里的数据是可以改变的。

## 定义和创建
### 常规定义：使用小括号()来定义元组
tuple_a = (1, 2, 3)
print(tuple_a)
### 无括号定义：只要是用逗号隔开多个单独的值，就算没有小括号，也会被打包成元组
tuple_b = "a", "b", "c", 1, 2, 3
print(tuple_b)
### 注意：单元素的元组，必须在第一个元素后添加逗号，否则会被当作数字或者字符串处理。
tuble_c = (1,)
print(tuble_c)

## 操作和高级解构
### 只读操作，支持与列表完全一致的索引读取和切片读取
db_config = ("127.0.0.1", 3306, "root", "password")
print(f"Port -> {db_config[1]}")
print(f"last 2 config -> {db_config[-2:]}")

### 多变量解包，可以一次性赋值给相同数量的变量
### 星号 * 吸收剩余元素。当你不确定元组长度，或者只关心前几个值时，可以使用星号将剩余部分打包成一个列表。
### 占位符 _ 忽略不需要的元素。如果你只需要元组中的某一个值，可以使用下划线作为哑变量
host, port, user, pw = db_config
print(f"用户 {user} 正在连接 {host}:{port}")
h1, *rest = db_config
print(f"host -> {h1}, rest -> {rest}")
_, p2, *rest = db_config
print(f"port -> {p2}")

### 元组与列表的相互转化
### 元组 -> 列表： list()
tuple_d = (1, 2, 3)
list_d = list(tuple_d)
print(f"tuple -> {tuple_d}, list -> {list_d}")
### 列表 -> 元组： tuple()
tuple_e = tuple(list_d)
print(f"tuple -> {tuple_e}")

## 核心应用场景（为什么不用列表？）
### 数据防篡改：
###     不可变性使其成为传递核心配置或系统常量的理想选择，能从物理层面防止数据在函数传递过程中被意外修改。

### 可哈希与字典键：
###     因为元组不可变，只要元组内部嵌套的所有元素也都不可变（如全是数字或字符串），
###     该元组就可以直接作为字典的键（Key），或者被存入集合中。
# 作为字典的键 (记录二维坐标点的温度)
temperature = {
    (0, 0): 25.5,
    (10, 5): 22.1
}
print(f"原点温度 -> {temperature[(0, 0)]}") # 输出: 25.5

### 底层性能优势：
###     由于结构固定，元组在底层的内存分配比列表更紧凑，整体的迭代遍历速度也略快于列表。