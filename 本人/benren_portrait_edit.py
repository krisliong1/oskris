from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import os

def apply_vintage_filter(image):
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # 精准匹配原图暖棕色调
    vintage = img_cv.copy()
    vintage[:, :, 1] = np.clip(vintage[:, :, 1] * 0.85, 0, 255)  # 降低绿色
    vintage[:, :, 2] = np.clip(vintage[:, :, 2] * 0.72, 0, 255)  # 降低蓝色
    
    # 柔和光影调整
    vintage = cv2.convertScaleAbs(vintage, alpha=1.03, beta=3)
    
    # 细腻胶片颗粒感
    noise = np.random.normal(0, 2.5, vintage.shape).astype(np.int16)
    vintage = np.clip(vintage + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(cv2.cvtColor(vintage, cv2.COLOR_BGR2RGB))

def add_face_text(image, text_left="keep", text_right="your self"):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # 确保手写字体加载
    try:
        font = ImageFont.truetype("IndieFlower.ttf", 28)
    except:
        try:
            font = ImageFont.truetype("Comic Sans MS.ttf", 28)
        except:
            font = ImageFont.load_default(size=28)
    
    # 精准定位文字
    draw.text((width * 0.27, height * 0.32), text_left, font=font, fill="black", stroke_width=1)
    draw.text((width * 0.56, height * 0.31), text_right, font=font, fill="black", stroke_width=1)
    
    return image

if __name__ == "__main__":
    input_path = "your_image.jpg"
    output_path = "vintage_portrait_verified.jpg"
    
    # 检查输入文件
    if not os.path.exists(input_path):
        print(f"错误：输入文件 {input_path} 不存在！")
    else:
        # 创建输出目录
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with Image.open(input_path).convert("RGB") as img:
            vintage_img = apply_vintage_filter(img)
            final_img = add_face_text(vintage_img)
            final_img.save(output_path)
            print(f"✅ 验证完成！图片已保存到: {output_path}")