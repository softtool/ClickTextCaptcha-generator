from PIL import Image, ImageDraw, ImageFont
import random
from captcha.image import ImageCaptcha

class CustomImageCaptcha(ImageCaptcha):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 确保 _fonts 被正确初始化
        self._fonts = kwargs.get('fonts', [])
        self.width =  kwargs.get('width', [])
        self.height =  kwargs.get('height', [])

    def _calc_font_size(self, num_chars, img_height):
        """根据字符数和图片高度动态计算字体大小"""
        min_size = max(40, img_height // 11)  # 提高最小字体大小
        max_size = min(300, img_height // 8)  # 增加最大字体大小上限

        # 基础尺寸随字符数增加而减小
        base_size = max_size - (num_chars * 2)  # 每增加一个字符，字体减少 2 点   # 可根据实际需求调整比例系数

        # 随机浮动 ±20%
        fluctuation = random.uniform(-1.0, 1.0)  # 减少到 ±10%
        final_size = int(base_size * (1 + fluctuation))

        return max(min(final_size, max_size), min_size)
    def create_captcha(self, text, fonts=None, font_sizes=None, drawings=()):
        if fonts is None:
            fonts = self._fonts
        if font_sizes is None:
            font_sizes = self._font_sizes

        # 创建 RGBA 图像（透明背景）
        image = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)


        # 存储已绘制字符的位置和大小，用于避免重叠
        occupied_boxes = []

        def is_overlap(new_box):
            """判断新字符是否会与其他字符重叠"""
            for box in occupied_boxes:
                if not (new_box[2] < box[0] or new_box[0] > box[2] or
                        new_box[3] < box[1] or new_box[1] > box[3]):
                    return True
            return False

        # 逐字绘制
        for char in text:
            # 每个字颜色不同
            r = random.randint(150, 255)
            g = random.randint(150, 255)
            b = random.randint(150, 255)
            color = (r, g, b, 255)

            # 随机选择字体，并使用动态计算的字体大小
            selected_font_path = random.choice(fonts)
            font = ImageFont.truetype(selected_font_path, self._calc_font_size(len(text), self.height))

            # 获取字符宽度
            char_bbox = draw.textbbox((0, 0), char, font=font)
            char_width = char_bbox[2] - char_bbox[0]
            char_height = char_bbox[3] - char_bbox[1]

            # 尝试生成不重叠的坐标
            for _ in range(100):  # 最多尝试100次防止死循环
                x = random.randint(0, self.width - char_width)
                y = random.randint(0, self.height - char_height)
                new_box = [x, y, x + char_width, y + char_height]

                if not is_overlap(new_box):
                    break
            else:
                # 如果100次都找不到合适位置，则默认放在中间附近
                x = random.randint(self.width // 2 - 20, self.width // 2 + 20)
                y = random.randint(self.height // 2 - 10, self.height // 2 + 10)

            # 绘制字符
            draw.text((x, y), char, fill=color, font=font)

            # 记录该字符占用的区域
            occupied_boxes.append(new_box)

        # 应用干扰元素
        for drawing in drawings:
            image = drawing(image)

        return image


