# RepoEval 数据集结构详解

## 📂 目录概览

```
origin_repoeval/
├── datasets/           # 测试数据（代码补全任务）
└── repositories/       # 源代码仓库
    └── function_level/ # 函数级代码仓库
```

---

## 📄 1. DATASETS 目录 - 测试数据

### 📊 内容概览

包含 **11 个 JSONL 文件**，总大小约 **70MB**，定义了不同难度级别的代码补全任务。

### 📝 文件列表

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `function_level_completion_2k_context_codex.test.jsonl` | 2.1M | 函数级补全，2k上下文 |
| `function_level_completion_4k_context_codex.test.jsonl` | 2.9M | 函数级补全，4k上下文 |
| `line_level_completion_2k_context_codex.test.jsonl` | 7.3M | 行级补全，2k上下文 |
| `line_level_completion_4k_context_codex.test.jsonl` | 11M | 行级补全，4k上下文 |
| `api_level_completion_2k_context_codex.test.jsonl` | 8.6M | API级补全，2k上下文 |
| `api_level_completion_4k_context_codex.test.jsonl` | 13M | API级补全，4k上下文 |
| `*_codegen.test.jsonl` | 多个 | CodeGen 模型变体 |

### 📈 数据统计

#### 函数级任务（Function Level）
- **总任务数**: 455 个
- **覆盖仓库**: 8 个
- **仓库分布**:
  - deepmind_tracr: 146 个任务
  - lucidrains_imagen-pytorch: 67 个任务
  - google_lightweight_mmm: 64 个任务
  - CarperAI_trlx: 46 个任务
  - maxhumber_redframes: 42 个任务
  - leopard-ai_betty: 36 个任务
  - amazon-science_patchcore-inspection: 32 个任务
  - facebookresearch_omnivore: 22 个任务

#### 行级/API级任务（Line/API Level）
- **总任务数**: 1600 个
- **覆盖仓库**: 8 个（不同于函数级）
- 每个仓库均分 200 个任务

### 📋 JSONL 文件格式

每行是一个 JSON 对象，表示一个代码补全任务：

```json
{
  "prompt": "代码上下文（用于模型输入）",
  "metadata": {
    "task_id": "CarperAI--trlx/idx",
    "ground_truth": "正确答案代码",
    "fpath_tuple": ["CarperAI_trlx", "trlx", "pipeline", "__init__.py"],
    "context_start_lineno": 0,
    "lineno": 19,
    "function_name": "register_datapipeline"
  }
}
```

### 🔍 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `prompt` | string | 代码上下文，模型需要根据此生成补全代码 |
| `task_id` | string | 任务唯一标识符，格式：`仓库名/文件路径/序号` |
| `ground_truth` | string | 正确答案，用于评估模型生成结果 |
| `fpath_tuple` | list | 文件路径（拆分为列表） |
| `context_start_lineno` | int | 上下文起始行号 |
| `lineno` | int | 目标补全的行号 |
| `function_name` | string | 函数名称（如果是函数级任务） |

### 📝 实际示例

```
Task ID: CarperAI--trlx/idx
文件: CarperAI_trlx/trlx/pipeline/__init__.py
行号: 19

Prompt (上下文):
────────────────────────────────────────
import random
import sys
from abc import abstractmethod, abstractstaticmethod
from typing import Any, Callable, Dict, Iterable

from torch.utils.data import DataLoader, Dataset

from trlx.data import GeneralElement, RLElement

_DATAPIPELINE: Dict[str, any] = {}

def register_datapipeline(name):
    """Decorator used register a CARP architecture
    Args:
        name: Name of the architecture
    """
    # 这里需要补全...
────────────────────────────────────────

Ground Truth (正确答案):
────────────────────────────────────────
    def register_class(cls, name):
        _DATAPIPELINE[name] = cls
        setattr(sys.modules[__name__], name, cls)
        return cls

    if isinstance(name, str):
        name = name.lower()
        return lambda c: register_class(c, name)

    cls = name
    name = cls.__name__
    register_class(cls, name)
────────────────────────────────────────
```

---

## 📦 2. REPOSITORIES 目录 - 源代码仓库

### 📊 内容概览

包含 **8 个真实的 Python 开源项目**，总计 **495 个 Python 文件**，用作检索的语料库。

### 🗂️ 仓库列表

