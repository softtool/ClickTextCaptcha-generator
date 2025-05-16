"""
验证码生成脚本

该脚本用于生成随机验证码图片，并将其保存到指定目录。
验证码支持以下类型：
- 纯数字（0-9）
- 英文字母（a-zA-Z）
- 常用汉字（可配置启用）
- 数学运算表达式（如 3 + 5 =？）

默认为4位长度，支持命令行参数控制数量和类型。
生成的图片保存在项目根目录下的 images/character/ClickTextCaptcha 目录中。

使用方法：
1. 安装依赖：pip install captcha
2. 运行脚本示例：
   python gen_by_image_captcha.py --count 20           # 生成20个默认类型的验证码（数字+字母）
   python gen_by_image_captcha.py --chinese           # 启用汉字验证码（需系统字体支持）
   python gen_by_image_captcha.py --arithmetic        # 生成数学运算类验证码
   python gen_by_image_captcha.py --no-use-digits     # 不使用数字
   python gen_by_image_captcha.py --no-use-letters    # 不使用英文字母

支持特性：
- 多字体混合渲染（微软雅黑、Arial 等）
- 字体大小随机变化
- 支持常用汉字过滤（避免生僻字）
- 可选是否添加哈希值防止重复文件名
"""

# 修改 gen_by_image_captcha.py 中的导入语句为绝对导入
from generate.character.ClickTextCaptcha.CustomImageCaptcha import CustomImageCaptcha

import string
import os
import argparse
import random
import re
from PIL import Image
from scipy.ndimage import map_coordinates
from PIL.ImageFilter import SMOOTH

import numpy as np
ADD_HASH = True  # 控制是否添加随机hash值
COMMON_CHINESE_CHARS = (
    "的了在和是就也你他我啊哦额不这有那说看进来着去上中下左又它们时能可可以对错"
    "你好谢谢再见请问是谁什么为什么怎么这里那里今天明天昨天现在早上中午晚上春天夏天秋天冬天"
    "高兴快乐伤心难过喜欢爱讨厌害怕希望相信想吃喝玩学工作学校老师学生家长孩子朋友家人"
    "大小多少高矮胖瘦快慢冷热干净漂亮清楚明白容易困难认真仔细简单复杂安静热闹有趣无聊"
    # 更多常用字...
)

def generate_random_captcha(length=4, use_digits=True, use_letters=True, use_chinese=False):
    """
    生成随机验证码文本

    :param length: 验证码长度
    :param use_digits: 是否使用数字
    :param use_letters: 是否使用英文字母
    :param use_chinese: 是否使用汉字
    :return: 验证码字符串
    """
    characters = ""
    if use_digits:
        characters += string.digits  # 0-9
    if use_letters:
        characters += string.ascii_letters  # a-zA-Z
    if use_chinese:
        characters += COMMON_CHINESE_CHARS  # 使用常用字集合

    if not characters:
        raise ValueError("必须启用至少一种字符类型（数字、字母或汉字）")

    captcha_text = ''.join(random.choices(characters, k=length))
    return captcha_text
def get_system_font_path(font_name):
    """
    根据字体名称查找系统字体路径
    :param font_name: 字体名称，如 "微软雅黑", "Arial"
    :return: 字体文件路径 or None
    """
    if os.name == "nt":  # Windows
        fonts_dir = os.path.join(os.environ["WINDIR"], "Fonts")
        font_files = {
            "微软雅黑": "msyh.ttc",
            "SimHei": "simhei.ttf",
            "Arial": "arial.ttf",
            "Arial Rounded MT Bold": "ARLRDBD.TTF",
            "Georgia": "georgia.ttf",
            "Impact": "impact.ttf",
            "Comic Sans MS": "comic.ttf",
            "Times New Roman": "times.ttf",
            "Courier New": "cour.ttf",
            # 新增字体支持
            "华文琥珀": "STHUPO.TTF",  # 华文琥珀字体文件名
            "隶书": "SIMLI.TTF"  # 隶书字体文件名
        }
        font_file = font_files.get(font_name)
        if font_file:
            return os.path.join(fonts_dir, font_file)
    elif os.name == "posix":  # Linux/Mac
        # 可扩展为通过 font_manager 查找字体
        pass
    return None


def add_background(image,bg_path):
    """
    随机选择一张背景图并将验证码叠加在其上。
    """
    # 确保 image 是 RGBA 模式
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # 获取 alpha 通道前先确认存在
    try:
        alpha = image.split()[3]
    except IndexError:
        alpha = None  # 或者根据需求处理无 alpha 的情况


    background = Image.open(bg_path).convert('RGB')

    # 将透明背景的验证码图像粘贴到背景图上
    background.paste(image, (0, 0), mask=alpha) # 使用 alpha 通道作为掩码
    return background


