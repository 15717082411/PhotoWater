#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图片水印工具 - 命令行程序
功能：给图片添加文字或图片水印
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont


def add_text_watermark(image_path, output_path, text, font_size=30, opacity=128, color=(255, 255, 255)):
    """
    添加文字水印
    :param image_path: 原图路径
    :param output_path: 输出图片路径
    :param text: 水印文字
    :param font_size: 字体大小
    :param opacity: 透明度（0-255）
    :param color: 文字颜色
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
        
        # 获取文字尺寸
        text_width, text_height = draw.textsize(text, font=font)
        
        # 计算水印位置（右下角）
        x = width - text_width - 20
        y = height - text_height - 20
        
        # 添加文字水印
        draw.text((x, y), text, font=font, fill=(*color, opacity))
        
        # 合成图片
        result = Image.alpha_composite(image, watermark)
        result = result.convert('RGB')  # 转换回RGB模式
        
        # 保存结果
        result.save(output_path)
        print(f"成功添加文字水印：{output_path}")
        
    except Exception as e:
        print(f"添加文字水印时出错：{str(e)}")


def add_image_watermark(image_path, output_path, watermark_path, opacity=128, scale=0.2):
    """
    添加图片水印
    :param image_path: 原图路径
    :param output_path: 输出图片路径
    :param watermark_path: 水印图片路径
    :param opacity: 透明度（0-255）
    :param scale: 水印缩放比例
    """
    try:
        # 打开原图和水印图
        image = Image.open(image_path).convert('RGBA')
        watermark = Image.open(watermark_path).convert('RGBA')
        
        # 调整水印大小
        width, height = image.size
        wm_width = int(width * scale)
        wm_height = int(watermark.height * (wm_width / watermark.width))
        watermark = watermark.resize((wm_width, wm_height), Image.LANCZOS)
        
        # 调整水印透明度
        if opacity != 255:
            alpha = watermark.split()[3]
            alpha = alpha.point(lambda p: p * opacity / 255)
            watermark.putalpha(alpha)
        
        # 计算水印位置（右下角）
        x = width - wm_width - 20
        y = height - wm_height - 20
        
        # 创建新图层并添加水印
        result = Image.new('RGBA', image.size, (0, 0, 0, 0))
        result.paste(image, (0, 0))
        result.paste(watermark, (x, y), watermark)
        
        # 保存结果
        result.convert('RGB').save(output_path)
        print(f"成功添加图片水印：{output_path}")
        
    except Exception as e:
        print(f"添加图片水印时出错：{str(e)}")


def batch_process(input_dir, output_dir, **kwargs):
    """
    批量处理图片
    :param input_dir: 输入目录
    :param output_dir: 输出目录
    :param kwargs: 水印参数
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 支持的图片格式
    supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    
    # 遍历输入目录
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in supported_formats:
            output_path = os.path.join(output_dir, file)
            
            # 根据参数选择水印类型
            if 'text' in kwargs:
                add_text_watermark(file_path, output_path, **kwargs)
            elif 'watermark_path' in kwargs:
                add_image_watermark(file_path, output_path, **kwargs)


def main():
    """主函数"""
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='图片水印工具')
    
    # 基本参数
    parser.add_argument('-i', '--input', required=True, help='输入图片路径或目录')
    parser.add_argument('-o', '--output', required=True, help='输出图片路径或目录')
    
    # 水印类型参数组
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--text', help='水印文字')
    group.add_argument('-w', '--watermark', help='水印图片路径')
    
    # 水印通用参数
    parser.add_argument('-a', '--opacity', type=int, default=128, help='水印透明度（0-255），默认128')
    
    # 文字水印特有参数
    parser.add_argument('--font-size', type=int, default=30, help='文字大小，默认30')
    parser.add_argument('--color', type=str, default='255,255,255', help='文字颜色（RGB），默认255,255,255')
    
    # 图片水印特有参数
    parser.add_argument('--scale', type=float, default=0.2, help='水印缩放比例，默认0.2')
    
    # 批量处理标志
    parser.add_argument('--batch', action='store_true', help='批量处理模式')
    
    # 解析参数
    args = parser.parse_args()
    
    # 处理颜色参数
    color = tuple(map(int, args.color.split(','))) if args.color else (255, 255, 255)
    
    # 准备参数
    kwargs = {'opacity': args.opacity}
    if args.text:
        kwargs['text'] = args.text
        kwargs['font_size'] = args.font_size
        kwargs['color'] = color
    elif args.watermark:
        kwargs['watermark_path'] = args.watermark
        kwargs['scale'] = args.scale
    
    # 执行水印操作
    if args.batch or (os.path.isdir(args.input) and os.path.isdir(args.output)):
        # 批量处理
        batch_process(args.input, args.output, **kwargs)
    else:
        # 单文件处理
        if args.text:
            add_text_watermark(args.input, args.output, **kwargs)
        elif args.watermark:
            add_image_watermark(args.input, args.output, **kwargs)


if __name__ == '__main__':
    main()
