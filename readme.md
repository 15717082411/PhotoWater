# 图片水印工具

一个简单的命令行工具，用于从图片的EXIF信息中提取拍摄日期并添加到图片上。

## 功能特性

- 自动从图片EXIF信息中提取拍摄日期
- 支持自定义水印字体大小、颜色和位置
- 支持批量处理目录中的所有图片
- 自动创建输出目录保存水印图片

## 环境要求

- Python 3.6+
- Pillow 库

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 处理单个图片文件

```bash
python main.py -i image.jpg
```

### 批量处理目录中的所有图片

```bash
python main.py -i images_folder
```

### 自定义水印参数

```bash
python main.py -i image.jpg --font-size 40 --opacity 150 --color 255,0,0 --position top-left
```

## 参数说明

- `-i`, `--input`: 输入图片文件路径或目录路径（必填）
- `--font-size`: 字体大小，默认30
- `--opacity`: 水印透明度（0-255），默认128
- `--color`: 文字颜色（RGB），默认255,255,255
- `--position`: 水印位置，可选值：top-left, top-right, bottom-left, bottom-right, center，默认bottom-right

## 输出说明

处理后的图片将保存在输入图片所在目录的一个名为`[原目录名]_watermark`的子目录中。

例如，如果输入图片路径为`C:\photos\image.jpg`，则输出图片将保存在`C:\photos\photos_watermark\image.jpg`。

## 注意事项

- 只有包含EXIF拍摄日期信息的图片才能被添加水印
- 程序会尝试加载系统中的中文字体（如黑体），如果不存在则使用默认字体
- 支持的图片格式：jpg, jpeg, png, bmp, gif\ n # #   Hr,g\ n 1 . 0 
 
 
