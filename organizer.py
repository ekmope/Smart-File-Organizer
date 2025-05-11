import os
import shutil
import argparse
import logging
from datetime import datetime
from typing import Dict, List

# 配置文件分类规则（支持用户自定义）
FILE_TYPES: Dict[str, List[str]] = {
    "Images": [".jpg", ".png", ".gif", ".webp", ".jpeg"],
    "Documents": [".pdf", ".docx", ".xlsx", ".txt", ".pptx", ".md"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".json"],
    "Media": [".mp4", ".mov", ".avi", ".mkv", ".mp3", ".wav"]
}

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("organizer.log"),
        logging.StreamHandler()
    ]
)

def create_folder(path: str) -> None:
    """创建文件夹并记录日志"""
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"📂 创建目录: {os.path.basename(path)}")
    except PermissionError:
        logging.error(f"❌ 没有权限创建目录: {path}")
        raise
    except OSError as e:
        logging.error(f"❌ 创建目录失败: {path} - {str(e)}")
        raise

def generate_unique_name(target_folder: str, filename: str) -> str:
    """生成带序号的不重复文件名"""
    base, ext = os.path.splitext(filename)
    counter = 1
    while True:
        new_name = f"{base}_{counter}{ext}" if counter > 1 else filename
        dest = os.path.join(target_folder, new_name)
        if not os.path.exists(dest):
            return new_name
        counter += 1

def organize_file(file_path: str, target_folder: str, dry_run: bool = False) -> None:
    """处理单个文件移动"""
    filename = os.path.basename(file_path)
    
    try:
        # 生成目标路径并处理重名
        dest_path = os.path.join(target_folder, filename)
        final_name = generate_unique_name(target_folder, filename)
        final_path = os.path.join(target_folder, final_name)
        
        action = "移动" if os.path.dirname(file_path) != target_folder else "跳过"
        
        if dry_run:
            logging.info(f"🔍 [干跑模式] {action}: {filename} → {os.path.basename(target_folder)}/")
            return
            
        if action == "移动":
            shutil.move(file_path, final_path)
            logging.info(f"📦 已{action}: {filename} → {os.path.basename(target_folder)}/")
    except Exception as e:
        logging.error(f"❌ 操作失败: {filename} - {str(e)}")

def organize_folder(folder_path: str, recursive: bool = False, dry_run: bool = False) -> None:
    """整理主函数"""
    logging.info(f"🔄 开始整理文件夹: {os.path.abspath(folder_path)}")
    
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.name.startswith('.') or entry.name == "organized":
                continue
            
            if entry.is_dir():
                if recursive:
                    organize_folder(entry.path, recursive, dry_run)
                continue
            
            file_ext = os.path.splitext(entry.name)[1].lower()
            category = next(
                (cat for cat, exts in FILE_TYPES.items() if file_ext in exts),
                "Others"
            )
            
            target_dir = os.path.join(folder_path, "organized", category)
            
            try:
                create_folder(target_dir)
                organize_file(entry.path, target_dir, dry_run)
            except Exception as e:
                logging.error(f"❌ 处理文件失败: {entry.name} - {str(e)}")
                continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="智能文件整理工具")
    parser.add_argument("path", nargs="?", default=".", help="整理路径（默认为当前目录）")
    parser.add_argument("-r", "--recursive", action="store_true", help="递归处理子目录")
    parser.add_argument("-d", "--dry-run", action="store_true", help="干跑模式（不实际移动文件）")
    parser.add_argument("-l", "--log", help="指定日志文件路径")
    args = parser.parse_args()
    
    if args.log:
        logging.getLogger().addHandler(logging.FileHandler(args.log))
    
    try:
        organize_folder(os.path.expanduser(args.path), args.recursive, args.dry_run)
        logging.info("\n✅ 整理完成！")
    except KeyboardInterrupt:
        logging.info("\n🛑 操作已取消")
    except Exception as e:
        logging.error(f"🔥 发生严重错误: {str(e)}")
        exit(1)