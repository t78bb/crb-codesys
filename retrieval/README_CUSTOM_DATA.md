# 如何为自定义项目创建 RepoEval 测试数据

## 问题说明

运行 `repoeval_repo.py` 需要两类数据：

1. **源代码仓库** - 您已经有了 ✅
   - 位置：`codesys_project/plc_hello_mixing_tank/`
   - 内容：`.st`, `.global`, `.dut` 等源代码文件

2. **测试数据文件** - 需要创建 ❌
   - 格式：`function_level_completion_2k_context_codex.test.jsonl`
   - 内容：代码补全任务的测试用例

---

## 方案一：使用官方 RepoEval 数据集

如果您想使用标准的 RepoEval 基准测试：

```bash
cd /root/code_rag_bench/code-rag-bench/retrieval

# 方法1：运行下载脚本
chmod +x download_repoeval_data.sh
./download_repoeval_data.sh

# 方法2：手动下载
mkdir -p output/repoeval
cd output/repoeval

# 下载测试数据
wget https://github.com/microsoft/CodeT/raw/main/RepoCoder/datasets/datasets.zip
unzip datasets.zip -d datasets/

# 下载代码仓库
wget https://github.com/Veronicium/repoeval_debug/raw/main/function_level.zip
mkdir -p repositories/function_level
unzip function_level.zip -d repositories/function_level/
```

然后修改 `repoeval_repo.py` 第227行，使用官方仓库：
```python
# REPOs = REPOs_codesys  # 注释掉这行
REPOs = REPOs_function   # 使用官方的6个仓库
```

---

## 方案二：为您的自定义项目创建测试数据 ⭐

### 步骤 1：创建测试数据文件

```bash
cd /root/code_rag_bench/code-rag-bench/retrieval

# 为 plc_hello_mixing_tank 项目创建测试数据
python3 create_custom_test_data.py \
    --project_dir codesys_project/plc_hello_mixing_tank \
    --repo_name plc_hello_mixing_tank \
    --output_file output/repoeval/datasets/function_level_completion_2k_context_codex.test.jsonl \
    --extensions .st .global .dut
```

这会：
- 扫描项目中的所有 `.st`, `.global`, `.dut` 文件
- 自动生成代码补全测试任务
- 保存为 RepoEval 格式的 JSONL 文件

### 步骤 2：准备代码仓库

```bash
# 将您的项目复制到 repositories 目录
mkdir -p output/repoeval/repositories/function_level
cp -r codesys_project/plc_hello_mixing_tank \
      output/repoeval/repositories/function_level/
```

### 步骤 3：修改配置

编辑 `repoeval_repo.py`：

```python
# 第 34-36 行：取消注释
REPOs_codesys = [
    "plc_hello_mixing_tank"  # 取消注释
]
```

### 步骤 4：运行脚本

```bash
python3 ./create/repoeval_repo.py
```

---

## 测试数据文件格式说明

每行是一个 JSON 对象，包含：

```json
{
  "prompt": "// 上下文代码\nVAR\n    mode: MODES;\nEND_VAR\n",
  "metadata": {
    "task_id": "plc_hello_mixing_tank/main.st/0",
    "ground_truth": "// 需要补全的代码\nIF mode = AUTO THEN\n",
    "fpath_tuple": ["plc_hello_mixing_tank", "main.st"],
    "lineno": 42,
    "context_start_lineno": 35,
    "line_no": 42
  }
}
```

**字段说明：**
- `prompt`: 代码上下文（用于生成）
- `task_id`: 任务唯一标识符
- `ground_truth`: 正确答案
- `fpath_tuple`: 文件路径（元组形式）
- `lineno`: 目标行号
- `context_start_lineno`: 上下文起始行号

---

## 快速开始（推荐流程）

```bash
cd /root/code_rag_bench/code-rag-bench/retrieval

# 1. 创建测试数据
python3 create_custom_test_data.py \
    --project_dir codesys_project/plc_hello_mixing_tank \
    --repo_name plc_hello_mixing_tank \
    --output_file output/repoeval/datasets/function_level_completion_2k_context_codex.test.jsonl \
    --extensions .st .global .dut

# 2. 复制项目代码
mkdir -p output/repoeval/repositories/function_level
cp -r codesys_project/plc_hello_mixing_tank \
      output/repoeval/repositories/function_level/

# 3. 修改 repoeval_repo.py（取消第35行注释）
# REPOs_codesys = ["plc_hello_mixing_tank"]

# 4. 运行
python3 ./create/repoeval_repo.py
```

---

## 验证结果

成功运行后，您会得到：

```
datasets/
└── repoeval__plc_hello_mixing_tank/
    ├── queries.jsonl      # 查询（代码补全任务）
    ├── corpus.jsonl       # 语料库（代码片段）
    └── qrels/
        └── test.tsv       # 相关性标注

results/
├── repoeval-function-plc_hello_mixing_tank-2k-gt.jsonl      # 带真实答案
└── repoeval-function-plc_hello_mixing_tank-2k-infile.jsonl  # 无答案版本
```

---

## 故障排除

### 问题1：没有生成任何文件

**原因**：`REPOs_codesys` 是空列表或被注释

**解决**：取消注释 `repoeval_repo.py` 第35行

### 问题2：找不到 codex.test.jsonl

**原因**：测试数据文件不存在

**解决**：运行 `create_custom_test_data.py` 创建

### 问题3：文件格式错误

**原因**：JSONL 文件格式不正确

**解决**：检查每行是否是有效的 JSON，没有空行

---

## 参考资源

- **RepoEval 论文**: https://arxiv.org/abs/2306.03091
- **Microsoft CodeT 项目**: https://github.com/microsoft/CodeT/tree/main/RepoCoder
- **BEIR 数据格式**: https://github.com/beir-cellar/beir










