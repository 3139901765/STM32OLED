from PIL import Image

def center_and_resize(input_path, output_path, target_size=(128, 64), bg_color=(255, 255, 255)):
    img = Image.open(input_path).convert("RGBA")

    # 找出非空白区域（非白或非透明）
    bbox = img.getbbox()  # getbbox会自动忽略完全透明区域，如果透明则有效

    if not bbox:
        raise ValueError("图片内容为空或全透明")

    # 裁剪出内容区域
    content = img.crop(bbox)

    # 计算缩放比例，保持等比例缩放，使内容能完整显示在目标大小内
    max_w, max_h = target_size
    w, h = content.size
    scale = min(max_w / w, max_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    # 缩放内容
    resized_content = content.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # 新建目标大小画布，填充背景色
    canvas = Image.new("RGBA", target_size, bg_color)

    # 计算粘贴位置，使内容居中
    paste_x = (max_w - new_w) // 2
    paste_y = (max_h - new_h) // 2

    # 粘贴内容到画布中央
    canvas.paste(resized_content, (paste_x, paste_y), resized_content)

    # 保存结果（如果需要单通道可以在此转换）
    canvas.save(output_path)
    print(f"处理完成，保存到 {output_path}")

# 调用示例
input_file = r"C:\Users\Duan\Desktop\小狗闭眼.bmp"
output_file = r"C:\Users\Duan\Desktop\your_image_centered.bmp"
center_and_resize(input_file, output_file)
