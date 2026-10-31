# 题目-1
def evaluate_accuracy(correct: int, total: int, as_percentage: bool = False) -> tuple[float, float]:
    if total <= 0:
        return (0.0, 1.0)
    
    accuracy = correct / total
    error_rate = round(1.0 - accuracy, 2)
    if as_percentage:
        accuracy = accuracy * 100
        error_rate = round(error_rate * 100, 2)

    return (accuracy, error_rate)

# test case 1
acc, err = evaluate_accuracy(85, 100)
print(f"acc->{acc}, err -> {err}") 
# test case 2
acc, err = evaluate_accuracy(correct=45, total=50, as_percentage=True)
print(f"acc->{acc}, err -> {err}") 



# 题目-2
def aggregate_judge_scores(model_name: str, *scores: float) -> dict[str, float]:
    result = {"model": model_name, "avg":0.0, "max":0.0, "min":0.0}
    if len(scores) == 0:
        print("no scores")
        return result
    
    result["avg"] = sum(scores) / len(scores)
    result["max"] = max(scores)
    result["min"] = min(scores)
    return result

# test case 1
print(aggregate_judge_scores("GPT-4o", 9.5, 8.0, 9.0, 8.5))

# test case 2
print(f"{aggregate_judge_scores("model_no_score")}")


# 题目-3
def build_model_config(model_name: str, **kwargs) -> dict:
    base_config = {
        "model": model_name,
        "temperature": 0.7,
        "max_tokens": 2048
    }

    # for key,value in kwargs.items():
    #     base_config[key] = value
    base_config.update(kwargs) # 简化的写法

    return base_config
    
# test case
result = build_model_config("Claude-3.5-Sonnet", temperature=0.1, top_p=0.9, stream=True)
print(result)


# 题目-4
def run_eval_pipeline(pipeline_name: str, *tags: str, env: str = "staging", **metadata):
    print(f"pipeline_name -> {pipeline_name}")

    if len(tags) > 0:
        print(f"过滤标签： {','.join(tags)}")
    else:
        print("无过滤标签")
    
    print(f"执行环境： {env}")

    print("遍历metadata：")
    for key,value in metadata.items():
        print(f"key -> {key}, value -> {value}")
    
# test case
run_eval_pipeline("数学推理评测", "math", "zero-shot", env="production", dataset="GSM8K", batch_size=32)


# 题目-5
print("题目-5")
eval_data = [
    {"id": "case_1", "category": "coding", "score": 95, "cost": 0.02},
    {"id": "case_2", "category": "math", "score": 60, "cost": 0.01},
    {"id": "case_3", "category": "coding", "score": 85, "cost": 0.03},
    {"id": "case_4", "category": "safety", "score": 40, "cost": 0.005},
    {"id": "case_5", "category": "math", "score": 75, "cost": 0.015},
]

def filter_and_export_report(records: list[dict], target_category: str | None = None, min_score: int = 0) -> dict:
    result = {
        "matched_count": 0, 
        "total_cost": 0, 
        "pass_rate": 0.0,
        "cases": [] 
    }
            
    new_records = [
        record for record in records 
        if (target_category is None or target_category == record["category"]) 
        and record["score"] >= min_score
    ]
    
    print(f"new_record: {new_records}")
    total_cost = 0.0
    pass_num = 0
    cases = []
    pass_rate = 0.0
    for record in new_records:
        total_cost += record["cost"]
        cases.append(record["id"])
        if record["score"] >= 70:
            pass_num += 1
    if len(new_records) > 0:
        pass_rate = pass_num / len(new_records)
    

    return {
        "matched_count": len(new_records), 
        "total_cost": total_cost, 
        "pass_rate" : pass_rate, 
        "cases": cases
    }

# test case 1
result_1 = filter_and_export_report(eval_data, "coding")
print(f"result_1: {result_1}")

# test case 2
result_2 = filter_and_export_report(eval_data, min_score=70)
print(f"result_2: {result_2}")