#!/usr/bin/env python3
"""
批量转换 my_datasets 下各子目录中的 qrels/test.csv 为 test.tsv 格式
"""
import os
from pathlib import Path


def convert_csv_to_tsv(csv_file_path, tsv_file_path):
    """
    将 CSV 文件转换为 TSV 文件（逗号替换为制表符）
    
    Args:
        csv_file_path: CSV 文件路径
        tsv_file_path: TSV 文件输出路径
    """
    with open(csv_file_path, 'r', encoding='utf-8') as f_in:
        content = f_in.read()
    
    # 将逗号替换为制表符
    tsv_content = content.replace(',', '\t')
    
    with open(tsv_file_path, 'w', encoding='utf-8') as f_out:
        f_out.write(tsv_content)
    
    print(f"✓ 转换成功: {csv_file_path} -> {tsv_file_path}")


def main():
    # my_datasets 目录路径
    my_datasets_dir = Path("my_datasets")
    
    if not my_datasets_dir.exists():
        print(f"错误: {my_datasets_dir} 目录不存在")
        return
    
    print(f"开始扫描 {my_datasets_dir} 目录...")
    print("=" * 60)
    
    converted_count = 0
    skipped_count = 0
    
    # 遍历 my_datasets 下的所有子目录
    for subdir in my_datasets_dir.iterdir():
        if not subdir.is_dir():
            continue
        
        # 检查是否存在 qrels/test.csv
        csv_file = subdir / "qrels" / "test.csv"
        
        if csv_file.exists():
            # 输出 TSV 文件路径
            tsv_file = subdir / "qrels" / "test.tsv"
            
            # 执行转换
            try:
                convert_csv_to_tsv(csv_file, tsv_file)
                converted_count += 1
            except Exception as e:
                print(f"✗ 转换失败 {csv_file}: {e}")
        else:
            print(f"- 跳过 {subdir.name}: 没有找到 qrels/test.csv")
            skipped_count += 1
    
    print("=" * 60)
    print(f"处理完成！")
    print(f"  成功转换: {converted_count} 个文件")
    print(f"  跳过: {skipped_count} 个目录")


if __name__ == "__main__":
    main()