def warp(image: Image.Image, mag=3):
    """
    对输入的 PIL 图像进行波浪形扭曲变形

    :param image: 输入图像 (PIL.Image)
    :param mag: 扭曲强度 (越大越明显)
    :return: 扭曲后的图像 (PIL.Image)
    """
    # 将 PIL.Image 转换为 NumPy 数组
    data = np.array(image)

    # 获取图像尺寸 (h, w, c) => height, width, channel
    h, w, c = data.shape

    # 创建坐标网格 (y, x)，注意顺序是 y 在前
    y, x = np.mgrid[0:h, 0:w]

    # 添加正弦波扰动 (mag 控制强度)
    dx = np.sin(x / (w / mag)) * mag  # 水平方向扰动
    dy = np.sin(y / (h / mag)) * mag  # 垂直方向扰动

    # 合并为坐标场，顺序必须是 [y + dy, x + dx]
    coords = [np.clip(y + dy, 0, h - 1), np.clip(x + dx, 0, w - 1)]

    # 创建输出数组
    warped_data = np.zeros_like(data)

    # 对每个通道分别处理
    for i in range(c):
        warped_data[:, :, i] = map_coordinates(data[:, :, i], coords, order=1, mode='reflect')

    # 将 NumPy 数组转回 PIL.Image
    return Image.fromarray(warped_data)

def generate_captcha_image(captcha_text, use_chinese=False):
    # 基础字体列表
    base_font_names = [
        "Times New Roman",
        "Arial",
        "Georgia",
        "Comic Sans MS",
        "Courier New",
        "Arial Rounded MT Bold",

    ]

    # 如果是中文验证码，则只允许使用“微软雅黑”
    if use_chinese:
        available_font_names = ['微软雅黑', '华文琥珀', '隶书']
    else:
        available_font_names = ['微软雅黑'] + base_font_names
    # 动态查找字体路径
    available_fonts = []
    for name in available_font_names:
        path = get_system_font_path(name)
        if path and os.path.exists(path):
            available_fonts.append(path)

    if not available_fonts:
        raise RuntimeError("未找到任何可用字体，请检查系统字体或安装相关字体")

    # 设置字体大小范围，随机选择
    font_sizes = random.sample(range(35, 60), 3)  # 从35~60之间随机选3个不同大小

    bg_dir = "bg-images"
    bg_files = [f for f in os.listdir(bg_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not bg_files:
        raise FileNotFoundError("未找到可用的背景图片")

    bg_path = os.path.join(bg_dir, random.choice(bg_files))
    # 获取背景图尺寸
    with Image.open(bg_path) as bg_img:
        bg_width, bg_height = bg_img.size
        bg_img.close()
    # 创建 ImageCaptcha 实例
    image_captcha = CustomImageCaptcha(
        width=bg_width,
        height=bg_height,
        fonts=available_fonts,
        font_sizes=tuple(font_sizes)
    )

    captcha_image = image_captcha.create_captcha(captcha_text,  drawings=[
        lambda img: warp(img, mag=26),     # 波浪扭曲
        lambda img: img.filter(SMOOTH)    # 平滑处理
    ])
    # 假设 captcha_image 是 RGBA 模式的验证码图像
    background_image = add_background(captcha_image, bg_path)


    # 构建保存路径
    save_dir = os.path.abspath(os.path.join(__file__, '..','..', '..', '..', 'images', 'character', 'ClickTextCaptcha'))
    os.makedirs(save_dir, exist_ok=True)

    # 保存图片
    if ADD_HASH:
        import hashlib
        random_hash = hashlib.md5(captcha_text.encode()).hexdigest()[:8]
        filename = f"{captcha_text}_{random_hash}.png"
    else:
        filename = f"{captcha_text}.png"
    background_image.save(os.path.join(save_dir, filename))


def batch_generate_captchas(count=10, length=4, use_digits=True, use_letters=True, use_chinese=False):
    for _ in range(count):
        captcha_text = generate_random_captcha(length, use_digits, use_letters, use_chinese)
        generate_captcha_image(captcha_text, use_chinese=use_chinese)
        print(f"Captcha text: {captcha_text}")

def batch_generate_arithmetic_captchas(count=10):
    """
    批量生成数学运算并打印结果

    :param count: 要生成的数学运算数量
    """
    for _ in range(count):
        expression, result = generate_arithmetic_captcha()
        print(f"Expression: {expression}, Result: {result}")

def generate_arithmetic_captcha():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    op = random.choice(['+', '-', '*'])
    op = random.choice(['+', '-'])

    if op == '+':
        result = num1 + num2
        expression = f"{num1} + {num2} =？"
    elif op == '-':
        # 确保不产生负数，并修正表达式
        a = max(num1, num2)
        b = min(num1, num2)
        result = a - b
        expression = f"{a} - {b} =？"
    else:
        result = num1 * num2
        expression = f"{num1} * {num2} =？"

    gentext = re.sub(r'[\\/*?:"<>|]', '_', expression)
    generate_captcha_image(gentext,use_chinese=True)
    return expression, str(result)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量生成验证码")
    parser.add_argument("--count", type=int, default=10, help="要生成的验证码数量，默认为10")
    parser.add_argument("--arithmetic", action="store_true", help="是否生成数学运算类验证码")
    parser.add_argument("--use-digits", action="store_true", default=True, help="是否使用数字，默认启用")
    parser.add_argument("--use-letters", action="store_true", default=True, help="是否使用英文字母，默认启用")
    parser.add_argument("--use-chinese", action="store_true", help="是否使用汉字，默认禁用")

    args = parser.parse_args()

    # if args.arithmetic:
    #     batch_generate_arithmetic_captchas(args.count)
    # else:
    #     batch_generate_captchas(
    #         count=args.count,
    #         length=4,
    #         use_digits=args.use_digits,
    #         use_letters=args.use_letters,
    #         use_chinese=args.use_chinese
    #     )


    batch_generate_captchas(3, use_digits=False, use_letters=False, use_chinese=True)