# 完整执行流程指南

从 Retrieval 到 CodeBLEU 评估的完整指令序列。

## 方式一：使用指定的结果目录名称（推荐）

这种方式便于管理多次实验的结果，所有步骤使用相同的 `--result_dir` 参数。

### 1. Retrieval（检索）

#### 批量执行（推荐）
```bash
cd /root/code_rag_bench/code-rag-bench/retrieval
python batch_retrieval.py --result_dir my_experiment_20251125
```

#### 单个数据集执行
```bash
cd /root/code_rag_bench/code-rag-bench/retrieval
python eval_beir_sbert_canonical.py \
    --dataset repoeval_can \
    --dataset_path output/repoeval/can.jsonl \
    --result_dir my_experiment_20251125
```

**结果保存位置：** `codesys_result/my_experiment_20251125/{dataset_name}/`
- `outputs.json` - 检索评估结果
- `results.jsonl` - 检索结果（用于后续生成）

### 2. Generation（代码生成）

#### 批量执行（推荐）
```bash
cd /root/code_rag_bench/code-rag-bench/generation
python batch_generation.py --result_dir my_experiment_20251125
```

#### 单个数据集执行
```bash
cd /root/code_rag_bench/code-rag-bench/generation
python main.py \
    --tasks repoeval-function \
    --model gpt-4o \
    --dataset_path json \
    --data_files_test ../codesys_result/my_experiment_20251125/repoeval_can/results.jsonl \
    --topk_docs 5 \
    --max_length_input 2048 \
    --max_length_generation 1024 \
    --model_backend api \
    --temperature 0.2 \
    --top_p 0.95 \
    --save_generations \
    --result_dir my_experiment_20251125
```

**结果保存位置：** `codesys_result/my_experiment_20251125/{dataset_name}/`
- `generations_repoeval-function.json` - 生成的代码
- `evaluation_results.json` - 生成评估结果

### 3. CodeBLEU 评估

```bash
cd /root/code-rag-bench/codebleu/check_generation
python main.py --result_dir my_experiment_20251125
```

**结果保存位置：**
- `codesys_result/my_experiment_20251125/evaluation_summary.json` - 评估汇总
- `codebleu/evaluate_result/{timestamp}/` - 归档结果
  - `my_experiment_20251125/` - 完整的结果目录副本
  - `evaluation_summary.json` - 评估汇总文件

---

## 方式二：使用默认时间戳（自动生成）

如果不指定 `--result_dir`，系统会自动使用当前时间戳作为目录名称。

### 1. Retrieval

```bash
cd /root/code_rag_bench/code-rag-bench/retrieval
python batch_retrieval.py
# 或单个执行
python eval_beir_sbert_canonical.py \
    --dataset repoeval_can \
    --dataset_path output/repoeval/can.jsonl
```

**结果保存位置：** `codesys_result/{timestamp}/{dataset_name}/`

### 2. Generation

**注意：** 如果不指定 `--result_dir`，generation 会使用新的时间戳，导致无法找到 retrieval 的结果。
**建议：** 先查看 retrieval 生成的时间戳目录，然后使用该目录名称。

```bash
# 查看 retrieval 生成的时间戳目录
ls -lt /root/code_rag_bench/code-rag-bench/codesys_result/ | head -5

# 使用该时间戳执行 generation
cd /root/code_rag_bench/code-rag-bench/generation
python batch_generation.py --result_dir 20251125_143022
```

### 3. CodeBLEU 评估

```bash
cd /root/code-rag-bench/codebleu/check_generation
python main.py --result_dir 20251125_143022
```

---

## 完整示例：端到端执行

### 示例 1：使用指定目录名称（推荐）

```bash
# 设置实验名称
EXPERIMENT_NAME="experiment_gpt4o_20251125"

# 1. Retrieval
cd /root/code_rag_bench/code-rag-bench/retrieval
python batch_retrieval.py --result_dir $EXPERIMENT_NAME

# 2. Generation
cd /root/code_rag_bench/code-rag-bench/generation
python batch_generation.py --result_dir $EXPERIMENT_NAME

# 3. CodeBLEU 评估
cd /root/code-rag-bench/codebleu/check_generation
python main.py --result_dir $EXPERIMENT_NAME
```

### 示例 2：单个数据集完整流程

```bash
# 设置实验名称和数据集
EXPERIMENT_NAME="test_can_dataset"
DATASET_NAME="repoeval_can"
DATASET_PATH_NAME="can"

# 1. Retrieval
cd /root/code_rag_bench/code-rag-bench/retrieval
python eval_beir_sbert_canonical.py \
    --dataset $DATASET_NAME \
    --dataset_path output/repoeval/$DATASET_PATH_NAME.jsonl \
    --result_dir $EXPERIMENT_NAME

# 2. Generation
cd /root/code_rag_bench/code-rag-bench/generation
python main.py \
    --tasks repoeval-function \
    --model gpt-4o \
    --dataset_path json \
    --data_files_test ../codesys_result/$EXPERIMENT_NAME/$DATASET_NAME/results.jsonl \
    --topk_docs 5 \
    --max_length_input 2048 \
    --max_length_generation 1024 \
    --model_backend api \
    --temperature 0.2 \
    --top_p 0.95 \
    --save_generations \
    --result_dir $EXPERIMENT_NAME

# 3. CodeBLEU 评估
cd /root/code-rag-bench/codebleu/check_generation
python main.py --result_dir $EXPERIMENT_NAME
```

---

## 目录结构说明

执行完成后，目录结构如下：

```
codesys_result/
└── {result_dir}/                    # 结果目录（时间戳或指定名称）
    ├── repoeval_can/                 # 数据集1
    │   ├── outputs.json              # Retrieval 评估结果
    │   ├── results.jsonl            # Retrieval 结果（用于 Generation）
    │   ├── generations_repoeval-function.json  # 生成的代码
    │   └── evaluation_results.json   # Generation 评估结果
    ├── repoeval_elevator/            # 数据集2
    │   └── ...
    └── evaluation_summary.json       # CodeBLEU 评估汇总（由评估脚本生成）

codebleu/evaluate_result/
└── {timestamp}/                      # 归档时间戳
    ├── {result_dir}/                 # 完整的结果目录副本
    │   └── ...
    └── evaluation_summary.json       # 评估汇总文件
```

---

## 注意事项

1. **保持目录名称一致**：Retrieval、Generation 和评估必须使用相同的 `--result_dir` 参数值
2. **检查路径**：确保 `dataset_path` 和 `data_files_test` 路径正确
3. **批量处理**：使用 `batch_retrieval.py` 和 `batch_generation.py` 可以自动处理所有数据集
4. **结果归档**：CodeBLEU 评估完成后会自动归档到 `codebleu/evaluate_result/` 目录

---

## 故障排查

### 问题：Generation 找不到 retrieval 结果

**原因：** `--result_dir` 参数不一致

**解决：** 确保 Generation 使用的 `--result_dir` 与 Retrieval 相同

### 问题：评估脚本找不到数据

**原因：** 目录不存在或路径错误

**解决：** 
```bash
# 检查目录是否存在
ls -la /root/code_rag_bench/code-rag-bench/codesys_result/{result_dir}/

# 检查项目目录
ls -la /root/code_rag_bench/code-rag-bench/codesys_result/{result_dir}/repoeval_*/
```

### 问题：批量处理时某些数据集失败

**解决：** 查看批量处理脚本的输出日志，单独执行失败的数据集


