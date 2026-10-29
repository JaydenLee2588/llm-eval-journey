# 变量命名核心规则
#  1. 只能包含字母、数字和下划线（A-z, 0-9, _）。
#  2. 绝对不能以数字开头（例如 1user 是错误的，user1 是合法的）。
#  3. 不能使用 Python 的内置关键字（如 if、for、class、True 等）   4.。
#  4. 推荐使用小写字母加下划线来分隔单词（即蛇形命名法，例如 account_balance），这符合 Python 的官方代码规范。


# 变量类型
username = "xiaohong"   # string
age = 18    # Integer
height = 1.78   # Decimal
is_student = True   # Boolean

from decimal import Decimal
print("Hello Python, I'm back!!!")

# 数值计算
a = 1
b = 2
print(a+b)

## 知识点: 浮点数的精度存储
a = 1.1
b = 2.2
print(a+b) # 3.3000000000000003
## 延申：
print(f"{a + b:.2f}")  # 输出: 3.30
print(round(a + b, 2)) # 输出: 3.3
### 条件判断：切勿直接使用 a + b == 3.3
import math
print(math.isclose(a + b, 3.3))  # True
### 要求绝对精确的场景（如金融、计费）
a = Decimal('1.1')
b = Decimal('2.2')
print(a + b)  # 输出: 3.3

# 字符串操作：Python 字符串是不可变对象，日常开发中最必须熟练掌握的内置操作主要围绕清理、拆分、拼接和判断这四大场景
## 清理与替换
### strip()：去除字符串首尾的空白字符（包括空格和换行符 \n），在处理用户输入或读取文件数据时是必不可少的步骤。
text = "1" + " hello python ".strip() + "1"
print(text)
# replace("old", "new")
print("hello python".replace("hello", "Hola"))

## 拆分与拼接
### split(sep)：按照指定的分隔符（默认是任意空白符）将字符串切分为一个列表。提取一段文本中的关键词时非常有用。
print("hello python".split(' '))
### 如果要以多个字符作为分隔符，可以先替换，再分割； 或者用正则表达式
print("hello python, I am back".replace(",", " ").split())
### 分隔符.join([a,b])
print("，".join(["hello python", "i am back"]))

## 查找与判断
### find(sub)，查找子串首先出现的位置索引，找不到返回-1
print("hello python".find("py"))
print("hello python".find("py1"))
### index(sub)，查找子串首先出现的位置索引，找不到则抛出异常
print("hello python".index("py"))
# print("hello python".index("py1"))
### startswith()和endswith(), 返回布尔值
print("hello python".startswith("hell"))
print("hello python".startswith("1hell"))

### lower(),和upper() 大小写转换
print("Hello Python".lower())
print("Hello Python".upper())

### 字符串切片 "text"[start:stop:step]
#### 基础切片
text = "hello world, i am back"
print(text[5:])  #省略 stop 时默认提取到末尾，从索引 5 一直取到最后。
print(text[:5])  #省略 start 时默认从头开始，提取前 5 个字符。
#### 负数索引截取，Python 允许从右向左倒着数，最后一个字符的索引是 -1。
print(text[-3:])
#### 步长与倒序翻转
print(text[::2])  # 省略前两个参数，将 step 设为 2，代表每隔一个字符提取一次（提取所有偶数索引的字符）
print(text[1::2])
print(text[::-1]) # 这是 Python 中最经典、最高效的字符串翻转写法。当步长设为 -1 时，引擎会从字符串的最后一位开始，从右向左依次提取全部字符，瞬间完成倒序。
print(text[50:])  # 如果指定的 start 索引完全超出了字符串最大长度，它只会默默地返回一个空字符串。
print(text[:50])  # 如果 stop 索引超出了实际长度，Python 会自动截断，将内容提取到字符串的最末尾为止。
#### 提取单个字符
print(text[1])
# print(str[50]) # IndexError

# 条件
## if-elif-else
score = 75
if score >= 80: 
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")
## 三元表达式： 结果A if 条件 else 结果B
age = 10
status = "成年" if age >= 18 else "未成年"
print(status)
## switch-case
##  1. 无需break
##  2. 条件守卫：case x if x > 10，只有变量x大于10才会进入到分支
### 匹配数字
status = 200
match status:
    case 200:
        print("请求成功")
    case 401 | 403: # 使用"|",匹配多个值
        print("权限拒绝")
    case _:     # "_"通配符，相当于default
        print("未知错误")
### 匹配字符串
command = "start1"
match command:
    case "start" | "run":
        print("start program...")
    case "stop":
        print("stop program...")
    case "restart":
        print("restart program...")
    case _:
        print("unkown command")
### 模式解构：match-case 的真正强大之处在于拆解复杂数据。它可以直接匹配并提取列表、元组、对象或字典内部的特定位置变量，而不仅仅是做简单的值相等判断。
### 等我复习到对应的知识点再练习

# 循环
## for ... in：用于按顺序提取可迭代对象（如列表、字符串、字典、集合）中的元素
text = "hello world i am back"
for s in text:
    print(s)
for word in text.split(" "):
    print(word)
## while 循环：条件驱动循环。只要指定的条件判断为真（True），循环就会持续执行。常用于未知具体执行次数、需要根据运行时状态决定何时停止的场景。
age = 1
while(age < 5):
    print(age)
    age = age + 1
### break: 立刻暴力砸碎并跳出整个所在的循环体。如果有多层嵌套循环，break 只会跳出离它最近的那一层
print("break")
age = 1
while(age < 5):
    height = 20
    while(height < 40):        
        height = height + 3
        if(height > 26 and height < 30 ):
            break
        print("age: " + str(age) + ", height: " + str(height))
    age = age + 1

### continue：
print("continue")
age = 1
while(age < 5):
    height = 20
    while(height < 40):        
        height = height + 3
        if(height > 26 and height < 30 ):
            continue
        print("age: " + str(age) + ", height: " + str(height))
    age = age + 1
### pass：占位符，啥也不干
print("pass")
age = 1
while(age < 5):
    height = 20
    while(height < 40):        
        height = height + 3
        age = age + 1
        pass

### 循环 + else 分支：这是 Python 特有的语法。无论是 for 还是 while，都可以在末尾接一个 else 块。只有当循环自然执行完毕（即没有被 break 强行中断）时，else 里的代码才会被执行。常用于搜索场景（找了一圈没找到，就执行 else）。
print("循环+else")
age = 1
while(age < 5):
    height = 20
    while(height < 40):        
        height = height + 3
        age = age + 1
        pass
else:
    print("娃娃长大了。。。")

### range(start, stop, step)：生成数字序列的利器，常与 for 结合用来控制纯数字循环的次数。
#### 四种常见参数
#### 一个参数，就是range(stop)，代表从0开始，到stop结束
for i in range(5):
    print(i)   # 输出 0, 1, 2, 3, 4
#### 两个参数：就是range(start,stop),
for i in range(3, 5):
    print(i)    # 输出3，4，
#### 三个参数：就是range(start, stop, step)
for i in range(1, 10, 2):
    print(i)    # 输出1，3，5，7，9
#### 倒序参数：就是range(start, stop, -1)
print("reverse")
for i in range(5, 1, -1):
    print(i)    # 输出5，4，3，2，

### enumerate(iterable)：当你遍历一个列表，既需要元素本身，又需要知道该元素对应的索引位置时，用它能同时优雅地提取出 (索引, 元素)。
tasks = ["write test case", "run", "submit bug"]
for index, task in enumerate(tasks, start=1):   # index默认从0开始，可以用“start=1"指定从1开始
    print( f"index-> {index}, task -> {task}")

