#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图片水印工具 - 命令行程序
功能：从图片EXIF信息提取拍摄时间并添加水印
"""

import argparse
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


def get_exif_date(image_path):
    """
    从图片EXIF信息中提取拍摄日期
    :param image_path: 图片路径
    :return: 格式化的日期字符串（YYYY-MM-DD），如果无法提取则返回None
    """
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if exif_data:
            # 36867是EXIF中日期时间的标签ID
            date_time_original = exif_data.get(36867)
            if date_time_original:
                # 解析日期时间字符串 (格式通常为：YYYY:MM:DD HH:MM:SS)
                date_time_obj = datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S')
                # 返回YYYY-MM-DD格式
                return date_time_obj.strftime('%Y-%m-%d')

        return None
    except Exception as e:
        print(f"提取EXIF信息时出错：{str(e)}")
        return None


def add_text_watermark(image_path, output_path, text, font_size=30, opacity=128,
                       color=(255, 255, 255), position='bottom-right'):
    """
    添加文字水印
    :param image_path: 原图路径
    :param output_path: 输出图片路径
    :param text: 水印文字
    :param font_size: 字体大小
    :param opacity: 透明度（0-255）
    :param color: 文字颜色
    :param position: 水印位置 (top-left, top-right, bottom-left, bottom-right, center)
    """
    try:
        # 打开图片
        image = Image.open(image_path).convert('RGBA')
        width, height = image.size

        # 创建水印图层
        watermark = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        # 加载字体（尝试使用系统字体）
        try:
            font = ImageFont.truetype("simhei.ttf", font_size)  # 尝试加载黑体
        except IOError:
            try:
                font = ImageFont.truetype("Arial.ttf", font_size)  # 尝试加载Arial
            except IOError:
                font = ImageFont.load_default()  # 使用默认字体

        # 获取文字尺寸 - 使用新版本的textbbox方法替代textsize
        # 获取文字尺寸
        try:
            # 对于Pillow 9.0.0及以上版本
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # 对于旧版本的Pillow
            text_width, text_height = draw.textsize(text, font=font)

        # 计算水印位置
        padding = 20  # 边距
        if position == 'top-left':
            x, y = padding, padding
        elif position == 'top-right':
            x, y = width - text_width - padding, padding
        elif position == 'bottom-left':
            x, y = padding, height - text_height - padding
        elif position == 'bottom-right':
            x, y = width - text_width - padding, height - text_height - padding
        elif position == 'center':
            x, y = (width - text_width) // 2, (height - text_height) // 2
        else:
            # 默认右下角
            x, y = width - text_width - padding, height - text_height - padding

        # 添加文字水印
        draw.text((x, y), text, font=font, fill=(*color, opacity))

        # 合成图片
        result = Image.alpha_composite(image, watermark)
        result = result.convert('RGB')  # 转换回RGB模式

        # 保存结果
        result.save(output_path)
        print(f"成功添加水印：{output_path}")

    except Exception as e:
        print(f"添加水印时出错：{str(e)}")


def process_directory(input_dir):
    """
    处理目录中的所有图片
    :param input_dir: 输入目录路径
    """
    # 创建输出目录
    output_dir = os.path.join(input_dir, f"{os.path.basename(input_dir)}_watermark")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 支持的图片格式
    supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

    # 遍历输入目录
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in supported_formats:
            # 获取EXIF日期
            date_str = get_exif_date(file_path)
            if date_str:
                # 准备输出路径
                output_path = os.path.join(output_dir, file)

                # 添加水印
                add_text_watermark(
                    file_path,
                    output_path,
                    date_str,
                    font_size=args.font_size,
                    opacity=args.opacity,
                    color=args.color,
                    position=args.position
                )
            else:
                print(f"无法从{file}提取拍摄日期，跳过此文件")


def main():
    """
    主函数
    """
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='图片水印工具 - 从EXIF信息提取拍摄日期作为水印')

    # 基本参数
    parser.add_argument('-i', '--input', required=True, help='输入图片文件或目录路径')

    # 水印参数
    parser.add_argument('--font-size', type=int, default=30, help='字体大小，默认30')
    parser.add_argument('--opacity', type=int, default=128, help='水印透明度（0-255），默认128')
    parser.add_argument('--color', type=str, default='255,255,255', help='文字颜色（RGB），默认255,255,255')
    parser.add_argument('--position', type=str, default='bottom-right',
                        choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'],
                        help='水印位置，默认右下角')

    # 解析参数
    global args
    args = parser.parse_args()

    # 处理颜色参数
    try:
        args.color = tuple(map(int, args.color.split(','))) if args.color else (255, 255, 255)
    except ValueError:
        print("颜色格式错误，使用默认颜色(255,255,255)")
        args.color = (255, 255, 255)

    # 验证透明度参数
    if not (0 <= args.opacity <= 255):
        print("透明度值无效，使用默认值128")
        args.opacity = 128

    # 执行水印操作
    if os.path.isdir(args.input):
        # 处理目录
        process_directory(args.input)
    elif os.path.isfile(args.input):
        # 处理单个文件
        # 获取EXIF日期
        date_str = get_exif_date(args.input)
        if date_str:
            # 创建输出目录
            input_dir = os.path.dirname(args.input)
            output_dir = os.path.join(input_dir, f"{os.path.basename(input_dir)}_watermark")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 准备输出路径
            file_name = os.path.basename(args.input)
            output_path = os.path.join(output_dir, file_name)

            # 添加水印
            add_text_watermark(
                args.input,
                output_path,
                date_str,
                font_size=args.font_size,
                opacity=args.opacity,
                color=args.color,
                position=args.position
            )
        else:
            print(f"无法从{args.input}提取拍摄日期")
    else:
        print(f"输入路径不存在：{args.input}")


if __name__ == '__main__':
    main()