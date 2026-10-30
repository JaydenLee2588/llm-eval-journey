# Python 各种容器类型下 Lambda 自定义排序完全指南

> **核心思想**：无论是 `sorted(iterable, key=...)` 还是 `list.sort(key=...)`，参数 `key` 接收的都是一个函数。  
> `lambda x: ...` 的本质是：**定义一个规则，告诉 Python “把容器里的每一个元素 `x` 拿出来，提取/计算出一个特征值，然后按这个特征值比大小”**。

---

## 目录
1. [容器与排序基础规则回顾](#1-容器与排序基础规则回顾)
2. [元组列表（List of Tuples）排序](#2-元组列表list-of-tuples排序)
3. [字典（Dict）相关排序](#3-字典dict相关排序)
   - [3.1 字典列表（List of Dicts）按指定键排序](#31-字典列表list-of-dicts按指定键排序)
   - [3.2 纯字典按 Value 或 Key 排序](#32-纯字典按-value-或-key-排序)
4. [多级/多条件组合排序（Tie-breaker）](#4-多级多条件组合排序tie-breaker)
5. [字符串列表的高级排序](#5-字符串列表的高级排序)
6. [大模型评测（LLM-Eval）实战常见场景代码](#6-大模型评测llm-eval实战常见场景代码)

---

## 1. 容器与排序基础规则回顾

* **`list.sort(key=..., reverse=...)`**：
  - 只能用于**列表**；
  - **原地修改**原列表，返回 `None`。
* **`sorted(iterable, key=..., reverse=...)`**：
  - 可以用于**任何可迭代对象**（列表、元组、字典、集合等）；
  - **不修改原数据**，统一返回一个**全新的排序后列表**。
* **`reverse=True`**：降序（从大到小）；默认 `reverse=False` 为升序（从小到大）。

---

## 2. 元组列表（List of Tuples）排序

元组通常用于表示结构化的行数据（如 `(名称, 分数, 耗时)`）。

### 场景 A：按元组中指定索引位置的值排序
```python
# 数据：(学生姓名, 评测得分)
scores = [("Alice", 85), ("Bob", 92), ("Charlie", 78), ("David", 92)]

# 1. 按得分（索引 1）升序排序
sorted_by_score = sorted(scores, key=lambda item: item[1])
# 输出: [('Charlie', 78), ('Alice', 85), ('Bob', 92), ('David', 92)]

# 2. 按得分降序（从高到低）
sorted_by_score_desc = sorted(scores, key=lambda item: item[1], reverse=True)
# 输出: [('Bob', 92), ('David', 92), ('Alice', 85), ('Charlie', 78)]
```

---

## 3. 字典（Dict）相关排序

### 3.1 字典列表（List of Dicts）按指定键排序
这是 Web 开发、数据分析和大模型评测中最常见的数据结构（例如 JSON 数组）。

```python
models = [
    {"name": "GPT-4o", "score": 88.5, "cost": 0.03},
    {"name": "Claude-3.5", "score": 92.0, "cost": 0.04},
    {"name": "Llama-3", "score": 84.0, "cost": 0.01},
]

# 按 'score' 降序排序
ranked_by_score = sorted(models, key=lambda x: x["score"], reverse=True)

# 按 'cost' 升序排序（性价比优先）
cheapest_first = sorted(models, key=lambda x: x["cost"])
```

### 3.2 纯字典按 Value 或 Key 排序
字典本身是键值映射。直接对 `my_dict` 做排序默认只会排 keys。  
如果想**按值（Value）排序**，核心技巧是使用 **`.items()`** 转换为 `(key, value)` 元组后再排。

```python
# 词频统计字典
word_counts = {"python": 5, "llm": 12, "eval": 8, "agent": 3}

# 1. 按频次（Value）降序排序，得到的是元组列表
sorted_by_freq = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
print(sorted_by_freq)
# 输出: [('llm', 12), ('eval', 8), ('python', 5), ('agent', 3)]

# 2. 如果后续还需要转回字典（Python 3.7+ 字典保持插入顺序）:
sorted_dict = dict(sorted_by_freq)
print(sorted_dict)
# 输出: {'llm': 12, 'eval': 8, 'python': 5, 'agent': 3}

# 3. 按字典的 Key（字母序）升序排序:
sorted_by_key = sorted(word_counts.items(), key=lambda item: item[0])
# 输出: [('agent', 3), ('eval', 8), ('llm', 12), ('python', 5)]
```

---

## 4. 多级/多条件组合排序（Tie-breaker）

当遇到“第一条件相同，按第二条件决胜负”的场景时，**让 lambda 返回一个元组 `(第一条件, 第二条件, ...)`**，Python 会依次比较元组的每一项。

### 场景 A：主条件与次条件同方向（如同为降序或同为升序）
```python
# 评测用例：(用例名, 得分, 执行耗时ms)
cases = [
    ("case_1", 90, 120),
    ("case_2", 85, 200),
    ("case_3", 90, 80),   # 与 case_1 得分相同，但耗时更短
    ("case_4", 85, 150),
]

# 要求：优先按得分降序；得分相同时，按耗时升序（耗时越短越靠前）
# 技巧：数字前面加负号 -，可将降序转为升序逻辑！
sorted_cases = sorted(cases, key=lambda x: (-x[1], x[2]))
# 解释：
# -x[1] (得分为 90 变成 -90，比 85 的 -85 小，因此排在前面，达到降序效果)
# x[2]  (耗时 80 比 120 小，排前面，达到升序效果)

print(sorted_cases)
# 输出:
# [('case_3', 90, 80),
#  ('case_1', 90, 120),
#  ('case_4', 85, 150),
#  ('case_2', 85, 200)]
```

---

## 5. 字符串列表的高级排序

### 场景 A：忽略大小写排序
```python
names = ["alice", "Bob", "charlie", "Dave"]

# 默认按 ASCII 码排序（大写字母都在小写前面）
print(sorted(names))
# 输出: ['Bob', 'Dave', 'alice', 'charlie']

# 使用 lambda 统一转小写比对
print(sorted(names, key=lambda s: s.lower()))
# 输出: ['alice', 'Bob', 'charlie', 'Dave']
```

### 场景 B：按长度排序，长度相同时按字母序
```python
words = ["python", "go", "java", "c", "rust", "ruby"]
# 先比长度 len(w)，长度相同再比单词本身 w
sorted_words = sorted(words, key=lambda w: (len(w), w))
print(sorted_words)
# 输出: ['c', 'go', 'java', 'ruby', 'rust', 'python']
```

---

## 6. 大模型评测（LLM-Eval）实战常见场景代码

### 实战示例：综合排查“高耗时、高成本”的 Bad Cases
```python
eval_logs = [
    {"id": "q1", "passed": False, "latency_ms": 1200, "cost": 0.05},
    {"id": "q2", "passed": True,  "latency_ms": 450,  "cost": 0.01},
    {"id": "q3", "passed": False, "latency_ms": 3200, "cost": 0.08},
    {"id": "q4", "passed": False, "latency_ms": 1200, "cost": 0.09},
]

# 1. 过滤出未通过的用例
bad_cases = [item for item in eval_logs if not item["passed"]]

# 2. 排序：优先按耗时降序，耗时相同时按成本降序
bad_cases_ranked = sorted(
    bad_cases,
    key=lambda x: (x["latency_ms"], x["cost"]),
    reverse=True
)

for rank, item in enumerate(bad_cases_ranked, start=1):
    print(f"Top {rank}: 用例 {item['id']} - 耗时: {item['latency_ms']}ms, 成本: ${item['cost']}")
```

---

## 💡 记忆小抄（Cheatsheet）

| 数据结构 | 排序目标 | 推荐写法 |
| :--- | :--- | :--- |
| **元组列表** `[(a, 1), (b, 2)]` | 按第 2 个元素排序 | `sorted(lst, key=lambda x: x[1])` |
| **字典** `{a: 1, b: 2}` | 按 Value 排序 | `sorted(d.items(), key=lambda x: x[1])` |
| **字典** `{a: 1, b: 2}` | 按 Key 排序 | `sorted(d.items(), key=lambda x: x[0])` |
| **字典列表** `[{"score": 90}, ...]` | 按指定 key 排序 | `sorted(lst, key=lambda x: x["score"])` |
| **多条件排序** | 先比 A 再比 B | `sorted(lst, key=lambda x: (x.a, x.b))` |
| **数值反转排序技巧** | 升降序混搭 | `key=lambda x: (-x["score"], x["latency"])` |

