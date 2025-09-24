# 图片水印工具

一个简单的命令行工具，用于给图片添加文字或图片水印。

## 功能特性

- 支持添加文字水印
- 支持添加图片水印
- 支持批量处理多个图片
- 可自定义水印透明度、大小、颜色等参数

## 环境要求

- Python 3.6+ 
- Pillow 库

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 添加文字水印

```bash
python main.py -i input.jpg -o output.jpg -t "水印文字" --font-size 30 --opacity 128 --color 255,255,255
```

### 添加图片水印

```bash
python main.py -i input.jpg -o output.jpg -w watermark.png --opacity 128 --scale 0.2
```

### 批量处理

```bash
python main.py -i input_folder -o output_folder -t "水印文字" --batch
```

## 参数说明

- `-i`, `--input`: 输入图片路径或目录（必填）
- `-o`, `--output`: 输出图片路径或目录（必填）
- `-t`, `--text`: 水印文字（与 `-w` 二选一）
- `-w`, `--watermark`: 水印图片路径（与 `-t` 二选一）
- `-a`, `--opacity`: 水印透明度（0-255），默认128
- `--font-size`: 文字大小，默认30
- `--color`: 文字颜色（RGB），默认255,255,255
- `--scale`: 水印缩放比例，默认0.2
- `--batch`: 批量处理模式

## 示例

添加半透明白色文字水印：
```bash
python main.py -i photo.jpg -o photo_watermark.jpg -t "我的图片" --opacity 100
```

添加自定义大小的图片水印：
```bash
python main.py -i photo.jpg -o photo_watermark.jpg -w logo.png --scale 0.3
```
