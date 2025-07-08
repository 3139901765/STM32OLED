from PIL import Image
import os

def convert_to_128x64_bw_bmp(input_path):
    img = Image.open(input_path)
    img = img.resize((128, 64), Image.Resampling.LANCZOS)
    img = img.convert('L')
    img = img.point(lambda x: 0 if x < 128 else 255, '1')

    base, _ = os.path.splitext(input_path)
    output_path = base + '_128x64.bmp'
    img.save(output_path, format='BMP')
    print(f"转换完成，保存到：{output_path}")
    return output_path

def bmp_to_oled_array(bmp_path):
    im = Image.open(bmp_path).convert('1')
    width, height = im.size

    if height % 8 != 0:
        raise ValueError("Height must be multiple of 8")

    oled_bytes = []
    for page in range(height // 8):
        for x in range(width):
            byte = 0
            for bit in range(8):
                y = page * 8 + bit
                pixel = im.getpixel((x, y))
                if pixel == 0:  # 黑色为1
                    byte |= (1 << bit)
            oled_bytes.append(byte)

    print("unsigned char BMP_OLED[] = {")
    for i, b in enumerate(oled_bytes):
        if i % 16 == 0:
            print()
        print(f"0x{b:02X}, ", end='')
    print("\n};")

if __name__ == "__main__":
    input_file = r"D:\img\睡觉小狗\原\frame_001.png"  # 这里写你的输入文件绝对路径

    bmp_path = convert_to_128x64_bw_bmp(input_file)
    bmp_to_oled_array(bmp_path)
