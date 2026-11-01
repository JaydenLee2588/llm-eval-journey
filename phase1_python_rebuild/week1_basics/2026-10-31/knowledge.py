# 文件的读写
# python中，主要使用全局函数open()来读写文件，结合with上下文管理，确保文件使用完后关闭，防止内存泄漏
# 核心打开模式：
#    "r": 只读（默认模式）。如果文件不存在，报错
#    "w": 读写，如果文件不存在，则新建文件；如果文件已经有内容，会覆盖
#    "a"：追加，将新内容追加到文件尾部，不破坏原内容
# 重要操作方法：
#    f.read(): 一次性读取文件的全部内容，返回纯文本的字符串
#    f.readlines(): 按行读取文件，返回列表，文本的每一行都是列表的一个元素
#    注意，还有一个f.readline(),只读取当前的一行
#    f.write(text): 将指定的文本写入到文件中。

# 示例代码：
from pathlib import Path
current_dir = Path(__file__).parent
file_path = current_dir / "eval_report.txt"

with open(file_path, 'r', encoding="utf-8") as f:
    # content = f.read() #将文件全部内容读取到content
    # print(content)

    # lines = f.readlines()
    # for line in lines :
    #     if line.strip(): # 过滤空行
    #         print(line.strip())  #加上strip()，避免打印出每行末尾的“\n",结果多出空行。

    # 直接遍历文件，文件对象f本身就是按行迭代的，不需要调readlines()
    for line in f:
        if line.strip():
            print(line.strip())


with open(file_path, 'a', encoding="utf-8") as f:
    f.write("\n这是追加的一行内容")

with open(file_path, 'w', encoding="utf-8") as f:
    f.write("\n这是追加的一行内容")

## 注意：这里有一个工程实践的点，就是修改文件的某一行或者几行内容。
##      如果文件不大，可以先把文件全部内容读取到内存里，然后找到目标行，修改后，再写入源文件进行覆盖
##      安全的修改方案是：
##          1. 双线操作：r 打开源文件，a 打开一个新的临时文件
##          2. 逐行流转：使用 for line in f 逐行读取原文件
##          3. 边审边些：当检查到需要修改的行时，将修改后的行写到新文件中
##          4. 文件替换：临时文件写入完毕并关闭后，使用系统命令os.replace()将临时文件改名，覆盖原文件。
##      这里还有一个我之前理解错的点，就是使用“w”模式打开文件时，会执行一次覆盖操作。只要文件在with结构中没有被关闭，
##      系统就会维护一个写入游标，每次调用write()，都会在游标当前位置执行追加写入操作，而不会覆盖之前的内容。


# JSON读写
# python处理JSON数据依赖内置的json模块，核心机制是序列化和反序列化

## JSON文件的读写
###  反序列化：读取JSON。用json.load(f)方法，一步到位的将纯文本转化为结构化的数据。
###  序列化：写入JSON。用json.dump(data, f)可以将数据写入到磁盘文件。
###     在生成大模型评测报告时，通常需要配合 ensure_ascii=False（防止中文被强制转码为 Unicode 乱码）和 indent=4（增加缩进，提升人工阅读体验）这两个参数使用

## 示例代码
import json

json_path = current_dir / "benchmark_results.json" 
json_path_new = current_dir /"benchmark_results_new.json"

# 1. 安全读取json文件
with open(json_path, 'r', encoding="utf-8") as f:
    eval_data = json.load(f)

# 2. 在内存中处理json数据
eval_data["version"] = "v1.2.1"

# 3. 将处理后的数据写入新文件
with open(json_path_new, 'w', encoding="utf-8") as f:
    json.dump(eval_data, f, ensure_ascii=False, indent=2)

## JSON字符串的读写
##   在python中，处理不依赖文件的JSON字符串，主要依靠loads()和dumps()两个核心函数
##   注意，这两个函数比json文件的两个函数多了字符“s”
###    反序列化：JSON字符串转python字典
###    核心函数：json.loads(json_string)
###    主要场景：当你调用API获取网络响应时，通常是一段json的纯文本。
###        使用这个函数就可以将纯文本转换为字典，然后使用.get()或者match-case解构，从而提取数据。

