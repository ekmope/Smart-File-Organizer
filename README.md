# Smart File Organizer 🗂️

## 新增功能 ✨
- 🎯 智能冲突解决（序号替代时间戳）
- 📁 独立整理目录保障安全
- 🔍 递归处理嵌套文件夹
- 📝 详尽的日志记录系统
- 🚦 干跑模式预览整理效果

## 使用说明
```bash
# 基本用法
python organizer.py [路径]

# 常用选项
-r, --recursive   递归处理子目录
-d, --dry-run     干跑模式（不实际移动文件）
-l, --log         指定日志文件路径

# 示例
python organizer.py ~/Downloads -r
python organizer.py ./test_files -d --log output.log