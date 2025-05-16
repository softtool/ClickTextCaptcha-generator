# 验证码生成脚本说明
English https://github.com/softtool/captcha-generator/blob/main/README-EN.MD

中文 https://github.com/softtool/captcha-generator/blob/main/README.md

## 概述
该脚本用于生成随机验证码图片，并将其保存到指定目录。


![8 + 6 =？_56670675.png](images/character/ImageCaptcha/8%20%2B%206%20%3D%EF%BC%9F_56670675.png)
![3 + 8 =？_6cdd1e9d.png](images/character/ImageCaptcha/3%20%2B%208%20%3D%EF%BC%9F_6cdd1e9d.png)
![jKsF_8ecb373d.png](images/character/ImageCaptcha/jKsF_8ecb373d.png)
![sVAW_bdc54215.png](images/character/ImageCaptcha/sVAW_bdc54215.png)
![子么来趣_7b951bcd.png](images/character/ImageCaptcha/%E5%AD%90%E4%B9%88%E6%9D%A5%E8%B6%A3_7b951bcd.png)
![相这静讨_d7282dd6.png](images/character/ImageCaptcha/%E7%9B%B8%E8%BF%99%E9%9D%99%E8%AE%A8_d7282dd6.png)

### 功能特性
- **支持类型**：
  - 纯数字（0-9）
  - 英文字母（a-zA-Z）
  - 常用汉字（可配置启用）
- **长度控制**：默认为4位长度，支持命令行参数控制生成数量。
- **存储路径**：生成的图片保存在项目根目录下的 `images/character/ImageCaptcha` 目录中。

### 使用方法
1. 安装依赖：确保安装了 `captcha` 库 (使用命令 `pip install captcha`）。
2. 运行脚本，生成的验证码文本和图片将显示在控制台，并保存至指定目录。

### 示例命令
- `   python gen_by_image_captcha.py --count 20 `：          # 生成20个默认类型的验证码（数字+字母）
- `   python gen_by_image_captcha.py --chinese  `：         # 启用汉字验证码（需系统字体支持）
- `   python gen_by_image_captcha.py --arithmetic  `：      # 生成数学运算类验证码
- `   python gen_by_image_captcha.py --no-use-digits `：    # 不使用数字
- `   python gen_by_image_captcha.py --no-use-letters `：   # 不使用英文字母

### 高级支持
- 多字体混合渲染（如微软雅黑、Arial 等）。
- 字体大小随机变化，增强验证码的视觉多样性。
- 支持常用汉字过滤，避免生成生僻字。

# 下载代码

使用 `git` 命令将项目克隆到本地：

``` bash
git clone https://github.com/softtool/captcha-generator.git
```

---

# 创建环境

建议使用 `conda` 来创建独立的 Python 环境。运行以下命令来创建并激活环境：
进入到captcha-generator目录中
``` bash
conda create -p runtime python=3.10
conda activate ./runtime
```

---

# 安装依赖

在激活的环境中，安装项目所需的依赖包：

``` bash
pip install -r requirements.txt
```

---

# 生成图片

进入生成验证码图片的目录，并运行脚本：

``` bash
cd generate/character/ImageCaptcha
python gen_by_image_captcha.py
```
该脚本会基于配置生成对应的验证码图片。您可以根据需求调整脚本中的参数。

---
```

