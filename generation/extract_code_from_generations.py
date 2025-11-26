#!/usr/bin/env python3
"""
从 generations_repoeval-function.json 中提取代码块
"""
import json
import re
import sys

CODE_BLOCK_PATTERN = r"```(\w*)\n(.*?)\n```"

def extract_code(text: str, pattern: str = CODE_BLOCK_PATTERN):
    """从文本中提取代码块"""
    if not text or not text.strip():
        return ""
    
    match = re.findall(pattern, text, flags=re.DOTALL)
    if match:
        # 返回第一个代码块的内容
        return match[0][1].strip()
    else:
        # 如果没有代码块，返回原始文本（可能是纯代码）
        return text.strip()

def main():
    input_file = "generations_repoeval-function.json"
    output_file = "generations_repoeval-function_extracted.json"
    
    print(f"读取文件: {input_file}")
    with open(input_file, 'r') as f:
        generations = json.load(f)
    
    print(f"总任务数: {len(generations)}")
    
    # 提取代码
    extracted_generations = []
    stats = {
        "total": len(generations),
        "has_code_block": 0,
        "no_code_block": 0,
        "empty": 0
    }
    
    for i, gen_list in enumerate(generations):
        if not gen_list or len(gen_list) == 0:
            extracted_generations.append([""])
            stats["empty"] += 1
            continue
        
        extracted_list = []
        for gen in gen_list:
            extracted = extract_code(gen)
            extracted_list.append(extracted)
            
            if "```" in gen:
                stats["has_code_block"] += 1
            elif not extracted:
                stats["no_code_block"] += 1
        
        extracted_generations.append(extracted_list)
    
    # 保存提取后的代码
    print(f"\n保存到: {output_file}")
    with open(output_file, 'w') as f:
        json.dump(extracted_generations, f, indent=2)
    
    # 打印统计信息
    print("\n统计信息:")
    print(f"  总任务数: {stats['total']}")
    print(f"  包含代码块: {stats['has_code_block']}")
    print(f"  无代码块（可能是纯代码）: {stats['no_code_block']}")
    print(f"  空结果: {stats['empty']}")
    
    # 显示几个示例
    print("\n前3个提取结果示例:")
    for i in range(min(3, len(extracted_generations))):
        print(f"\n任务 {i+1}:")
        extracted = extracted_generations[i][0] if extracted_generations[i] else ""
        if extracted:
            print(f"  长度: {len(extracted)} 字符")
            print(f"  前200字符:\n{extracted[:200]}...")
        else:
            print("  (空)")

if __name__ == "__main__":
    main()

