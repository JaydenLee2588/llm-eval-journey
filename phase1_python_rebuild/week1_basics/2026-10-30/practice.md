# Python 基础复习 - Day 3 练习题（函数专项）

**日期**: 2026-10-30  
**目标**: 深入掌握 Python 函数设计、多类型传参（位置/关键字/默认值/*args/**kwargs）、作用域规则、多返回值解包以及类型注解（Type Hints）。

---

## 📝 题目 1：评测准确率与置信区间计算（考察：多返回值、类型注解、默认参数）
* **背景**: 在大模型分类评测中，我们需要根据总样本数和命中样本数计算准确率，并支持可选的缩放展示。
* **要求**:
  1. 编写函数 `evaluate_accuracy(correct: int, total: int, as_percentage: bool = False) -> tuple[float, float]`:
     - 如果 `total <= 0`，返回 `(0.0, 1.0)`；
     - 计算 `accuracy = correct / total` 以及 `error_rate = 1.0 - accuracy`；
     - 若 `as_percentage=True`，则将两项指标都乘以 100（保留为数值，例如 90.0）；
     - 返回 `(accuracy, error_rate)` 元组。
  2. 调用该函数测试：
     - 测试 1（默认参数）：传入 `85, 100`，使用元组解包接收 `acc, err` 并打印；
     - 测试 2（关键字传参）：传入 `correct=45, total=50, as_percentage=True`，解包打印百分比结果。

---

## 📝 题目 2：可变评分汇总器（考察：`*args`、内置聚合函数 `sum/max/min`、防御性编程）
* **背景**: LLM-as-a-Judge（大模型裁判）对同一个回答从多轮或者多维度给出了若干个整数得分（分值 0~10 分），需要统计综合表现。
* **要求**:
  1. 编写函数 `aggregate_judge_scores(model_name: str, *scores: float) -> dict[str, float]`:
     - 如果没有传入任何分数（即 `scores` 为空），返回 `{"model": model_name, "avg": 0.0, "max": 0.0, "min": 0.0}`；
     - 否则，利用内置函数 `sum()`、`max()`、`min()` 计算出这组分数的平均分（保留 2 位小数）、最高分和最低分；
     - 返回包含上述统计结果的字典。
  2. 调用测试：
     - 测试 1：传入 `"GPT-4o", 9.5, 8.0, 9.0, 8.5`；
     - 测试 2：传入 `"Model-Blank"`（不传任何后续分数），验证边界处理。

---

## 📝 题目 3：模型推理配置与超参打包器（考察：`**kwargs`、参数优先级、字典合并）
* **背景**: 调用不同 LLM 接口时，有通用基准配置（如 `temperature=0.7`, `max_tokens=2048`），但也需要根据任务动态覆盖或传入特定厂商专有参数。
* **要求**:
  1. 编写函数 `build_model_config(model_name: str, **kwargs) -> dict`:
     - 预设一个基准默认配置字典：`base_config = {"model": model_name, "temperature": 0.7, "max_tokens": 2048}`；
     - 将额外传入的 `kwargs` 更新合并到配置中（如果传入了同名参数如 `temperature=0.2`，应覆盖默认值；如果是专有参数如 `top_p=0.9`, `frequency_penalty=0.5`，应作为新增字段保留）；
     - 返回最终的配置字典。
  2. 调用测试：
     - 调用 `build_model_config("Claude-3.5-Sonnet", temperature=0.1, top_p=0.9, stream=True)` 并打印结果，确认 `temperature` 被成功覆盖且新增了 `top_p` 与 `stream` 字段。

---

## 📝 题目 4：全参数类型混合调度器（考察：参数严格定义顺序：`常规 -> *args -> 默认参数 -> **kwargs`）
* **背景**: 评测任务的调度总入口函数，需要处理测试用例名、若干动态过滤标签、执行环境配置以及额外的元数据标签。
* **要求**:
  1. 按照 Python 标准规范的参数顺序编写函数：
     ```python
     def run_eval_pipeline(pipeline_name: str, *tags: str, env: str = "staging", **metadata):
     ```
  2. 函数逻辑：
     - 打印流水线名称 `pipeline_name`；
     - 检查 `tags`，如果传入了标签，打印 `"过滤标签: "` 并用逗号 `, ` 拼接打印标签内容；若无标签则打印 `"无过滤标签"`；
     - 打印执行环境 `env`；
     - 遍历打印 `metadata` 中的所有额外元数据（如 `dataset="GSM8K"`, `timeout=60`）。
  3. 调用测试：
     - 完整传参调用：`run_eval_pipeline("数学推理评测", "math", "zero-shot", env="production", dataset="GSM8K", batch_size=32)`。

---

## 📝 题目 5：综合实战：评测报告多维度筛选与导出器（考察：高阶实战、类型注解、作用域与闭包思维）
* **背景**: 我们有一个批量评测的结果列表，需要实现一个带过滤条件的统计导出函数。
* **输入测试数据**:
  ```python
  eval_data = [
      {"id": "case_1", "category": "coding", "score": 95, "cost": 0.02},
      {"id": "case_2", "category": "math", "score": 60, "cost": 0.01},
      {"id": "case_3", "category": "coding", "score": 85, "cost": 0.03},
      {"id": "case_4", "category": "safety", "score": 40, "cost": 0.005},
      {"id": "case_5", "category": "math", "score": 75, "cost": 0.015},
  ]
  ```
* **要求**:
  1. 编写函数 `filter_and_export_report(records: list[dict], target_category: str | None = None, min_score: int = 0) -> dict`:
     - 使用列表推导式过滤出符合条件的用例：
       - 若 `target_category` 不为 `None`，则用例的 `category` 必须等于 `target_category`；
       - 用例的 `score` 必须 `>= min_score`；
     - 计算过滤后用例的总成本 `total_cost`（保留 4 位小数）和通过率 `pass_rate`（假设 `score >= 70` 视为通过）；
     - 返回包含以下字段的汇总报告字典：
       ```python
       {
           "matched_count": 符合条件的用例数量,
           "total_cost": 总成本,
           "pass_rate": 通过率（0.0 ~ 1.0 之间）,
           "cases": 过滤后的用例 id 列表（如 ['case_1', 'case_3']）
       }
       ```
  2. 调用测试：
     - 场景 1：只筛选 `"coding"` 类别的所有用例；
     - 场景 2：筛选全部分类中（`target_category=None`），`min_score=70` 的高质量用例，并打印报告。

