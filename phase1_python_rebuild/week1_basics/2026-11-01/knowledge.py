# 类与对象
# 类是模板，对象是示例
# 初始化方法：def __init__(self):
# self关键字：在类定义的方法内部，必须将self作为第一个参数传入，通过self.属性 来跨方法持久化和调用对象的属性

# 示例代码
class TodoList:
    # 类属性，定义在方法外部，所以实例共享
    total_task_created = 0

    def __init__(self, task_name):
        # 实例属性定义
        self.task_name = task_name
        self.task_status = False

        TodoList.total_task_created += 1
   
    def show_task(self):
        print(f"task: {self.task_name}")

todo1 = TodoList("复习字典")
todo2 = TodoList("学习类与对象章节")

todo1.show_task()
print(f"{TodoList.total_task_created}")


## 私有属性与封装
## 类属性和实例属性的私有权限
## 无论是类属性还是实例属性，只要在名字前加上两个下划线“__"，就变成了私有属性，如果外部想通过属性名来访问，就会报错AttributeError
##      必须提供公共的方法来访问这些私有属性，例如getter和setter接口方法

# 示例
class TodoList:
    __total_task = 0

    def __init__(self, task_name):
        self.__task_name = task_name
        TodoList.__total_task += 1
    
    def get_task_name(self):
        return self.__task_name
    
    def set_task_name(self, task_name):
        self.task_name = task_name
    
    def get_total_task(self):
        return TodoList.__total_task
    
    def display(self):
        print(f"task_name -> {self.task_name}")

todo1 = TodoList("study Class")
# print(f"total_task -> {todo1.__total_task}") # 报错，试图访问类的私有属性
# print(f"total_task -> {todo1.__task_name}") # 报错，试图访问实例的属性
print(f"total_task -> {todo1.get_task_name()}")
print(f"total task num -> {todo1.get_total_task()}")


## 继承
## 子类可以将父类作为模板，直接继承其所有公开属性和方法
## 子类定义方法： class SubClass(ParentClass)
### 方法重写(overloading)：子类定义了父类同名的方法，python会优先执行子类定义的代码段，从而实现多态
### 多态：python里的多态，是指不同的子类实现父类的同名的方法，而不同于java的多态。
class PriorityTodo(TodoList):
    def __init__(self, task_name, priority):
        super().__init__(task_name)
        self.priority = priority
    
    def display(self):
        print(f"priority task -> {self.get_task_name()}, priority -> {self.priority}")

class NormalTodo(TodoList):
    def __init__(self, task_name, due_date):
        super().__init__(task_name)
        self.due_date = due_date
    def display(self):
        print(f"Normal task -> {self.get_task_name()}, Due data -> {self.due_date}")

priority_todo = PriorityTodo("play music", "high")
priority_todo.display()
normal_todo = NormalTodo("gym", "11-02")
normal_todo.display()

### 魔术方法 (Dunder Methods)


### python要实现类似java的多态，方法：
###     1. 动态参数接收：直接使用带有默认值的参数，或者利用 *args 吸收位置参数、**kwargs 吸收关键字参数，让单一方法就能兼容各种不同的参数组合与数量。
###     2. 内部逻辑路由：在方法内部，结合 isinstance() 类型检查或 match-case 模式解构，根据传入参数的结构特征或长度动态路由到不同的执行分支。
###     3. 单分派装饰器：如果必须根据参数类型彻底解耦代码，Python 标准库 functools 提供了 @singledispatch 装饰器，专门用于实现基于数据类型的优雅重载。


# 模块和包
# 模块（module）：任何一个py源代码文件都是一个独立的模块，用于将不同功能的代码解耦存放
# 包（package）：将多个相关模块组织在一起的文件夹，工程开发中用于构建具备层级结构的复杂应用
# 引用方法： 通过import module或者from module_name import function_name 将外部功能引入当前文件
#   初始化文件：标准的包目录内部通常包含一个名为 __init__.py 的特殊文件（即使它是空的）。这个文件向 Python 引擎声明当前文件夹是一个可被导入的包，你也可以在其中编写包级别的初始化数据暴露逻辑。
#   __init__.py 文件的核心作用是向 Python 引擎声明当前文件夹是一个标准包，同时它也是该包被导入时第一个自动执行的文件。
##      统一访问入口：外部文件只需要执行 import todo_package，就可以直接通过 todo_package.__version__ 读取版本数据，或者使用 todo_package.TodoItem 实例化对象，调用方完全不需要关心底层代码到底拆分在了多少个不同的 .py 文件中。
##      命名空间保护 (__all__)：通过显式定义暴露白名单，可以拦截外部对包内部不稳定辅助逻辑的非法导入，维持清晰的公共 API 边界。
##      相对导入 (.)：代码中的 from .core 里的 . 代表当前 __init__.py 所在的同级目录。这确保了哪怕整个包被改名或移动到其他层级，包内部的互相引用也不会断裂。

# 示例代码
# todo_package/__init__.py


# 1. 包级别的初始化数据（全局常量、版本号、作者信息）
__version__ = "1.0.0"
__author__ = "LLM Eval Learner"
DEFAULT_PRIORITY = "正常"

# 2. 提前进行包内模块导入，缩短外部调用路径
# 假设包内有一个 core.py 文件，里面定义了 TodoItem 类
# from .core import TodoItem
# from .storage import load_tasks, save_tasks

# 3. 严格控制暴露接口 (Export Control)
# 当外部使用 `from todo_package import *` 时，只有 __all__ 列表里的对象会被允许暴露
# 这能有效隐藏包内部的辅助函数或私有逻辑
__all__ = [
    "TodoItem",
    "load_tasks",
    "save_tasks",
    "DEFAULT_PRIORITY"
]

# 初始化执行逻辑：只要外部引入了这个包，下面这行代码就会自动执行一次
print(f"[系统日志] 成功加载待办事项引擎 v{__version__}")
