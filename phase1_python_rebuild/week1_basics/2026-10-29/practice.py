# 题目-1
models_data = [
    {"name": "GPT-4o", "score": 88.5},
    {"name": "Claude-3.5-Sonnet", "score": 92.0},
    {"name": "Gemini-1.5-Pro", "score": 89.2},
    {"name": "Llama-3-70B", "score": 84.0}
]

ranked_models = sorted(models_data, key=lambda x: x["score"], reverse=True)
for index, value in enumerate(ranked_models, start = 1):
    print(f"Top {index}: {value["name"]} - {value["score"]}分")

# 题目-2
server_config = ("192.168.1.100", 8080, "eval_user", "v1.2", "us-west-1", "active")
ip, port, user, *rest_info = server_config
print(f"ip -> {ip}, port->{port}, user->{user}, rest_info -> {rest_info}")

single_task = ("eval_math",)
print(single_task)

eval_matrix = {}
eval_matrix[(0, 1)] = 95.0
eval_matrix[(1, 1)] = 88.5
print(f"eval_matrix[(0, 1) -> {eval_matrix[(0, 1)]}")

# 题目-3
v1_cases = ["case_01", "case_02", "case_03", "case_01", "case_04", "case_05"]
v2_cases = ["case_03", "case_04", "case_06", "case_07", "case_06"]

set_v1 = set(v1_cases)
set_v2 = set(v2_cases)
print(set_v1)
print(set_v2)
print(f"**共同测试** -> {set_v1 & set_v2}")
print(f"**v2 版本新增** -> {set_v2 - set_v1}")
print(f"**v1 版本废弃** -> {set_v1 - set_v2}")

# 题目-4
log_records = [
    ["ERROR", "RateLimitExceeded"],
    ["WARN", "LatencyHigh", "qps=150", "region=us-east"],
    ["INFO", "TaskFinished", "case_id=1024", "tokens=450", "cost=0.002"],
    ["FATAL"]
]
for log in log_records:
    match log:
        # case ["ERROR", msg] if len(log) == 2:
        case ["ERROR", msg]:
            print(f"⚠️ 错误拦截: {msg}")
        case ["WARN", issue, *details]:
            print(f"⚠️ 警告: {issue}, 详细附加信息: {details}")
        case ["INFO", *rest]:
            print(f"ℹ️ 正常信息: 包含 {len(rest)} 个字段")
        case _:
            print(f"❓ 未知日志格式")

# 题目-5
print("题目-5")
node1_errors = {"hallucination": 12, "timeout": 5, "format_error": 3}
node2_errors = {"hallucination": 8, "safety_risk": 2, "timeout": 4}

total_errors = node1_errors.copy()
print(total_errors)
for key,value in node2_errors.items():
    total_errors[key] = total_errors.get(key, 0) + value
total_errors.popitem()
print(total_errors)


# 题目-6
raw_text = """
  Hello LLM, welcome to evaluation journey! LLM evaluation is exciting, 
  and Python is great for LLM testing. 
  Is LLM evaluation reliable? Yes, evaluation is reliable and Python is powerful!
  """
print(raw_text)
# 标点与格式清洗
clean_text = raw_text.replace(',', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ').lower()
words = clean_text.split()
print(words)

# 字典词频统计
word_counts = {}
for word in words:
    word_counts[word] = word_counts.get(word, 0) + 1
print(word_counts)

# 频次排行与展示
sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
print(sorted_words)
print(sorted_words[:3])
for key, value in enumerate(sorted_words[:3], start=1):
    print(f"{key}. {value[0]}: {value[1]}次")