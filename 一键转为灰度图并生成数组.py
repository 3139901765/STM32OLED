from PIL import Image
import os

# 输入输出路径
input_dir = r"D:\img\新建文件夹\新建文件夹"
mono_dir = r"D:\img\新建文件夹\新建文件夹"
os.makedirs(mono_dir, exist_ok=True)

output_file = r"D:\img\新建文件夹\新建文件夹\oled_gif_frames.c"

# 屏幕参数
WIDTH = 128
HEIGHT = 64
PAGES = HEIGHT // 8
BYTES_PER_FRAME = WIDTH * PAGES

ARRAY_NAME = "gif_frames"

# 1. 转为1-bit单色图并保存
for filename in os.listdir(input_dir):
    if not filename.lower().endswith(('.png', '.bmp')):
        continue

    img_path = os.path.join(input_dir, filename)
    out_path = os.path.join(mono_dir, os.path.splitext(filename)[0] + '.bmp')

    img = Image.open(img_path).convert("L")  # 灰度
    bw = img.point(lambda x: 0 if x < 128 else 255, '1')  # 转1-bit黑白
    bw.save(out_path, format='BMP')

    print(f"已转换: {filename} → 1-bit BMP")

# 2. 定义函数，将PIL图像转换为OLED格式的字节数组
def image_to_oled_array(img):
    img = img.convert("1")  # 1-bit 黑白
    pixels = img.load()
    data = []
    for page in range(PAGES):
        for x in range(WIDTH):
            byte = 0
            for bit in range(8):
                y = page * 8 + bit
                if pixels[x, y] == 0:  # 黑色为点亮
                    byte |= (1 << bit)
            data.append(byte)
    return data

# 3. 批量读取单色图生成C数组文件
frame_files = sorted(f for f in os.listdir(mono_dir) if f.lower().endswith((".bmp", ".png")))

with open(output_file, "w", encoding="utf-8") as f_out:
    f_out.write("// 自动生成的 OLED 动画帧数组\n\n")
    f_out.write(f"const uint8_t {ARRAY_NAME}[] = {{\n")

    total_frames = 0
    for filename in frame_files:
        filepath = os.path.join(mono_dir, filename)
        img = Image.open(filepath)
        if img.size != (WIDTH, HEIGHT):
            print(f"跳过尺寸错误帧：{filename}")
            continue
        

        data = image_to_oled_array(img)
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            line = "    " + ", ".join(f"0x{b:02X}" for b in chunk) + ",\n"
            f_out.write(line)

        total_frames += 1

    f_out.write("};\n\n")
    f_out.write(f"const uint16_t gif_frame_count = {total_frames};\n")
    f_out.write(f"const uint16_t gif_frame_size = {BYTES_PER_FRAME};\n")

print(f"\n完成！共处理帧数: {total_frames}，C数组保存到: {output_file}")