| 仓库名 | Python 文件数 | 领域 | 说明 |
|--------|--------------|------|------|
| **amazon-science_patchcore-inspection** | 26 | 机器学习 | 异常检测算法 |
| **CarperAI_trlx** | 108 | 强化学习 | Transformer RL 框架 |
| **deepmind_tracr** | 56 | 机器学习 | Transformer 可解释性工具 |
| **facebookresearch_omnivore** | 65 | 计算机视觉 | 多模态视觉模型 |
| **google_lightweight_mmm** | 36 | 营销分析 | 轻量级营销混合模型 |
| **leopard-ai_betty** | 141 | 深度学习 | 多层优化框架 |
| **lucidrains_imagen-pytorch** | 14 | 生成模型 | Imagen 文本生成图像 |
| **maxhumber_redframes** | 49 | 数据分析 | Pandas 数据框架扩展 |

**总计**: 8 个仓库，495 个 Python 文件

### 📁 仓库结构示例

以 `amazon-science_patchcore-inspection` 为例：

```
amazon-science_patchcore-inspection/
├── setup.py
├── src/
│   └── patchcore/
│       ├── __init__.py
│       ├── patchcore.py       # 核心算法
│       ├── metrics.py         # 评估指标
│       ├── sampler.py         # 采样器
│       └── utils.py           # 工具函数
├── build/
│   └── lib/
└── datasets/                   # 数据集处理
```

### 💻 代码示例

```python
# 文件: amazon-science_patchcore-inspection/src/patchcore/patchcore.py
"""PatchCore and PatchCore detection methods."""
import logging
import os
import pickle

import numpy as np
import torch
import torch.nn.functional as F

class PatchCore(torch.nn.Module):
    def __init__(self, device):
        """PatchCore anomaly detection class."""
        super(PatchCore, self).__init__()
        self.device = device

    def load(
        self,
        backbone,
        layers_to_extract_from,
        device,
        input_shape,
        pretrain_embed_dimension,
        target_embed_dimension,
        patchsize=3,
        patchstride=1,
        anomaly_score_num_nn=1,
        featuresampler=patchcore.sampler.IdentitySampler(),
        nn_method=patchcore.common.FaissNN(False, 4),
        **kwargs,
    ):
        # ... 实现代码 ...
```

---

## 🔗 两者的关系

### 工作流程

```
1. 测试任务（datasets/*.jsonl）
   ↓ 定义需要补全的代码位置
   
2. 代码仓库（repositories/function_level/*）
   ↓ 提供检索的语料库
   
3. 检索系统
   ↓ 从仓库中检索相关代码
   
4. 代码生成
   ↓ 使用检索到的代码辅助生成
   
5. 评估
   ↓ 与 ground_truth 比较
```

### 匹配关系

- **测试任务的 `task_id`** 对应 **仓库名**
- **测试任务的 `fpath_tuple`** 对应 **仓库中的文件路径**
- **测试任务的 `lineno`** 对应 **文件中的具体行号**

**示例映射**:
```
Task ID: CarperAI--trlx/idx
         ↓
仓库目录: repositories/function_level/CarperAI_trlx/
         ↓
文件路径: CarperAI_trlx/trlx/pipeline/__init__.py
         ↓
行号: 19
```

---

## 🎯 使用场景

### 1. 检索增强代码生成（RAG）

从仓库中检索相关代码片段，辅助模型生成：

```
Query: [测试任务的 prompt]
    ↓ 检索
Corpus: [repositories 中的代码片段]
    ↓ 检索结果
Retrieved Docs: [Top-K 相关代码]
    ↓ 输入模型
Generated Code: [模型输出]
    ↓ 评估
Compare with: [ground_truth]
```

### 2. 代码理解评估

- 测试模型是否能理解项目上下文
- 评估在真实仓库中的代码补全能力
- 比较有/无检索的生成效果

### 3. 检索系统评估

- 评估不同检索算法（BM25, Dense, API）
- 测试检索精度（是否能找到正确的代码片段）
- 优化检索参数

---

## 📊 数据规模总结

| 项目 | 数量 | 说明 |
|------|------|------|
| **测试文件** | 11 个 | 不同难度的 JSONL 文件 |
| **测试任务** | 455 个（函数级）<br>1600 个（行/API级） | 代码补全任务 |
| **代码仓库** | 8 个 | 真实开源项目 |
| **Python 文件** | 495 个 | 检索语料库 |
| **总数据量** | ~70MB（测试）<br>+ 代码仓库 | - |

---

## 🔧 下一步操作

现在您已经有了完整的数据集，可以：

1. **运行 `repoeval_repo.py`** 构建检索数据集
2. **使用标准仓库**：注释掉 `REPOs = REPOs_codesys`
3. **或者创建自定义数据**：使用 `create_custom_test_data.py`

---

## 📚 参考资源

- **RepoEval 论文**: https://arxiv.org/abs/2306.03091
- **Microsoft CodeT**: https://github.com/microsoft/CodeT/tree/main/RepoCoder
- **数据来源**: RepoCoder 项目的测试数据集










