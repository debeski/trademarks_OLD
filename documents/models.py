from django.db import models
import uuid
import json
from django.http import JsonResponse
from django.views import View


Countries = [
    ('Afghanistan', 'أفغانستان'),
    ('Albania', 'ألبانيا'),
    ('Algeria', 'الجزائر'),
    ('Andorra', 'أندورا'),
    ('Angola', 'أنغولا'),
    ('Antigua and Barbuda', 'أنتيغوا وباربودا'),
    ('Argentina', 'الأرجنتين'),
    ('Armenia', 'أرمينيا'),
    ('Australia', 'أستراليا'),
    ('Austria', 'النمسا'),
    ('Azerbaijan', 'أذربيجان'),
    ('Bahamas', 'باهاماس'),
    ('Bahrain', 'البحرين'),
    ('Bangladesh', 'بنغلاديش'),
    ('Barbados', 'بربادوس'),
    ('Belarus', 'بيلاروسيا'),
    ('Belgium', 'بلجيكا'),
    ('Belize', 'بليز'),
    ('Benin', 'بنين'),
    ('Bhutan', 'بوتان'),
    ('Bolivia', 'بوليفيا'),
    ('Bosnia and Herzegovina', 'البوسنة والهرسك'),
    ('Botswana', 'بوتسوانا'),
    ('Brazil', 'البرازيل'),
    ('Brunei', 'بروناي'),
    ('Bulgaria', 'بلغاريا'),
    ('Burkina Faso', 'بوركينا فاسو'),
    ('Burundi', 'بوروندي'),
    ('Cabo Verde', 'كابو فيردي'),
    ('Cambodia', 'كمبوديا'),
    ('Cameroon', 'الكاميرون'),
    ('Canada', 'كندا'),
    ('Central African Republic', 'جمهورية أفريقيا الوسطى'),
    ('Chad', 'تشاد'),
    ('Chile', 'تشيلي'),
    ('China', 'الصين'),
    ('Colombia', 'كولومبيا'),
    ('Comoros', 'جزر القمر'),
    ('Congo (Congo-Brazzaville)', 'جمهورية الكونغو'),
    ('Costa Rica', 'كوستاريكا'),
    ('Croatia', 'كرواتيا'),
    ('Cuba', 'كوبا'),
    ('Cyprus', 'قبرص'),
    ('Czechia (Czech Republic)', 'تشيكيا'),
    ('Denmark', 'الدنمارك'),
    ('Djibouti', 'جيبوتي'),
    ('Dominica', 'دومينيكا'),
    ('Dominican Republic', 'جمهورية الدومينيكان'),
    ('Ecuador', 'الإكوادور'),
    ('Egypt', 'مصر'),
    ('El Salvador', 'السلفادور'),
    ('Equatorial Guinea', 'غينيا الاستوائية'),
    ('Eritrea', 'إريتريا'),
    ('Estonia', 'إستونيا'),
    ('Eswatini', 'إسواتيني'),
    ('Ethiopia', 'إثيوبيا'),
    ('Fiji', 'فيجي'),
    ('Finland', 'فنلندا'),
    ('France', 'فرنسا'),
    ('Gabon', 'الغابون'),
    ('Gambia', 'غامبيا'),
    ('Georgia', 'جورجيا'),
    ('Germany', 'ألمانيا'),
    ('Ghana', 'غانا'),
    ('Greece', 'اليونان'),
    ('Grenada', 'غرينادا'),
    ('Guatemala', 'غواتيمالا'),
    ('Guinea', 'غينيا'),
    ('Guinea-Bissau', 'غينيا بيساو'),
    ('Guyana', 'غيانا'),
    ('Haiti', 'هايتي'),
    ('Honduras', 'هندوراس'),
    ('Hungary', 'المجر'),
    ('Iceland', 'آيسلندا'),
    ('India', 'الهند'),
    ('Indonesia', 'إندونيسيا'),
    ('Iran', 'إيران'),
    ('Iraq', 'العراق'),
    ('Ireland', 'أيرلندا'),
    ('Italy', 'إيطاليا'),
    ('Jamaica', 'جامايكا'),
    ('Japan', 'اليابان'),
    ('Jordan', 'الأردن'),
    ('Kazakhstan', 'كازاخستان'),
    ('Kenya', 'كينيا'),
    ('Kiribati', 'كيريباتي'),
    ('Kuwait', 'الكويت'),
    ('Kyrgyzstan', 'قيرغيزستان'),
    ('Laos', 'لاوس'),
    ('Latvia', 'لاتفيا'),
    ('Lebanon', 'لبنان'),
    ('Lesotho', 'ليسوتو'),
    ('Liberia', 'ليبيريا'),
    ('Libya', 'ليبيا'),
    ('Liechtenstein', 'ليختنشتاين'),
    ('Lithuania', 'ليتوانيا'),
    ('Luxembourg', 'لوكسمبورغ'),
    ('Madagascar', 'مدغشقر'),
    ('Malawi', 'مالاوي'),
    ('Malaysia', 'ماليزيا'),
    ('Maldives', 'جزر المالديف'),
    ('Mali', 'مالي'),
    ('Malta', 'مالطا'),
    ('Marshall Islands', 'جزر مارشال'),
    ('Mauritania', 'موريتانيا'),
    ('Mauritius', 'موريشيوس'),
    ('Mexico', 'المكسيك'),
    ('Micronesia', 'ميكرونيسيا'),
    ('Moldova', 'مولدوفا'),
    ('Monaco', 'موناكو'),
    ('Mongolia', 'منغوليا'),
    ('Montenegro', 'الجبل الأسود'),
    ('Morocco', 'المغرب'),
    ('Mozambique', 'موزمبيق'),
    ('Myanmar (Burma)', 'ميانمار'),
    ('Namibia', 'ناميبيا'),
    ('Nauru', 'ناورو'),
    ('Nepal', 'نيبال'),
    ('Netherlands', 'هولندا'),
    ('New Zealand', 'نيوزيلندا'),
    ('Nicaragua', 'نيكاراغوا'),
    ('Niger', 'النيجر'),
    ('Nigeria', 'نيجيريا'),
    ('North Korea', 'كوريا الشمالية'),
    ('North Macedonia', 'مقدونيا الشمالية'),
    ('Norway', 'النرويج'),
    ('Oman', 'عُمان'),
    ('Pakistan', 'باكستان'),
    ('Palau', 'بالاو'),
    ('Palestine', 'فلسطين'),
    ('Panama', 'بنما'),
    ('Papua New Guinea', 'بابوا غينيا الجديدة'),
    ('Paraguay', 'باراغواي'),
    ('Peru', 'بيرو'),
    ('Philippines', 'الفلبين'),
    ('Poland', 'بولندا'),
    ('Portugal', 'البرتغال'),
    ('Qatar', 'قطر'),
    ('Romania', 'رومانيا'),
    ('Russia', 'روسيا'),
    ('Rwanda', 'رواندا'),
    ('Saint Kitts and Nevis', 'سانت كيتس ونيفيس'),
    ('Saint Lucia', 'سانت لوسيا'),
    ('Saint Vincent and the Grenadines', 'سانت فنسنت والغرينادين'),
    ('Samoa', 'ساموا'),
    ('San Marino', 'سان مارينو'),
    ('Sao Tome and Principe', 'ساو تومي وبرينسيبي'),
    ('Saudi Arabia', 'المملكة العربية السعودية'),
    ('Senegal', 'السنغال'),
    ('Serbia', 'صربيا'),
    ('Seychelles', 'سيشل'),
    ('Sierra Leone', 'سيراليون'),
    ('Singapore', 'سنغافورة'),
    ('Slovakia', 'سلوفاكيا'),
    ('Slovenia', 'سلوفينيا'),
    ('Solomon Islands', 'جزر سليمان'),
    ('Somalia', 'الصومال'),
    ('South Africa', 'جنوب أفريقيا'),
    ('South Korea', 'كوريا الجنوبية'),
    ('South Sudan', 'جنوب السودان'),
    ('Spain', 'إسبانيا'),
    ('Sri Lanka', 'سريلانكا'),
    ('Sudan', 'السودان'),
    ('Suriname', 'سورينام'),
    ('Sweden', 'السويد'),
    ('Switzerland', 'سويسرا'),
    ('Syria', 'سوريا'),
    ('Tajikistan', 'طاجيكستان'),
    ('Tanzania', 'تنزانيا'),
    ('Thailand', 'تايلاند'),
    ('Timor-Leste', 'تيمور الشرقية'),
    ('Togo', 'توغو'),
    ('Tonga', 'تونغا'),
    ('Trinidad and Tobago', 'ترينيداد وتوباغو'),
    ('Tunisia', 'تونس'),
    ('Turkey', 'تركيا'),
    ('Turkmenistan', 'تركمانستان'),
    ('Tuvalu', 'توفالو'),
    ('Uganda', 'أوغندا'),
    ('Ukraine', 'أوكرانيا'),
    ('United Arab Emirates', 'الإمارات العربية المتحدة'),
    ('United Kingdom', 'المملكة المتحدة'),
    ('United States of America', 'الولايات المتحدة الأمريكية'),
    ('Uruguay', 'أوروغواي'),
    ('Uzbekistan', 'أوزبكستان'),
    ('Vanuatu', 'فانواتو'),
    ('Vatican City', 'الفاتيكان'),
    ('Venezuela', 'فنزويلا'),
    ('Vietnam', 'فيتنام'),
    ('Yemen', 'اليمن'),
    ('Zambia', 'زامبيا'),
    ('Zimbabwe', 'زيمبابوي'),
]


