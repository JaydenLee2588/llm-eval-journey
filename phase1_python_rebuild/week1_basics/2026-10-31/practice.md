# Python 基础复习 - Day 4 练习题（文件 I/O、JSON 与异常处理）

**日期**: 2026-10-31  
**目标**: 深入掌握标准文件读写（`with open`、逐行流式处理）、`json.load/dump/loads/dumps` 序列化与反序列化、防御性异常捕获（`try-except-else-finally`），并完成端到端“读 JSON -> 处理 -> 写新 JSON”的评测实战。

---

## 📝 题目 1：评测日志纯文本解析与筛选（考察：`with open` 逐行流式读取、`strip`、字符串提取）
* **背景**: 同级目录下有一份大模型评测文本报告 `eval_report.txt`，需要从中提取出所有失败（FAILED）或被安全拦截（BLOCKED）的用例信息。
* **要求**:
  1. 使用 `Path(__file__).parent / "eval_report.txt"` 定位文件，以只读模式（`"r"`）打开；
  2. 使用 `for line in f:` 逐行流式读取文件（注意使用 `strip()` 移除多余换行符）；
  3. 提取并统计文件中所有状态为 `Status: FAILED` 或 `Status: BLOCKED` 的用例行；
  4. 打印格式要求：
     ```text
     总计拦截异常用例数: 2
     - Status: FAILED
     - Status: BLOCKED
     ```

---

## 📝 题目 2：防御性安全加载 JSON 配置文件（考察：`FileNotFoundError`、`json.JSONDecodeError`、`else-finally`）
* **背景**: 评测脚本通常需要在启动时加载模型超参配置，如果配置文件丢失或格式被破坏，需要优雅降级为默认配置，绝不能让整个流水线崩掉。
* **要求**:
  1. 编写函数 `safe_load_config(file_name: str) -> dict`:
     - 尝试使用 `json.load()` 读取指定文件；
     - 若捕获到 `FileNotFoundError`：打印 `"⚠️ 警告: 配置文件 [{file_name}] 不存在，使用默认配置"`，并返回默认配置字典 `{"temperature": 0.7, "max_tokens": 1024, "model": "default-fallback"}`；
     - 若捕获到 `json.JSONDecodeError`：打印 `"❌ 错误: 配置文件 [{file_name}] 格式损坏，解析失败"`，并返回空字典 `{}`；
     - 若读取成功无异常（利用 `else` 分支）：打印 `"✅ 配置文件 [{file_name}] 加载成功"` 并返回解析后的字典；
     - 无论是否出错（利用 `finally` 分支）：打印 `"--- 完成 [{file_name}] 加载尝试 ---"`。
  2. 调用测试：
     - 测试 1：传入一个不存在的文件名 `"non_exist_config.json"`，观察默认值返回与日志；
     - 测试 2：传入正常存在的 `"benchmark_results.json"`，观察正常加载日志。

---

## 📝 题目 3：API 响应字符串快速序列化与追加日志（考察：`json.loads()`、`json.dumps()`、文件追加模式 `"a"`）
* **背景**: 在大模型 API 评测过程中，服务端返回的是 JSON 格式的字符串。我们需要解析它，提取字段，并将格式化后的审计日志追加到磁盘日志文件 `audit.log` 中。
* **输入模拟数据**:
  ```python
  raw_response = '{"task_id": "eval_9527", "model": "GPT-4o", "status": "completed", "tokens": 328, "cost": 0.0026}'
  ```
* **要求**:
  1. 使用 `json.loads()` 将 `raw_response` 字符串解析为 Python 字典；
  2. 在字典中动态新增一个审计时间戳字段 `"logged_at": "2026-10-31 20:00:00"`；
  3. 以追加模式（`"a"`，`encoding="utf-8"`）打开 `audit.log` 文件；
  4. 使用 `json.dumps(..., ensure_ascii=False)` 将该字典序列化为单行 JSON 字符串，写入文件末尾并补上换行符 `\n`；
  5. 再次读取该文件内容并打印，验证追加成功。

---

## 📝 题目 4：数值型评测指标安全转换与异常捕获（考察：`try-except` 捕获 `ValueError` / `TypeError`）
* **背景**: 从外部 CSV/文本日志中读取的指标可能包含脏数据（如 `"0.95"`, `"N/A"`, `None`, `"ERROR_TIMEOUT"`）。
* **输入测试数据**:
  ```python
  raw_scores = ["0.92", "0.88", "N/A", "0.95", None, "timeout_error", "0.78"]
  ```
* **要求**:
  1. 遍历 `raw_scores` 列表，编写一个安全的数值转换逻辑；
  2. 使用 `try-except` 包裹类型转换代码 `float(score)`：
     - 如果能成功转换为浮点数，将其保留 2 位小数并存入 `valid_scores` 列表；
     - 如果遇到 `ValueError` 或 `TypeError`（使用元组 `(ValueError, TypeError)` 一并捕获）：打印 `"跳过脏数据: {score}"`；
  3. 最终打印 `valid_scores` 列表，并用 `sum()` 和 `len()` 计算出这些有效分数的平均值。

---

## 🌟 题目 5（核心大题）：读评测 JSON -> 计算增强指标 -> 写入新 JSON（端到端实战）
* **考察综合能力**: `json.load`、深层字典与列表访问、数据转换与计算、`sorted` 排序、`json.dump`（带缩进和编码）
* **背景**: 评测系统输出了一份原始基准评测文件 `benchmark_results.json`，管理层需要一份更精简的“排行榜报告”，要求计算出性价比得分并按综合分由高到低排序，写出到新文件 `leaderboard_report.json` 中。
* **业务要求与处理流程**:
  1. **读取原始 JSON**：
     - 读取同级目录下的 `benchmark_results.json` 文件内容。
  2. **在内存中转换与指标增强**：
     - 从顶层提取出 `benchmark_name` 与 `environment` 字典；
     - 遍历 `models` 列表，为每个模型提取并重构一个精简字典：
       - `rank`: 初始占位（排序后生成）
       - `model`: 模型的 `display_name`
       - `overall_score`: 综合得分
       - `coding_score`: 从子层级 `metrics.coding` 提取
       - `efficiency`: 根据 `tokens_per_second / avg_latency_ms` 计算推理效率指数（保留 4 位小数）
     - 将重构后的模型列表按照 `overall_score` 从高到低进行**降序排序**；
     - 根据排序结果，为每个模型的 `rank` 字段赋值为 1, 2, 3...
  3. **组装新字典结构**:
     ```python
     new_report = {
         "report_title": "大模型综合能力榜单 (Leaderboard)",
         "source_benchmark": 提取出的原始基准名称,
         "generated_date": "2026-10-31",
         "leaderboard": 排序并带上了 rank 的模型列表
     }
     ```
  4. **写入目标文件**:
     - 将组装好的 `new_report` 字典写入到同级目录下的 `leaderboard_report.json` 文件；
     - **必须**使用 `ensure_ascii=False`（确保中文正常显示不乱码）和 `indent=2`（保持优美的缩进排版）。
  5. 打印一条成功提示，并重新读取 `leaderboard_report.json` 打印前 15 行或全文进行验证。

