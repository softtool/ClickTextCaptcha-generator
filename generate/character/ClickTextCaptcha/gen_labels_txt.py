import os


def write_labels_txt(image_dir, output_file):
    """
    遍历指定目录及其子目录下的所有图片文件，并将图片路径和对应的标签数据写入 labels.txt 文件。

    :param image_dir: 图片文件所在的根目录
    :param output_file: 输出 labels.txt 文件的路径
    """
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(image_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    # 获取相对路径（相对于 image_dir）
                    relative_path = os.path.relpath(root, image_dir)
                    # 构建最终的文件名格式：folder_name/filename 或 filename
                    if relative_path == '.':
                        file_prefix = file  # 根目录下直接使用文件名
                    else:
                        file_prefix = os.path.join(relative_path, file)  # 子目录则加上路径前缀

                    label = file.split('_')[0]  # 取下划线分割的第一部分作为 label
                    full_line = f"{file_prefix}\t{label}\n"  # 拼接完整行

                    f.write(full_line)  # 写入一行到 labels.txt


if __name__ == "__main__":
    # 定义图片目录和输出文件路径
    #image_directory = os.path.abspath(os.path.join(__file__, '..', '..', '..', '..', 'images', 'character', 'ImageCaptcha'))

    #labels_output = os.path.join(image_directory, 'labels.txt')

    image_directory =r"C:\bigmodel\dddd\dddd_trainer\images_set\images"
    labels_output =r"C:\bigmodel\dddd\dddd_trainer\images_set\labels.txt"
    # 调用函数生成 labels.txt
    write_labels_txt(image_directory, labels_output)
    print(f"Labels written to {labels_output}")
