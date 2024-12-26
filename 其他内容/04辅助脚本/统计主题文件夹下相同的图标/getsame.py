import os
import hashlib
from PIL import Image
import pandas as pd

def calculate_image_hash(image_path):
    """计算图片的哈希值，用于判断图片内容是否相同"""
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # 确保一致的颜色模式
        resized_img = img.resize((64, 64))  # 统一大小
        hash_value = hashlib.md5(resized_img.tobytes()).hexdigest()
    return hash_value

def get_image_size(image_path):
    """获取图片的尺寸"""
    with Image.open(image_path) as img:
        return img.size

def classify_images_with_icons(input_folder, output_folder):
    """分类图片并输出结果到Excel，附带图片图标"""
    image_groups = {}  # 用于存储分类结果，键为 (hash, size)，值为文件列表

    # 遍历文件夹
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".png"):
                file_path = os.path.join(root, file)
                image_hash = calculate_image_hash(file_path)
                image_size = get_image_size(file_path)
                key = (image_hash, image_size)
                if key not in image_groups:
                    image_groups[key] = []
                image_groups[key].append(file_path)

    # 准备输出Excel
    output_file = os.path.join(output_folder, "分类结果.xlsx")
    writer = pd.ExcelWriter(output_file, engine="xlsxwriter")
    
    # 创建工作表
    workbook = writer.book
    worksheet = workbook.add_worksheet("图片分类")
    writer.sheets["图片分类"] = worksheet

    # 写入标题
    headers = ["图标", "文件名", "尺寸"]
    worksheet.write_row(0, 0, headers)

    # 写入内容
    row = 1
    for (image_hash, image_size), file_list in image_groups.items():
        # 图标插入一次即可
        icon_path = file_list[0]
        icon_cell = f"A{row + 1}"
        worksheet.insert_image(icon_cell, icon_path, {'x_scale': 0.5, 'y_scale': 0.5})
        
        for file_path in file_list:
            file_name = os.path.basename(file_path)
            worksheet.write(row, 1, file_name)  # 写入文件名
            worksheet.write(row, 2, f"{image_size[0]}x{image_size[1]}")  # 写入尺寸
            row += 1

    # 保存Excel
    writer.close()
    print(f"分类结果已保存到: {output_file}")

# 配置输入和输出路径
if __name__ == "__main__":
   # 指定输入的文件夹路径
    input_folder = "输入路径"  # 替换为实际的输入文件夹路径
    # 指定输出的文件夹路径
    output_folder = "输入路径"  # 替换为实际的输出文件夹路径

    # 检查输入文件夹和输出文件夹是否存在
    if not os.path.exists(input_folder):
        print("输入的文件夹路径不存在，请检查路径设置！")
    elif not os.path.exists(output_folder):
        print("输出的文件夹路径不存在，请检查路径设置！")
    else:
        classify_images_with_icons(input_folder, output_folder)