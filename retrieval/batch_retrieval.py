#!/usr/bin/env python3
"""
批量执行 retrieval 脚本
对 my_datasets 下的每个数据集（除了 repoeval__amazon-science_patchcore-inspection_）执行 retrieval
"""
import os
import subprocess
import sys
from datetime import datetime

def remove_repoeval_prefix(dataset_name):
    """移除 repoeval 前缀，返回用于 dataset_path 的名称"""
    # 处理 repoeval_xxx 或 repoeval__xxx_ 格式
    if dataset_name.startswith("repoeval_"):
        # 移除 repoeval_ 前缀
        name = dataset_name[len("repoeval_"):]
        # 如果开头还有下划线（repoeval__xxx），去掉
        if name.startswith("_"):
            name = name[1:]
        # 如果末尾有下划线，也移除
        if name.endswith("_"):
            name = name[:-1]
        return name
    return dataset_name

def main():
    import argparse
    parser = argparse.ArgumentParser(description="批量执行 retrieval 脚本")
    parser.add_argument(
        "--result_dir",
        type=str,
        default=None,
        help="Directory name under codesys_result to save results. If not provided, will use timestamp."
    )
    args = parser.parse_args()
    
    # 如果没有提供 result_dir，生成统一的时间戳（确保所有任务使用同一个目录）
    if not args.result_dir:
        args.result_dir = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"未指定 --result_dir，使用时间戳: {args.result_dir}")
    
    base_dir = "my_datasets"
    skip_dataset = "repoeval__amazon-science_patchcore-inspection_"
    
    if not os.path.exists(base_dir):
        print(f"错误: {base_dir} 目录不存在")
        sys.exit(1)
    
    # 获取所有子目录
    all_dirs = [d for d in os.listdir(base_dir) 
                 if os.path.isdir(os.path.join(base_dir, d))]
    
    # 过滤：跳过指定的数据集
    datasets = [d for d in all_dirs if d != skip_dataset]
    datasets.sort()
    
    print("="*80)
    print("批量执行 Retrieval")
    print("="*80)
    print(f"\n结果目录: {args.result_dir}")
    print(f"跳过数据集: {skip_dataset}")
    print(f"待处理数据集数: {len(datasets)}")
    print(f"\n数据集列表:")
    for i, d in enumerate(datasets, 1):
        print(f"  {i}. {d}")
    
    # 记录结果
    results = {
        "success": [],
        "failed": [],
        "skipped": []
    }
    
    print(f"\n开始执行...")
    print("="*80)
    
    for idx, dataset_name in enumerate(datasets, 1):
        print(f"\n[{idx}/{len(datasets)}] 处理数据集: {dataset_name}")
        print("-" * 80)
        
        # 生成 dataset_path（去掉 repoeval 前缀）
        dataset_path_name = remove_repoeval_prefix(dataset_name)
        dataset_path = f"output/repoeval/{dataset_path_name}.jsonl"
        
        # 检查 dataset_path 文件是否存在
        if not os.path.exists(dataset_path):
            print(f"  ⚠ 跳过: dataset_path 文件不存在: {dataset_path}")
            results["skipped"].append({
                "dataset": dataset_name,
                "reason": f"dataset_path 文件不存在: {dataset_path}"
            })
            continue
        
        # 构建命令（始终传递 result_dir，确保所有任务使用同一个目录）
        cmd = [
            "python3",
            "eval_beir_sbert_canonical.py",
            "--dataset", dataset_name,
            "--dataset_path", dataset_path,
            "--result_dir", args.result_dir
        ]
        
        print(f"  命令: {' '.join(cmd)}")
        print(f"  dataset_path: {dataset_path}")
        
        # 执行命令
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600  # 1小时超时
            )
            
            if result.returncode == 0:
                print(f"  ✓ 成功")
                results["success"].append(dataset_name)
            else:
                print(f"  ✗ 失败 (返回码: {result.returncode})")
                error_msg = result.stderr if result.stderr else result.stdout
                results["failed"].append({
                    "dataset": dataset_name,
                    "returncode": result.returncode,
                    "error": error_msg[:500] if error_msg else "无错误信息"
                })
                print(f"  错误信息: {error_msg[:200] if error_msg else '无'}")
        
        except subprocess.TimeoutExpired:
            print(f"  ✗ 超时（超过1小时）")
            results["failed"].append({
                "dataset": dataset_name,
                "returncode": -1,
                "error": "执行超时（超过1小时）"
            })
        
        except Exception as e:
            print(f"  ✗ 异常: {str(e)}")
            results["failed"].append({
                "dataset": dataset_name,
                "returncode": -1,
                "error": str(e)
            })
    
    # 输出总结
    print("\n" + "="*80)
    print("执行总结")
    print("="*80)
    print(f"\n总数据集数: {len(datasets)}")
    print(f"成功: {len(results['success'])}")
    print(f"失败: {len(results['failed'])}")
    print(f"跳过: {len(results['skipped'])}")
    
    if results["success"]:
        print(f"\n✓ 成功的数据集 ({len(results['success'])}):")
        for d in results["success"]:
            print(f"  - {d}")
    
    if results["skipped"]:
        print(f"\n⚠ 跳过的数据集 ({len(results['skipped'])}):")
        for item in results["skipped"]:
            print(f"  - {item['dataset']}: {item['reason']}")
    
    if results["failed"]:
        print(f"\n✗ 失败的数据集 ({len(results['failed'])}):")
        for item in results["failed"]:
            print(f"\n  数据集: {item['dataset']}")
            print(f"  返回码: {item['returncode']}")
            print(f"  错误信息:")
            print(f"    {item['error']}")
            print("-" * 80)
    
    # 保存结果到文件
    import json
    result_file = f"batch_retrieval_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n详细结果已保存到: {result_file}")
    
    # 如果有失败，返回非零退出码
    if results["failed"]:
        sys.exit(1)

if __name__ == "__main__":
    main()

