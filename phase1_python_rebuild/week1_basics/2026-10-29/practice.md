# Python 基础复习 - Day 2 练习题

**日期**: 2026-10-29  
**目标**: 深入掌握 Python 四大核心容器类型（List、Dict、Set、Tuple）、自定义排序、模式解构及文本清洗统计实战。

---

## 📝 题目 1：评测模型得分排行（考察：`sorted()`、`lambda` 自定义排序）
* **背景**: 评测任务中，多个基座模型完成了相同的测试集，需要按照平均分进行降序排名，并输出格式化榜单。
* **输入**:
  ```python
  models_data = [
      {"name": "GPT-4o", "score": 88.5},
      {"name": "Claude-3.5-Sonnet", "score": 92.0},
      {"name": "Gemini-1.5-Pro", "score": 89.2},
      {"name": "Llama-3-70B", "score": 84.0}
  ]
  ```
* **要求**:
  1. 使用内置全局函数 `sorted()`，通过 `key=lambda ...` 与 `reverse=True`，按照 `score` 从高到低排序，生成新列表 `ranked_models`（不能修改原列表）；
  2. 使用 `enumerate(ranked_models, start=1)` 遍历，格式化打印排行榜：
     ```text
     Top 1: Claude-3.5-Sonnet - 92.0分
     Top 2: Gemini-1.5-Pro - 89.2分
     ...
     ```

---

## 📝 题目 2：元组解包与配置校验（考察：元组单元素陷阱、解构 `*rest`、字典多维键）
* **背景**: 评测框架需要读取评测环境配置，并将每个用例在坐标点（`x, y`）上的测试结果存入字典。
* **输入**:
  ```python
  server_config = ("192.168.1.100", 8080, "eval_user", "v1.2", "us-west-1", "active")
  ```
* **要求**:
  1. 使用元组解包语法，提取出 `ip`、`port`、`user`，并将剩余的所有参数打包给 `rest_info` 列表打印出来；
  2. 创建一个只包含单个元素的元组 `single_task`，元素为 `"eval_math"`（注意单元素元组的逗号语法），打印其类型确保为 `tuple`；
  3. 创建一个以二维坐标元组 `(x, y)` 为键、评测得分（float）为值的字典 `eval_matrix`，存入两个坐标 `(0, 1): 95.0` 和 `(1, 1): 88.5`，并通过键读取并打印原点右侧 `(0, 1)` 的得分。

---

## 📝 题目 3：评测用例集差集与去重对比（考察：集合操作、去重、交集 `&`、差集 `-`）
* **背景**: 模型升级前后分别跑了两次用例集，需要快速比对用例的覆盖情况。
* **输入**:
  ```python
  v1_cases = ["case_01", "case_02", "case_03", "case_01", "case_04", "case_05"]
  v2_cases = ["case_03", "case_04", "case_06", "case_07", "case_06"]
  ```
* **要求**:
  1. 分别将 `v1_cases` 与 `v2_cases` 转换为集合 `set_v1` 和 `set_v2`，完成自动去重；
  2. 计算并打印两个版本**共同测试**的用例集合（交集）；
  3. 计算并打印 **v2 版本新增**的用例集合（即属于 v2 但不属于 v1 的差集）；
  4. 计算并打印 **v1 版本废弃**的用例集合（即属于 v1 但不属于 v2 的差集）。

---

## 📝 题目 4：评测日志模式解构分流（考察：`match-case` 列表模式解构、通配符 `*`）
* **背景**: 评测监控器会实时捕获各种结构的日志数据，需要快速提取结构化字段。
* **输入**:
  ```python
  log_records = [
      ["ERROR", "RateLimitExceeded"],
      ["WARN", "LatencyHigh", "qps=150", "region=us-east"],
      ["INFO", "TaskFinished", "case_id=1024", "tokens=450", "cost=0.002"],
      ["FATAL"]
  ]
  ```
* **要求**:
  遍历 `log_records`，对每条记录使用 `match-case` 模式解构分流：
  1. 如果是长度恰好为 2 的 `["ERROR", msg]`：打印 `⚠️ 错误拦截: {msg}`；
  2. 如果是 `["WARN", issue, *details]`：提取 `issue`，并将剩余详细信息 `details` 打包成列表打印：`⚠️ 警告: {issue}, 详细附加信息: {details}`；
  3. 如果是 `["INFO", *rest]`：打印 `ℹ️ 正常信息: 包含 {len(rest)} 个字段`；
  4. 其他任何未知格式：打印 `❓ 未知日志格式`。

---

## 📝 题目 5：字典安全存取与统计合并（考察：`get(key, default)`、`popitem()`、字典推导/遍历）
* **背景**: 从两个不同的评测节点汇聚了各个错误类型的计数。
* **输入**:
  ```python
  node1_errors = {"hallucination": 12, "timeout": 5, "format_error": 3}
  node2_errors = {"hallucination": 8, "safety_risk": 2, "timeout": 4}
  ```
* **要求**:
  1. 创建一个新字典 `total_errors = node1_errors.copy()`；
  2. 遍历 `node2_errors.items()`，使用 `total_errors.get(k, 0)` 将 `node2` 的数值累加合并到 `total_errors` 中；
  3. 调用字典的 `popitem()` 方法弹出最后一项错误统计，分别打印弹出的键与值；
  4. 最终打印完整的合并字典 `total_errors`。

---

## 🌟 今日核心大题：评测文本标点清洗与词频统计（Word Frequency Counter）

* **考察综合能力**: 字符串清洗替换（多标点处理）、`lower()`、`split()`、字典计数累加（或 `dict.get()`）、`sorted(..., key=lambda ...)` 降序排序。
* **背景**: 在大模型评测（尤其是开放式问答、摘要评测、困惑度分析）中，文本预处理是非常关键的一步。测试集或模型吐出的大段文字通常包含各种逗号、句号、感叹号、换行符等混合标点，需要清洗后统计词频分布。
* **输入文本**:
  ```python
  raw_text = """
  Hello LLM, welcome to evaluation journey! LLM evaluation is exciting, 
  and Python is great for LLM testing. 
  Is LLM evaluation reliable? Yes, evaluation is reliable and Python is powerful!
  """
  ```
* **要求**:
  1. **标点与格式清洗**：
     - 去除文本中的常见标点符号：`逗号 (,)`、`句号 (.)`、`感叹号 (!)`、`问号 (?)`（可以使用链式 `replace`，或者遍历标点字符替换为空格）；
     - 将所有文本全部转换为小写，确保统计词频时不区分大小写（例如 `LLM` 和 `llm` 视作同一个词）；
     - 使用 `split()` 将清洗后的纯文本拆分为单词列表 `words`。
  2. **字典词频统计**：
     - 创建一个空字典 `word_counts = {}`；
     - 遍历 `words` 列表，使用 `word_counts.get(word, 0) + 1` 统计每个单词出现的次数。
  3. **频次排行与展示**：
     - 将统计好的字典，按照**出现频次由高到低**进行降序排序；
     - 打印输出出现频率最高的前 3 个单词及其次数（例如格式：`1. llm: 4次`）。

