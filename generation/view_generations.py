#!/usr/bin/env python3
"""
查看代码生成结果的脚本
"""
import json
import re
import sys

def extract_code(text: str, pattern: str = r"```(\w*)\n(.*?)\n```"):
    """从文本中提取代码块"""
    match = re.findall(pattern, text, flags=re.DOTALL)
    return match[0][1] if match else text

def main():
    # 读取生成文件
    with open('generations_repoeval-function.json', 'r') as f:
        data = json.load(f)
    
    print("="*80)
    print("代码生成结果查看器")
    print("="*80)
    print(f"\n生成文件包含 {len(data)} 个样本")
    print(f"每个样本有 {len(data[0])} 个候选生成结果\n")
    
    for idx, sample in enumerate(data):
        print("="*80)
        print(f"样本 {idx + 1}")
        print("="*80)
        
        for cand_idx, generation in enumerate(sample):
            print(f"\n--- 候选生成 {cand_idx + 1} ---\n")
            
            # 显示完整生成内容
            print("【完整生成内容】")
            print("-" * 80)
            print(generation)
            print("-" * 80)
            print(f"长度: {len(generation)} 字符\n")
            
            # 提取代码部分
            extracted = extract_code(generation)
            print("【提取的代码部分】")
            print("-" * 80)
            print(extracted)
            print("-" * 80)
            print(f"长度: {len(extracted)} 字符\n")
            
            # 检查是否包含代码块
            has_code_block = bool(re.search(r"```(\w*)\n(.*?)\n```", generation, re.DOTALL))
            print(f"包含代码块: {'是' if has_code_block else '否'}")
            
            if not has_code_block:
                print("⚠️  警告: 生成内容中没有找到代码块，将使用整个文本作为代码")

if __name__ == "__main__":
    main()


