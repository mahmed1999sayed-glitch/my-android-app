[app]
# اسم التطبيق اللي هيظهر تحت الأيقونة على الماشة
title = Abo 7ama6a Survey Volume Pro

# اسم الحزمة (اكتبه بحروف صغيرة وبدون مسافات)
package.name = surveyvolumepro
package.domain = org.abuhamada

# مكان الكود (النقطة تعني الفولدر الحالي)
source.dir = .

# امتدادات الملفات اللي التطبيق محتاجها
source.include_exts = py,png,jpg,kv,atlas

# إصدار التطبيق
version = 1.0

# المكتبات البرمجية اللي التطبيق محتاجها عشان يشتغل
requirements = python3,kivy

# اتجاه الشاشة (رأسي فقط تليق بالموبايل)
orientation = portrait

fullscreen = 0

# معمارية المعالجات (arm64-v8a هي الأساسية لمعظم موبايلات الأندرويد الحديثة)
android.archs = arm64-v8a

# طلب صلاحيات الوصول لذاكرة الموبايل وقراءة الملفات (مهمة جداً لزرار Choose File)
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# اسم صورة الأيقونة اللي عملناها سوا
icon.filename = logo.png

[buildozer]
log_level = 2
warn_on_root = 1