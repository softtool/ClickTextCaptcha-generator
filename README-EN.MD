# Captcha Generation Script Documentation
English https://github.com/softtool/captcha-generator/blob/main/README-EN.MD

中文 https://github.com/softtool/captcha-generator/blob/main/README.md

## Overview
This script is used to generate random captcha images and save them to a specified directory.


![8 + 6 =？_56670675.png](images/character/ImageCaptcha/8%20%2B%206%20%3D%EF%BC%9F_56670675.png)
![3 + 8 =？_6cdd1e9d.png](images/character/ImageCaptcha/3%20%2B%208%20%3D%EF%BC%9F_6cdd1e9d.png)
![jKsF_8ecb373d.png](images/character/ImageCaptcha/jKsF_8ecb373d.png)
![sVAW_bdc54215.png](images/character/ImageCaptcha/sVAW_bdc54215.png)
![子么来趣_7b951bcd.png](images/character/ImageCaptcha/%E5%AD%90%E4%B9%88%E6%9D%A5%E8%B6%A3_7b951bcd.png)
![相这静讨_d7282dd6.png](images/character/ImageCaptcha/%E7%9B%B8%E8%BF%99%E9%9D%99%E8%AE%A8_d7282dd6.png)

## Features
- **Supported Types**:
  - Numeric digits (0-9)
  - English letters (a-zA-Z)
  - Common Chinese characters (configurable)
- **Length Control**: Default length is 4 characters, supports command-line arguments to control the number of generated captchas.
- **Storage Path**: Generated images are saved in the `images/character/ImageCaptcha` directory under the project root.

## Usage
1. Install dependencies: Ensure that the `captcha` library is installed (use the command `pip install captcha`).
2. Run the script; the generated captcha text and images will be displayed in the console and saved to the specified directory.

## Example Commands
- `python gen_by_image_captcha.py --count 20`: Generates 20 default type captchas (numbers + letters).
- `python gen_by_image_captcha.py --chinese`: Enables Chinese character captchas (requires system font support).

## Advanced Features
- Mixed font rendering (e.g., Microsoft YaHei, Arial, etc.).
- Random font sizes to enhance visual diversity of the captchas.
- Support for filtering common Chinese characters to avoid obscure characters.

---

# Downloading the Code

Use the `git` command to clone the project to your local machine:

```bash
git clone https://github.com/softtool/captcha-generator.git
```


---

# Setting Up the Environment

It is recommended to use `conda` to create an isolated Python environment. Run the following commands to create and activate the environment:

Navigate into the captcha-generator directory:

```bash
conda create -p runtime python=3.10
conda activate ./runtime
```


---

# Installing Dependencies

Once the environment is activated, install the project dependencies:

```bash
pip install -r requirements.txt
```


---

# Generating Images

Navigate to the captcha image generation directory and run the script:

```bash
cd generate/character/ImageCaptcha
python gen_by_image_captcha.py
```

The script will generate captcha images based on configurations. You can adjust parameters within the script according to your needs.