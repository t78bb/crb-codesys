#!/bin/bash
# 下载官方 RepoEval 数据集

set -e

echo "=================================="
echo "下载 RepoEval 官方数据集"
echo "=================================="

OUTPUT_DIR="output/repoeval"
mkdir -p "$OUTPUT_DIR"

# 下载测试数据集
echo ""
echo "📥 下载测试数据集..."
DATASETS_URL="https://github.com/microsoft/CodeT/raw/main/RepoCoder/datasets/datasets.zip"
wget -O "$OUTPUT_DIR/datasets.zip" "$DATASETS_URL" || {
    echo "❌ 下载失败，尝试使用 curl..."
    curl -L -o "$OUTPUT_DIR/datasets.zip" "$DATASETS_URL"
}

echo "📦 解压 datasets..."
unzip -o "$OUTPUT_DIR/datasets.zip" -d "$OUTPUT_DIR/datasets/"
echo "✅ Datasets 完成"

# 下载代码仓库（function level）
echo ""
echo "📥 下载代码仓库 (function level)..."
REPOS_URL="https://github.com/Veronicium/repoeval_debug/raw/main/function_level.zip"
wget -O "$OUTPUT_DIR/function_level.zip" "$REPOS_URL" || {
    echo "❌ 下载失败，尝试使用 curl..."
    curl -L -o "$OUTPUT_DIR/function_level.zip" "$REPOS_URL"
}

echo "📦 解压 repositories..."
mkdir -p "$OUTPUT_DIR/repositories/function_level"
unzip -o "$OUTPUT_DIR/function_level.zip" -d "$OUTPUT_DIR/repositories/function_level/"
echo "✅ Repositories 完成"

# 清理
echo ""
echo "🧹 清理临时文件..."
rm -f "$OUTPUT_DIR/datasets.zip"
rm -f "$OUTPUT_DIR/function_level.zip"

echo ""
echo "=================================="
echo "✅ 下载完成！"
echo "=================================="
echo "数据位置："
echo "  - Datasets: $OUTPUT_DIR/datasets/"
echo "  - Repositories: $OUTPUT_DIR/repositories/function_level/"
echo ""










