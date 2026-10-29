### 列表推导式（List Comprehension）是 Python 中用来快速生成和过滤列表的优雅语法
#### 结构：表达式 for 变量 in 可迭代对象 if 条件
####   表达式：你要放入新列表中的元素，或者对元素进行的操作。
####   for 循环：遍历现有的序列。
####   if 条件：（可选）用于过滤，只有满足条件的元素才会被处理并放入新列表。
tasks = ["write test case", "run", "submit bug"]
new_tasks = [task for task in tasks if task.startswith("write")]
print(new_tasks)

#### 传统写法：
new_tasks = []
for task in tasks:
    if(task.startswith("write")):
        new_tasks.append(task)
print(new_tasks)