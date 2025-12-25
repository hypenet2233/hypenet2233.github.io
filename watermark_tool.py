import os
from PIL import Image, ImageEnhance

# ============================
# إعدادات الأداة
# ============================
LOGO_SIZE_RATIO = 0.2  # حجم الشعار بالنسبة للصورة (20%)
OPACITY = 0.7          # شفافية الشعار (0.0 شفاف - 1.0 معتم)
PADDING = 20           # المسافة من الحافة

def add_watermark(input_folder, logo_path):
    # إنشاء مجلد للنتائج
    output_folder = os.path.join(input_folder, "watermarked_images")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        # تحميل الشعار
        watermark = Image.open(logo_path).convert("RGBA")
        
        # تقليل شفافية الشعار
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(OPACITY)
        watermark.putalpha(alpha)
        
        print(f"🚀 بدء المعالجة في المجلد: {input_folder}")

        processed_count = 0
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                img_path = os.path.join(input_folder, filename)
                
                with Image.open(img_path) as base_image:
                    base_image = base_image.convert("RGBA")
                    width, height = base_image.size

                    # تغيير حجم الشعار ليتناسب مع الصورة
                    wm_width = int(width * LOGO_SIZE_RATIO)
                    aspect_ratio = watermark.width / watermark.height
                    wm_height = int(wm_width / aspect_ratio)
                    wm_resized = watermark.resize((wm_width, wm_height), Image.Resampling.LANCZOS)

                    # تحديد مكان الشعار (أسفل يمين)
                    position = (width - wm_width - PADDING, height - wm_height - PADDING)

                    # دمج الصور
                    transparent = Image.new('RGBA', (width, height), (0,0,0,0))
                    transparent.paste(base_image, (0,0))
                    transparent.paste(wm_resized, position, mask=wm_resized)
                    
                    # الحفظ
                    final_path = os.path.join(output_folder, filename)
                    transparent.convert("RGB").save(final_path, quality=95)
                    print(f"✅ تم الختم: {filename}")
                    processed_count += 1

        print(f"\n🎉 اكتملت العملية! تم حفظ {processed_count} صورة في المجلد: watermarked_images")
        
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    print("=== أداة حماية الأصول HYPE NET ===")
    folder = input("أدخل مسار مجلد الصور: ").strip().strip('"')
    logo = input("أدخل مسار صورة الشعار (Logo): ").strip().strip('"')
    
    if os.path.exists(folder) and os.path.exists(logo):
        add_watermark(folder, logo)
    else:
        print("❌ المسارات غير صحيحة.")
    
    input("\nاضغط Enter للخروج...")