# PDF Files Naming Functions:
def generate_random_filename(instance, filename):
    """Generate a random filename for uploaded files."""
    random_filename = f"{uuid.uuid4().hex}.pdf"
    model_name = instance.__class__.__name__.lower()
    return f'{model_name}/{random_filename}'

def generate_random_filename_img(instance, filename):
    """Generate a random filename for uploaded files."""
    random_filename = f"{uuid.uuid4().hex}.jpg"
    model_name = instance.__class__.__name__.lower()
    return f'{model_name}/{random_filename}'

def get_pdf_upload_path(instance, filename):
    """Get the upload path for PDF files."""
    return f'pdfs/{generate_random_filename(instance, filename)}'

def get_attach_upload_path(instance, filename):
    """Get the upload path for attachment files."""
    return f'attach/{generate_random_filename(instance, filename)}'

def get_img_upload_path(instance, filename):
    """Get the upload path for IMG files."""
    return f'item_img/{generate_random_filename_img(instance, filename)}'

# # Section Models:
# class Department(models.Model):
#     """Model representing a department."""
#     name = models.CharField(max_length=255, unique=True)

#     def __str__(self):
#         return self.name

# class Affiliate(models.Model):
#     """Model representing an affiliate."""
#     name = models.CharField(max_length=255, unique=True)
#     is_attached = models.BooleanField(default=False)


