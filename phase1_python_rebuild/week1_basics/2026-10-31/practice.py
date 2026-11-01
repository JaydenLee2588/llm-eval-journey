from pathlib import Path
import json

# 题目-1
print("题目-1")
current_path = Path(__file__).parent
target_file = current_path / "eval_report.txt"

with open(target_file, 'r', encoding="utf-8") as f:
    num_fail = 0
    num_block = 0
    for line in f:
        if line.strip() == "Status: FAILED":
            num_fail += 1
        if line.strip() == "Status: BLOCKED":
            num_block += 1

num_not_pass = num_fail + num_block
print(f"总计拦截异常用例数： {num_not_pass}")
print(f"Status:FAILED: {num_fail}")
print(f"Status:BLOCKED: {num_block}")

# 题目-2
print("\n题目-2")
def safe_load_config(file_name: str) -> dict:
    try:
        with open(file_name, 'r', encoding="utf-8") as f:
            json.load(f)
    except FileNotFoundError as e:
        print(f"⚠️ 警告: 配置文件 [{file_name}] 不存在，使用默认配置")
        return {"temperature": 0.7, "max_tokens": 1024, "model": "default-fallback"}
    except json.JSONDecodeError as e:
        print(f"❌ 错误: 配置文件 [{file_name}] 格式损坏，解析失败")
        return {}
    else:
        print(f"✅ 配置文件 [{file_name}] 加载成功")
    finally:
        print(f"--- 完成 [{file_name}] 加载尝试 ---")

# test case 1:
target_file_1 = current_path / "non_exist_config.json"
safe_load_config(target_file_1)

# test case 2:
target_file_1 = current_path / "benchmark_results.json"
safe_load_config(target_file_1)


# 题目-3
print("\n题目-3")
raw_response = """{
    "task_id": "eval_9527", 
    "model": "GPT-4o", 
    "status": "completed", 
    "tokens": 328, 
    "cost": 0.0026
}"""

dict_response = json.loads(raw_response)
dict_response["logged_at"] = "2026-10-31 20:00:00"
print(dict_response)

write_filename = current_path / "audit.log"
try:
    with open(write_filename, 'a', encoding="utf-8") as f:
        # json.dump(dict_response, f, ensure_ascii=False)
        f.write(json.dumps(dict_response, ensure_ascii=False)+"\n")


    with open(write_filename, 'r', encoding="utf-8") as f:
        content = f.read()
        print(f"content: {content}")
except Exception as e:
    print(f"发生异常: {e}")


# 题目-4
print("\n题目-4")
raw_scores = ["0.92", "0.88", "N/A", "0.95", None, "timeout_error", "0.78"]
# safe_transformer(raw_scores)
valid_scores = []
for score in raw_scores:
    try:        
        print(f"score: {score}")
        score = float(score)
    except (ValueError, TypeError) as e:
        print(f"跳过脏数据：{score}")
    else:
        valid_scores.append(score)
    
print(f"valid_scores: {valid_scores}\nSUM: {round(sum(valid_scores),2)}\nLEN:{len(valid_scores)}")


# 题目-5
print("\n题目-5")
base_file = current_path / "benchmark_results.json"

try: 
    with open(base_file, 'r', encoding="utf-8") as f:
        content = json.load(f)
        # print(content)
except FileNotFoundError as e:
    print("源文件未找到") 
else:    
    benchmark_name = content["benchmark_name"]
    environment = content["environment"]
    print(f"benchmark_name -> {benchmark_name}, environment -> {environment}")

    model_list = []
    for model in content["models"]:
        try:
            new_model = {}
            new_model["rank"] = ""
            new_model["model"] = model["display_name"]
            new_model["overall_score"] = model["overall_score"]
            new_model["coding_score"] = model["metrics"]["coding"]
            new_model["efficiency"] = round(model["performance"]["tokens_per_second"] / model["performance"]["avg_latency_ms"], 4)
            # print(f"new_model -> {new_model}")
            model_list.append(new_model)
        except Exception as e:
            print(f"模型数转换过程中发生异常 -> {e}")
    
    ranked_models = sorted(model_list, key=lambda x: x["overall_score"], reverse=True)
    
    rank = 1
    for model in ranked_models:
        model["rank"] = rank
        rank += 1

    new_report = {
        "report_title": "大模型综合能力榜单 (Leaderboard)",
        "source_benchmark": benchmark_name,
         "generated_date": "2026-10-31",
         "leaderboard": ranked_models
    }

    try:
        new_report_file = current_path / "leaderboard_report.json"
        with open(new_report_file, 'w', encoding="utf-8") as f:
            json.dump(new_report, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"新报告写入过程中发生异常 -> {e}")
    else:
        print("新报告写入成功")
        with open(new_report_file, 'r', encoding="utf-8") as f:
            report = f.read()
            print(f"report: -> {report}")
finally:
    print(" --- report 处理结束 ---")