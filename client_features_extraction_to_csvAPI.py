import requests
import os
import csv

# تحديد مسار الصورة التي سترسلها
image_path = "ImagesClient/moathFromClient.jpg"
image_name = os.path.basename(image_path).split(".")[0]  # احصل على اسم الصورة دون الامتداد

# إرسال الصورة إلى الخادم
url = "http://localhost:5000/upload"  # تأكد من تغيير الرابط وفقًا لمنفذ الخادم إذا تم تغييره
files = {"image": open(image_path, "rb")}
response = requests.post(url, files=files)

# تحقق من رمز الاستجابة
if response.status_code == 200:
    print("تم رفع الصورة واستخراج الميزات بنجاح.")




    # استخراج الميزات من الاستجابة
    features = response.text.strip()

    # حفظ الميزات في ملف CSV
    with open("ImagesClient/features_all.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(features.split(","))
        

else:
    print("حدث خطأ أثناء رفع الصورة واستخراج الميزات.")