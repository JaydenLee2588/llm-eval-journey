# practice-1:
raw_prompt = "  \n  User: What is the capital of France!?  \n  "
target_prompt = raw_prompt.strip().split(": ")[1].replace("!?", "?").lower()[::-1]
print(target_prompt)

# practice-2:
from math import isclose 
score_a = 0.1
score_b = 0.2
c = score_a + score_b
print(c)
print(f"{c:.2f}")
print(round(c, 2))
print(isclose(c, 0.3))
print("得分正常" if isclose(c, 0.3) else "计算异常")

# practice-3:
case_statuses = ["SUCCESS", "TIMEOUT", "FAILED", "SUCCESS", "BAD_GATEWAY"]
for index, case_status in enumerate(case_statuses, start=1):
    match case_status:
        case "SUCCESS":
            print(f"Case {index}: pass")
        case "TIMEOUT" | "FAILED":
            print(f"Case {index}: need confirm")
        case _:
            print(f"Case {index}: status TBD")

# practice-4:
latencies = [120, 30, 180, 25, 150, 90, 110]
for latency in latencies:
    if latency < 50:
        continue
    elif latency >= 500:
        print(f"⚠️ 发现严重超时 [{latency}ms]，熔断退出！")
        break
    else:
        print(f"推理完成，耗时: {latency}ms")
else:
    print("🎉 压测完成，未发生熔断")

# prictice-5:
tags = ["CRITICAL_hallucination", "WARN_slow", "CRITICAL_prompt_leak", "INFO_token_overflow", "CRITICAL_jailbreak"]
#表达式 for 变量 in 可迭代对象 if 条件
new_tags = [tag for tag in tags if tag.startswith("CRITICAL_")]
print(new_tags)
final_tags = []
for tag in new_tags:
    final_tags.append(tag[9:])
print(" | ".join(final_tags))

# Practice-5 opt-1:
final_tags_1 = [tag[9:] for tag in tags if tag.startswith("CRITICAL_")]
print(" | ".join(final_tags_1))

# Practice-5 opt-2:
final_tags_2 = [tag.removeprefix("CRITICAL_") for tag in tags if tag.startswith("CRITICAL_")]
print(" | ".join(final_tags_2))