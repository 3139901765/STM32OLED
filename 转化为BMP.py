from PIL import Image

def convert_png_to_128x64_bw_bmp(input_path, output_path):
    img = Image.open(input_path)
    img = img.resize((128, 64), Image.Resampling.LANCZOS)  # Pillow新版推荐用法
    img = img.convert('L')  # 转灰度图
    img = img.point(lambda x: 0 if x < 128 else 255, '1')  # 二值化处理（阈值128）
    img.save(output_path, format='BMP')
    print(f"转换完成，保存到：{output_path}")

if __name__ == "__main__":
    input_file = r"C:\Users\Duan\Desktop\睁开眼睛.bmp"    # 这里写你的输入文件绝对路径
    output_file = r"D:\PythonProject\素材库\output4.bmp"  # 这里写你的输出文件路径

    convert_png_to_128x64_bw_bmp(input_file, output_file)
