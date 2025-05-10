import os
import shutil
from datetime import datetime

# 配置文件分类规则
FILE_TYPES = {
    "Images": [".jpg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".xlsx", ".txt"],
    "Archives": [".zip", ".rar", ".7z"],
    "Code": [".py", ".js", ".html", ".css"]
}

def create_folder(path):
    """自动创建不存在的文件夹"""
    if not os.path.exists(path):
        os.makedirs(path)

def organize_files(folder_path="."):
    """主整理函数"""
    print(f"🔄 开始整理文件夹: {os.path.abspath(folder_path)}")
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # 跳过文件夹和隐藏文件
        if os.path.isdir(file_path) or filename.startswith("."):
            continue
        
        # 获取文件扩展名
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        # 确定分类
        category = "Others"
        for cat, exts in FILE_TYPES.items():
            if ext in exts:
                category = cat
                break
        
        # 创建目标文件夹
        target_folder = os.path.join(folder_path, category)
        create_folder(target_folder)
        
        # 移动文件（带时间戳防重名）
        new_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
        try:
            shutil.move(file_path, os.path.join(target_folder, new_filename))
            print(f"📦 已移动: {filename} → {category}/")
        except Exception as e:
            print(f"❌ 移动失败: {filename} - {str(e)}")

if __name__ == "__main__":
    path = input("请输入要整理的路径（直接回车使用当前目录）: ").strip()
    organize_files(path if path else os.getcwd())
    print("\n✅ 整理完成！")