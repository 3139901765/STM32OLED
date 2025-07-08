from PIL import Image, ImageDraw, ImageFont
import textwrap

# 固定画布为 128x64，文字居上绘制，剩下填充为黑
def render_full_screen_chinese(text, font_path, font_size=16, max_chars_per_line=8):
    width, height = 128, 64  # OLED 固定分辨率
    lines = textwrap.wrap(text, max_chars_per_line)
    max_lines = height // font_size  # 屏幕最多容纳的行数

    img = Image.new("1", (width, height), 0)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)

    for i, line in enumerate(lines[:max_lines]):
        draw.text((0, i * font_size), line, font=font, fill=1)

    return img

# 转换图像为 C 数组（垂直分页）
def convert_image_to_c_array(image):
    width, height = image.size
    pages = height // 8
    data = []

    for page in range(pages):
        for x in range(width):
            byte = 0
            for bit in range(8):
                y = page * 8 + bit
                if y >= height:
                    continue
                pixel = image.getpixel((x, y))
                if pixel:
                    byte |= (1 << bit)
            data.append(byte)

    return data, width, height

# 生成 C 代码
def generate_c_code(text, font_path, font_size=16, max_chars_per_line=8):
    img = render_full_screen_chinese(text, font_path, font_size, max_chars_per_line)
    data, width, height = convert_image_to_c_array(img)

    c_array = f"const uint8_t chinese_bmp[] = {{\n"
    for i, byte in enumerate(data):
        if i % 16 == 0:
            c_array += "    "
        c_array += f"0x{byte:02X}, "
        if (i + 1) % 16 == 0:
            c_array += "\n"
    if len(data) % 16 != 0:
        c_array += "\n"
    c_array += f"}};\n\n"
    c_array += f"// Width: {width}, Height: {height}\n"

    return c_array

# 示例用法
if __name__ == "__main__":
    text = "赵佳妮聪明蛋。"
    font_path = "msyh.ttc"  # 微软雅黑字体路径
    c_code = generate_c_code(text, font_path, font_size=16, max_chars_per_line=8)

    print(c_code)