###    序列化：python字段转JSON字符串
###    核心函数：json.dumps(data_dict)
###    应用场景：当你发起API请求前，必须把组装好的python字典转换成严格格式的json字符串
###    关键参数：配合ensure_ascii=False使用，保证中文字符正常显示，不会被改成unicode乱码

### 示例代码

api_response_str = '{"model": "gpt-4", "status": "success", "usage": {"tokens": 150}}'
# 将纯文本解析为 Python 字典
response_dict = json.loads(api_response_str)
print(f"提取消耗的token: {response_dict["usage"]["tokens"]}")

# 2. 准备向外发送的结构化字典数据
payload_dict = {
    "task": "RAG_Eval",
    "metrics": ["accuracy", "hallucination_rate"],
    "中文字段": "正常显示"
}

json_payload_str = json.dumps(payload_dict, ensure_ascii=False)
print(f"发送的数据： {json_payload_str}")


## 深层 JSON 数据的优雅提取 (match-case)
##   python中的macth-case语法中，最强大的特性便是模式解构（destructuring），
##     它能够在校验数据解构的同时，直接将嵌套在深层的元素按位置或键名提取为独立的变量
##   字典解构的核心机制：
##       部分匹配特性：在处理类似 JSON 的复杂字典时，字典匹配默认是部分匹配。只要指定的键值对存在即可匹配成功，字典中多余的键会被自动忽略。
##       直接穿透提取：可以直接深入提取嵌套字典内部的值，
##          避免编写层层嵌套的 if "meta" in payload and "ip" in payload["meta"]: 检查语句。
##       结合条件守卫：可以在 case 的匹配模式之后直接跟上 if 表达式（如 case x if x > 10:），
##          只有当初步匹配成功且附加条件为真时，程序才会进入该分支。

### 示例代码
user_payload = {
    "name": "Alice",
    "role": "admin",
    "status": "active",
    "meta": {"last_login": "2026-10-28", "ip": "10.0.0.5"}
}
match user_payload:
    # 校验 role 必须是 admin，同时提取 name，并深入 meta 提取 ip
    case {"role": "admin", "name": name, "meta":{"ip": ip}}:
        print(f"name-> {name}, ip -> {ip}")
    # 常规提取
    case {"name": name, "role": role}:
        print(f"name -> {name}, role -> {role}")
    case _:
        print("无效的格式")


# 异常处理 try-except
#   try-except结构是拦截运行时错误，并执行兜底逻辑的核心机制，能有效防止脚本因突发错误而彻底奔溃
#   执行逻辑：
#   1. try代码块：将读取文件、网络相应、数据类型转换等“危险操作”包裹在其中
#   2. except代码块：当try代码块报错，将进入到except代码分支。通常精准拦截特定的错误类型，
#           提供默认值，并记录日志，从而让程序安全的继续执行下去
#   3. else与finally分支：else仅在try代码块没有报错的情况下执行；
#           finally分支无论是否发生异常都会被执行，常用于关闭网络连接或者释放系统资源

# 示例代码
#读取一个json文件，处理异常
json_path = current_dir / "bench_wrong.json"
try:
    with open(json_path, 'r', encoding="utf-8") as f:
        json.load(f)
except FileNotFoundError:
    print("文件未找到。。。")
    data = {"model": "gpt-4", "status": "default"}
except json.decoder.JSONDecodeError as e:
    print(f"json配置文件格式损坏，具体原因：{e}")
    data = {}
else:
    print("成功加载并解析配置文件")
finally:
    print("--- 配置文件读取阶段结束 ---")


## python中，可以使用raise主动向外抛出异常，程序立即中断当前的逻辑，将指定的错误对象沿着调用栈向外传递，
##  直到被外层的try-except拦截。如果外层没有任何拦截，整个脚本将奔溃并打印错误堆栈
##  在except 代码块中，直接编写一个不带任何参数的孤立 raise 关键字，即可将当前刚刚拦截到的异常原封不动地向上一级调用链再次抛出
def calculate_accuracy(correct, total):
    if total <= 0:
        raise ValueError("评测总数必须大于0")
        
def calculate():
    try:
        calculate_accuracy(95, 0)
    except ValueError as e:
        print(f"已拦截错误： {e}")
        raise

try:
    calculate()
except:
    print(f"拦截到错误")