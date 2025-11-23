#!/usr/bin/env python3
"""
为自定义代码项目创建 RepoEval 格式的测试数据文件

使用方法：
    python3 create_custom_test_data.py --project_dir codesys_project/plc_hello_mixing_tank \
                                       --output_file output/repoeval/datasets/function_level_completion_2k_context_codex.test.jsonl \
                                       --repo_name plc_hello_mixing_tank
"""

import os
import json
import glob
import argparse
from pathlib import Path


def extract_code_snippets(file_path, repo_name, window_size=50):
    """
    从代码文件中提取代码片段作为测试任务
    
    Args:
        file_path: 代码文件路径
        repo_name: 仓库名称
        window_size: 代码窗口大小（行数）
    
    Returns:
        List[Dict]: 测试任务列表
    """
    tasks = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"⚠️  无法读取文件 {file_path}: {e}")
        return tasks
    
    if len(lines) < 10:
        return tasks
    
    # 相对路径
    rel_path = Path(file_path).relative_to(Path(file_path).parts[0])
    fpath_tuple = list(rel_path.parts)
    
    # 每隔一定行数创建一个测试任务
    step = max(5, window_size // 4)
    
    for i in range(0, len(lines), step):
        if i + 5 >= len(lines):  # 确保至少有5行
            break
        
        # 上下文：前面的代码
        context_start = max(0, i - 20)
        context_end = i
        prompt_lines = lines[context_start:context_end]
        prompt = ''.join(prompt_lines)
        
        # Ground truth：接下来的几行作为答案
        gt_end = min(len(lines), i + 5)
        ground_truth_lines = lines[i:gt_end]
        ground_truth = ''.join(ground_truth_lines)
        
        task_id = f"{repo_name}/{'/'.join(fpath_tuple)}/{len(tasks)}"
        
        task = {
            "prompt": prompt,
            "metadata": {
                "task_id": task_id,
                "ground_truth": ground_truth,
                "fpath_tuple": fpath_tuple,
                "lineno": i,
                "context_start_lineno": context_start,
                "line_no": i
            }
        }
        tasks.append(task)
    
    return tasks


def create_test_data(project_dir, repo_name, output_file, file_extensions=None):
    """
    为项目创建测试数据文件
    
    Args:
        project_dir: 项目目录
        repo_name: 仓库名称
        output_file: 输出文件路径
        file_extensions: 要处理的文件扩展名列表
    """
    if file_extensions is None:
        # 默认处理这些文件类型
        file_extensions = ['.py', '.st', '.java', '.cpp', '.c', '.js', '.ts', '.go']
    
    print(f"{'='*80}")
    print(f"📦 为项目创建测试数据")
    print(f"{'='*80}")
    print(f"项目目录: {project_dir}")
    print(f"仓库名称: {repo_name}")
    print(f"输出文件: {output_file}")
    print(f"文件类型: {', '.join(file_extensions)}")
    print()
    
    if not os.path.exists(project_dir):
        print(f"❌ 错误: 项目目录不存在 - {project_dir}")
        return
    
    # 查找所有代码文件
    all_files = []
    for ext in file_extensions:
        pattern = os.path.join(project_dir, f"**/*{ext}")
        files = glob.glob(pattern, recursive=True)
        all_files.extend(files)
    
    print(f"📂 找到 {len(all_files)} 个代码文件")
    
    # 提取测试任务
    all_tasks = []
    for file_path in all_files:
        print(f"   处理: {file_path}")
        tasks = extract_code_snippets(file_path, repo_name)
        all_tasks.extend(tasks)
        print(f"      提取了 {len(tasks)} 个任务")
    
    print(f"\n📝 总共生成 {len(all_tasks)} 个测试任务")
    
    # 保存到文件
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for task in all_tasks:
            f.write(json.dumps(task, ensure_ascii=False) + '\n')
    
    print(f"\n✅ 测试数据已保存到: {output_file}")
    
    # 显示示例
    if all_tasks:
        print(f"\n{'='*80}")
        print(f"📄 第一个任务示例:")
        print(f"{'='*80}")
        print(json.dumps(all_tasks[0], indent=2, ensure_ascii=False)[:500])
        print("...")
    
    return all_tasks


def main():
    parser = argparse.ArgumentParser(description='为自定义项目创建 RepoEval 格式的测试数据')
    parser.add_argument('--project_dir', type=str, required=True,
                       help='项目源代码目录')
    parser.add_argument('--repo_name', type=str, required=True,
                       help='仓库名称（将用于 task_id）')
    parser.add_argument('--output_file', type=str, required=True,
                       help='输出 JSONL 文件路径')
    parser.add_argument('--extensions', type=str, nargs='+',
                       default=['.py', '.st', '.java', '.cpp', '.c', '.js', '.ts'],
                       help='要处理的文件扩展名')
    
    args = parser.parse_args()
    
    create_test_data(
        project_dir=args.project_dir,
        repo_name=args.repo_name,
        output_file=args.output_file,
        file_extensions=args.extensions
    )


if __name__ == "__main__":
    main()