#     def __str__(self):
#         return self.name

# class Government(models.Model):
#     """Model representing a government entity."""
#     name = models.CharField(max_length=255, unique=True)

#     def __str__(self):
#         return self.name

# class Minister(models.Model):
#     """Model representing a minister."""
#     name = models.CharField(max_length=255, unique=True)
#     government = models.ManyToManyField(Government, related_name='minister_on_duty')

#     def __str__(self):
#         return self.name


# Document Models:
class Decree(models.Model):
    """Model representing a minister decree."""
    number = models.CharField(max_length=10, blank=False, null=False, verbose_name="رقم القرار")
    date = models.DateField(blank=False, verbose_name="تاريخ القرار")
    status = models.CharField(max_length=50, choices=[
        ('accepted', 'قبول'),
        ('rejected', 'رفض'),
        ('withdraw', 'سحب'),
        ('canceled', 'الغاء')
    ], verbose_name="حالة القرار")
    applicant = models.CharField(max_length=255, blank=False, verbose_name="مقدم الطلب")
    company = models.CharField(max_length=255, blank=False, verbose_name="صاحب العلامة")
    country = models.CharField(max_length=50, choices=Countries, verbose_name="الدولة")
    date_applied = models.DateField(blank=False, verbose_name="تاريخ التقديم")
    number_applied = models.CharField(max_length=10, blank=False, null=False, verbose_name="رقم القيد")
    ar_brand = models.CharField(max_length=255, blank=False, verbose_name="العلامة (عربي)")
    en_brand = models.CharField(max_length=255, blank=False, verbose_name="العلامة (انجليزي)")
    category = models.CharField(max_length=255, blank=True, verbose_name="الفئة")
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True, verbose_name="ملف القرار")
    attach = models.FileField(upload_to=get_attach_upload_path, blank=True, verbose_name="المرفقات")
    notes = models.TextField(max_length=999, blank=True, verbose_name="ملاحظات")
    objection_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الاعتراض")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.number

    @property
    def get_model_name(self):
        return "قرارات"


class Publication(models.Model):
    """Model representing a minister decree."""
    year = models.IntegerField(null=True, blank=True)  # Add this field
    number = models.CharField(max_length=10, blank=False, null=False, verbose_name="رقم التسجيل")
    decree = models.CharField(max_length=10, blank=False, null=False, verbose_name="رقم القرار")

    applicant = models.CharField(max_length=255, blank=False, verbose_name="طالب التسجيل")
    owner = models.CharField(max_length=255, blank=False, verbose_name="مالك العلامة")
    country = models.CharField(max_length=50, choices=Countries, verbose_name="الدولة")
    address = models.CharField(max_length=255, blank=False, verbose_name="العنوان")
    date_applied = models.DateField(blank=False, verbose_name="تاريخ التقديم")
    ar_brand = models.CharField(max_length=255, blank=False, verbose_name="العلامة (عربي)")
    en_brand = models.CharField(max_length=255, blank=False, verbose_name="العلامة (انجليزي)")
    category = models.CharField(max_length=255, blank=True, verbose_name="الفئة")
    img_file = models.ImageField(upload_to=get_img_upload_path, blank=True, verbose_name="الصورة")
    attach = models.FileField(upload_to=get_attach_upload_path, blank=True, verbose_name="المرفقات")
    e_number = models.CharField(max_length=10, blank=False, null=False, verbose_name="رقم النشرية")
    status = models.CharField(max_length=50, choices=[
        ('initial', 'نشر مبدئي'),
        ('final', 'نشر نهائي'),
        ('conflict', 'متنازع عليه')
    ], verbose_name="حالة التسجيل")
    is_hidden = models.BooleanField(default=False, verbose_name="مخفي")
    notes = models.TextField(max_length=999, blank=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ النشر")
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.number
    
    @property
    def get_model_name(self):
        return "اشهارات"


# class Report(models.Model):
#     """Ambiguous Model representing a report of some sort."""
#     number = models.CharField(max_length=20, blank=True, null=True)
#     date = models.DateField(blank=True)
#     title = models.CharField(max_length=255, blank=False)
#     keywords = models.TextField(max_length=999, blank=True)
#     pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return self.title
    
#     @property
#     def get_model_name(self):
#         return "تقارير"

