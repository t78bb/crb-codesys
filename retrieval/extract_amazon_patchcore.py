#!/usr/bin/env python3
"""
从 function_level_completion_2k_context_codex.test.jsonl 中提取
所有 task_id 为 'amazon-science--patchcore-inspection/idx' 的 JSON 行，
移动到 amazon-science--patchcore-inspection.jsonl 文件
"""
import json
import os
from pathlib import Path

def main():
    # 文件路径
    input_file = "output/origin_repoeval/datasets/function_level_completion_2k_context_codex.test.jsonl"
    output_file = "output/origin_repoeval/datasets/amazon-science--patchcore-inspection.jsonl"
    
    # 目标 task_id 模式
    target_task_id = "amazon-science--patchcore-inspection/idx"
    
    print("="*80)
    print("提取 Amazon PatchCore 任务")
    print("="*80)
    print(f"\n输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print(f"目标 task_id: {target_task_id}")
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"\n错误: 输入文件不存在: {input_file}")
        return
    
    # 读取并过滤
    matched_lines = []
    remaining_lines = []
    total_count = 0
    matched_count = 0
    
    print(f"\n正在处理文件...")
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            total_count += 1
            try:
                data = json.loads(line)
                task_id = data.get('metadata', {}).get('task_id', '')
                
                if task_id == target_task_id:
                    matched_lines.append(line)
                    matched_count += 1
                else:
                    remaining_lines.append(line)
            except json.JSONDecodeError as e:
                print(f"警告: 第 {line_num} 行 JSON 解析失败: {e}")
                remaining_lines.append(line)  # 保留无法解析的行
    
    print(f"\n处理完成:")
    print(f"  总行数: {total_count}")
    print(f"  匹配的行数: {matched_count}")
    print(f"  剩余的行数: {len(remaining_lines)}")
    
    # 写入输出文件
    if matched_lines:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in matched_lines:
                f.write(line + '\n')
        print(f"\n✓ 已写入 {matched_count} 行到: {output_file}")
    else:
        print(f"\n⚠ 没有找到匹配的行，未创建输出文件")
        return
    
    # 更新原文件（删除已移动的行）
    if remaining_lines:
        backup_file = input_file + '.backup'
        print(f"\n创建备份文件: {backup_file}")
        os.rename(input_file, backup_file)
        
        with open(input_file, 'w', encoding='utf-8') as f:
            for line in remaining_lines:
                f.write(line + '\n')
        
        print(f"✓ 已更新原文件，移除了 {matched_count} 行")
        print(f"✓ 原文件已备份到: {backup_file}")
    else:
        print(f"\n⚠ 原文件中的所有行都被移除了，文件将为空")
        # 可以选择删除或保留空文件
        # os.remove(input_file)
    
    print("\n" + "="*80)
    print("完成！")
    print("="*80)

if __name__ == "__main__":
    main()

