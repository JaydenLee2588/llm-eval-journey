# 函数的定义
# def关键字声明函数的名称和参数，return向外输出返回值
# 如果没有写return，默认返回None

# 变量作用域
#   局部变量：函数内部创建的变量，生命周期只在函数运行期间，外部无法访问
#   全局变量：函数内部可以直接读取外部的全局变量。
#           如果函数内部定义了同名的变量，不会破坏全局变量；
def count_words(raw_text):
    word_counts = {}

    # 标点与格式清洗
    clean_text = raw_text.replace(',', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ').lower()
    words = clean_text.split()
    print(words)

    # 字典词频统计
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
    print(word_counts)

    return word_counts

raw_text = """
  Hello LLM, welcome to evaluation journey! LLM evaluation is exciting, 
  and Python is great for LLM testing. 
  Is LLM evaluation reliable? Yes, evaluation is reliable and Python is powerful!
  """
count_words(raw_text)

score = 100
def update_score():
    score = 80
    print(f"inside -> {score}")
update_score()
print(f"outside score -> {score}")


## 多参数传递
### 位置参数（Position Arguments)
###     传入参数时，严格按照函数定义时的参数顺序，从左到右进行赋值

### 关键字参数（Keyword Arguments）
###     调用时明确指定“参数名=值”

### 默认参数（Default Arguments）
###     在定义函数时，直接为参数预设一个初始值。
###     如果调用函数时，没有传入该参数，则使用默认值
###     注意： 函数定义时，带有默认值的参数必须放在没有默认值参数的后面。

def calculate(a, b, operation="add"):
    if operation == "add":
        return a + b
    elif operation == "substract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    elif operation == "mod":
        return a % b
    else:
        return "Unknown Operation"

print(f"Default add -> {calculate(10, 5)}")
print(f"multiply -> {calculate(10, 5, "multiply")}")
print(f"Keyword -> {calculate(operation="divide", a=10, b=5)}")


## 不确定数量的参数： *args
##      当调用方传入数量不确定的多个参数时，python底层会自动将这些参数打包成一个元组tuple。
##      所以可以使用for .. in 循环来遍历并处理args内部所有数据
def record_scores(student, *args):
    print(f"student name: {student}")
    total = 0
    for score in args:
        total += score
    return total

print(f"Total Score: {record_scores("Alice", 90,85,80)}")


## 不确定数量的参数： **kwargs
##      在参数名前加两个*，可以允许函数接受任意数量的关键字参数。
##      **kwargs会将所有额外传入的关键字参数打包成一个字典。
##      所以可以使用items()来提取和处理这些数据
## 使用规则：
##      1. 命名约定：**是生效的核心语法，kwargs是社区通用的变量名规范
##      2. 严格顺序：如果一个函数需要同时接受多种类型的参数，定义时的顺序严格为：
##              常规参数 -> *args -> 默认参数 -> **kwargs
def generate_report(testname, **metrix):
    print(f"eval project: {testname}")
    for key,value in metrix.items():
        print(f"指标 {key} : {value}")
generate_report("RAG 检索测试", accuracy=0.95, f1_score=0.88)

# 参数顺序的示例代码
def configure_server(host, *args, port=8080, **kwargs):
    print(f"常规参数 (host): {host}")
    print(f"不定位置参数 (*args): {args}")
    print(f"默认参数 (port): {port}")
    print(f"不定关键字参数 (**kwargs): {kwargs}")
# 完整传参调用演示
configure_server("192.168.1.1", "fast_mode", "debug_on", port=9000, timeout=30, retry=3)


## 多个返回值
##      函数定义多个返回值，代码底层会打包成元组，可以使用元组解包的技巧提取。
def calculate_metrics(correct_predictions, total_samples):
    # 计算两项独立的评测指标
    accuracy = correct_predictions / total_samples
    error_rate = 1 - accuracy
    
    # 表面上返回两个值，底层引擎会自动打包为元组 (accuracy, error_rate)
    return accuracy, error_rate

# 结合元组极速解包，直接用两个独立变量接收返回值
acc, err = calculate_metrics(90, 100)

print(f"准确率: {acc}")
print(f"错误率: {err}")


## 类型注解
##      类型注解，允许在定义函数时，明确申明各个参数预期接收的数据类型，以及返回值的数据类型
##  语法：1. 参数注解：在参数名后加冒号“：”和预期数据类型
##       2. 返回值注解：在返回值后加“->”和预期数据类型
##  例子： def process(text: str) -> dict[str, int]

# 测试调用
sample_text = "apple banana apple orange banana apple"
# 由于有了注解，IDE 会知道 result 是字典，按 '.' 会自动提示 .items() 等方法
result = count_words(sample_text)
print(result) 
# 输出: {'apple': 3, 'banana': 2, 'orange': 1}

def count_words(text: str) -> dict[str, int]:
    if not text.strip():
        return {}
    words: list[str] = text.split()
    words_count: dict[str, int] = {}
    for word in words:
        words_count[word] = words_count.get(word, 0) + 1
    return words_count