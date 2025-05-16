import os
import random
import json
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from datetime import datetime


class ClickCaptchaGeneratorPro:
    def __init__(self):
        # 初始化配置
        self.output_dir = "captcha_output"
        self.bg_images_dir = "bg-images"
        self.data_file = "captcha_records.json"
        self.fonts = self._load_enhanced_fonts()

        # 确保目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.bg_images_dir, exist_ok=True)




    def _calc_font_size(self, num_chars, img_height):
        """根据字符数和图片高度动态计算字体大小"""
        min_size = max(32, img_height // 12)  # 提高最小字体大小
        max_size = min(300, img_height // 5)  # 增加最大字体大小上限

        # 基础尺寸随字符数增加而减小
        base_size = max_size - (num_chars * 2)  # 每增加一个字符，字体减少 2 点   # 可根据实际需求调整比例系数

        # 随机浮动 ±20%
        fluctuation = random.uniform(-0.1, 0.1)  # 减少到 ±10%
        final_size = int(base_size * (1 + fluctuation))

        return max(min(final_size, max_size), min_size)

    def _load_enhanced_fonts(self, size=None):
        """加载指定大小的字体集"""
        if size is None:
            sizes = [48, 52, 56]
        else:
            sizes = [size]

        fonts = []
        for size in sizes:
            for path in self._find_system_fonts():
                try:
                    fonts.append(ImageFont.truetype(path, size=size))
                except:
                    continue
        return fonts or [ImageFont.load_default()]

    def _find_system_fonts(self):
        """查找系统字体（优先使用已知中文字体）"""
        font_paths = []

        # 预定义要查找的字体列表（中文优先）
        preferred_fonts = [
            ("微软雅黑", "msyh.ttc"),
            ("黑体", "simhei.ttf"),
            ("楷体", "simkai.ttf"),
            ("宋体", "simsun.ttc"),
            ("Arial", "arial.ttf"),
            ("Verdana", "verdana.ttf")
        ]

        if os.name == "nt":  # Windows 系统
            try:
                fonts_dir = os.path.join(os.environ["WINDIR"], "Fonts")
                for font_name, font_file in preferred_fonts:
                    font_path = os.path.join(fonts_dir, font_file)
                    if os.path.exists(font_path):
                        print(f"✅ 找到字体：{font_name} -> {font_path}")
                        font_paths.append(font_path)
                    else:
                        print(f"❌ 未找到字体：{font_name}（路径：{font_path}）")
            except Exception as e:
                print(f"⚠️ Windows 字体查找异常：{e}")

        elif os.name == "posix":  # Linux / macOS
            try:
                from matplotlib import font_manager
                fm = font_manager.FontManager()

                for font_name, _ in preferred_fonts:
                    found = False
                    for f in fm.ttflist:
                        if font_name.lower() in f.name.lower():
                            print(f"✅ 找到字体：{f.name} -> {f.fname}")
                            font_paths.append(f.fname)
                            found = True
                            break
                    if not found:
                        print(f"❌ 未找到字体：{font_name}")
            except ImportError:
                print("⚠️ matplotlib 未安装，无法自动查找字体")
            except Exception as e:
                print(f"⚠️ 系统字体查找失败：{e}")

        else:
            print("⚠️ 不支持的操作系统")

        if not font_paths:
            print("⚠️ 未找到任何可用字体，将使用 PIL 默认字体")

        return font_paths

    def _generate_gradient_bg(self, size):
        """生成渐变背景"""
        w, h = size
        img = Image.new('RGB', size, (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # 横向渐变
        for x in range(w):
            r = int(255 * math.sin(math.pi * x / w))
            g = int(255 * math.cos(math.pi * x / (2 * w)))
            b = int(255 * math.sin(math.pi * (x + w / 2) / w))
            draw.line([(x, 0), (x, h)], fill=(r, g, b))
        return img

    def _get_optimized_bg(self, size=(1000, 500)):
        """获取优化后的背景"""
        # 1. 尝试获取本地背景图
        valid_bgs = [f for f in os.listdir(self.bg_images_dir)
                     if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if valid_bgs:
            bg_path = os.path.join(self.bg_images_dir, random.choice(valid_bgs))
            img = Image.open(bg_path).convert('RGB')
        else:
            # 2. 生成渐变背景
            img = self._generate_gradient_bg(size)

        # 亮度均衡处理
        enhancer = ImageEnhance.Brightness(img.resize(size))
        return enhancer.enhance(0.8).filter(ImageFilter.SMOOTH_MORE)

    def _calc_contrast_color(self, img, area):
        """计算区域对比色"""
        crop = img.crop(area)
        histogram = crop.convert('L').histogram()
        avg_brightness = sum(i * val for i, val in enumerate(histogram)) / sum(histogram)
        return (0, 0, 0) if avg_brightness > 128 else (255, 255, 255)

    def _draw_char_with_effect(self, draw, char, position, font, color):
        # 在原有对比色基础上增加10%的随机色差
        varied_color = (
            min(255, max(0, color[0] + random.randint(-25, 25))),
            min(255, max(0, color[1] + random.randint(-25, 25))),
            min(255, max(0, color[2] + random.randint(-25, 25)))
        )

        # 文字描边改为随机深色
        stroke_color = (
            random.randint(0, 250),
            random.randint(0, 50),
            random.randint(0, 150)
        )

        # 增加描边密度
        for offset in [(-3, -3), (-3, 0), (-3, 3), (0, -3), (0, 3), (3, -3), (3, 0), (3, 3)]:
            draw.text((position[0] + offset[0], position[1] + offset[1]),
                      char, font=font, fill=stroke_color)

        # 增加文字渐变色
        for i in range(3):
            draw.text((position[0] + i, position[1] + i), char,
                      font=font, fill=varied_color)

    def _is_overlap(self, new_area, used_areas):
        """判断新区域是否与已有区域重叠"""
        nx1, ny1, nx2, ny2 = new_area
        for area in used_areas:
            ax1, ay1, ax2, ay2 = area
            if not (nx2 < ax1 or nx1 > ax2 or ny2 < ay1 or ny1 > ay2):
                return True
        return False
    def generate_captcha(self, char_sets, num_chars=5, size=(1000, 500)):
            img_height = size[1]
            font_size = self._calc_font_size(num_chars, img_height)
            self.fonts = self._load_enhanced_fonts(font_size)

            bg = self._get_optimized_bg(size)
            draw = ImageDraw.Draw(bg)
            used_areas = []
            positions = []

            # 生成噪点背景
            for _ in range(random.randint(300, 500)):
                x = random.randint(0, size[0])
                y = random.randint(0, size[1])
                draw.rectangle([x, y, x + 2, y + 2],
                               fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            # 生成干扰线
            for _ in range(random.randint(10, 15)):
                x1 = random.randint(0, size[0])
                y1 = random.randint(0, size[1])
                x2 = random.randint(0, size[0])
                y2 = random.randint(0, size[1])
                draw.line([x1, y1, x2, y2],
                          fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                          width=2)

            # 生成文字
            for _ in range(num_chars):
                char = random.choice(char_sets)
                font = random.choice(self.fonts)

                # 计算字符尺寸
                bbox = font.getbbox(char)
                char_w = bbox[2] - bbox[0]
                char_h = bbox[3] - bbox[1]

                # 寻找非重叠位置
                attempt = 0
                while attempt < 50:
                    x = random.randint(20, size[0] - char_w - 20)
                    y = random.randint(20, size[1] - char_h - 20)
                    angle = random.uniform(-25, 25)
                    current_area = (
                        x - 10, y - 10,
                        x + char_w + 10,
                        y + char_h + 10
                    )

                    if not self._is_overlap(current_area, used_areas):
                        break
                    attempt += 1

                # 确定颜色：生成与背景对比的随机颜色
                bg_region = bg.crop(current_area)
                avg_color = self._get_average_color(bg_region)
                avg_brightness = avg_color[0] * 0.299 + avg_color[1] * 0.587 + avg_color[2] * 0.114

                # 根据背景亮度生成高对比度随机颜色
                if avg_brightness > 128:
                    # 背景较亮，生成暗色系随机颜色
                    text_color = (
                        random.randint(0, 100),
                        random.randint(0, 100),
                        random.randint(0, 100)
                    )
                else:
                    # 背景较暗，生成亮色系随机颜色
                    text_color = (
                        random.randint(200, 255),
                        random.randint(200, 255),
                        random.randint(200, 255)
                    )

                # 创建文字图层
                text_layer = Image.new('RGBA', size)
                text_draw = ImageDraw.Draw(text_layer)

                # 绘制旋转文字
                rotated_layer = Image.new('RGBA', (char_w * 2, char_h * 2))
                r_draw = ImageDraw.Draw(rotated_layer)
                self._draw_char_with_effect(r_draw, char, (char_w // 2, char_h // 2), font, text_color)
                rotated_layer = rotated_layer.rotate(angle, expand=True, resample=Image.BICUBIC)

                # 合成文字到主图
                paste_pos = (
                    x - rotated_layer.width // 4,
                    y - rotated_layer.height // 4
                )
                bg.paste(rotated_layer, paste_pos, rotated_layer)

                # 记录位置信息
                positions.append({
                    "char": char,
                    "x": x + rotated_layer.width // 4,
                    "y": y + rotated_layer.height // 4,
                    "width": char_w,
                    "height": char_h,
                    "angle": round(angle, 1)
                })
                used_areas.append(current_area)

            return bg.filter(ImageFilter.SHARPEN), positions

    def _get_average_color(self, image):
        # 快速获取图像区域的平均颜色
        small_img = image.resize((1, 1), Image.Resampling.LANCZOS)
        color = small_img.getpixel((0, 0))
        return color[:3]  # 返回RGB，忽略Alpha通道
    def generate_batch(self, chinese_chars="点击验证码", english_chars="ABCDEFGHKMNPQRST",
                       num_chars=4, quantity=10):
        """批量生成入口"""
        char_set = list(chinese_chars + english_chars)
        records = {}

        for _ in range(quantity):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            filename = f"captcha_{timestamp}.jpg"
            image, positions = self.generate_captcha(char_set, num_chars)
            image.save(os.path.join(self.output_dir, filename), quality=95)
            records[filename] = positions

        # 保存记录
        with open(os.path.join(self.output_dir, self.data_file), 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    generator = ClickCaptchaGeneratorPro()
    generator.generate_batch(
        chinese_chars="请点击下面所示的文字内容",
        english_chars="ABCDEFGHKMNPQRSTUVWXYZ",
        num_chars=5,
        quantity=2
    )