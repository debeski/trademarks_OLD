# Imports:
##########
from django.db import models
import uuid
import os
import json
from django.http import JsonResponse
from django.views import View
from datetime import datetime, time
import random
import string

# Temporary Lists:
##################
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

ComTypes = [
    ('commercial', 'تجارية'),
    ('industrial', 'صناعية'),
    ('both', 'صناعية - تجارية')
]

DocTypes = [
        ('decree', 'قرار'),
        ('form', 'نموذج'),
        ('list', 'لائحة')
]


# Helper Functions:
###################
def generate_random_filename(instance, filename):
    """Generate a random filename with the same extension as the uploaded file."""
    # Get the file extension
    file_name, file_extension = os.path.splitext(filename)
    
    # Generate a random filename with the same extension
    random_filename = f"{uuid.uuid4().hex}{file_extension}"
    
    # Get the model name and format the upload path
    model_name = instance.__class__.__name__.lower()
    
    # Return the full path where the file will be uploaded
    return f'{model_name}/{random_filename}'

def default_created_at():
    today = datetime.today().date()
    return datetime.combine(today, time(15, 0))

def generate_unique_code():
    # Generate a 13-digit random number
    return ''.join(random.choices(string.digits, k=13))

# def generate_random_filename(instance, filename):
#     """Generate a random filename for uploaded files."""
#     random_filename = f"{uuid.uuid4().hex}.pdf"
#     model_name = instance.__class__.__name__.lower()
#     return f'{model_name}/{random_filename}'

# def generate_random_filename_img(instance, filename):
#     """Generate a random filename for uploaded files."""
#     random_filename = f"{uuid.uuid4().hex}.jpg"
#     model_name = instance.__class__.__name__.lower()
#     return f'{model_name}/{random_filename}'

# def get_pdf_upload_path(instance, filename):
#     """Get the upload path for PDF files."""
#     return f'pdfs/{generate_random_filename(instance, filename)}'

# def get_attach_upload_path(instance, filename):
#     """Get the upload path for attachment files."""
#     return f'attach/{generate_random_filename(instance, filename)}'

# def get_img_upload_path(instance, filename):
#     """Get the upload path for IMG files."""
#     return f'item_img/{generate_random_filename_img(instance, filename)}'


# Section Models:
#################
class Country(models.Model):
    """Model representing a government entity."""
    en_name = models.CharField(max_length=255, unique=True, verbose_name="الاسم بالانجليزية")
    ar_name = models.CharField(max_length=255, unique=True, verbose_name="الاسم بالعربية")

    class Meta:
        verbose_name = "دولة"
        verbose_name_plural = "الدول"

    def __str__(self):
        return self.en_name

    @classmethod
    def get_table_class(cls):
        return 'documents.tables.CountryTable'

    @classmethod
    def get_filter_class(cls):
        return 'documents.filters.CountryFilter'

    @classmethod
    def get_form_class(cls):
        return 'documents.forms.CountryForm'

class Government(models.Model):
    """Model representing a government entity."""
    name = models.CharField(max_length=255, unique=True, verbose_name="الاسم")
        
    class Meta:
        verbose_name = "حكومة"
        verbose_name_plural = "الحكومات"
        
    def __str__(self):
        return self.name

    @classmethod
    def get_table_class(cls):
        return 'documents.tables.GovernmentTable'

    @classmethod
    def get_filter_class(cls):
        return 'documents.filters.GovernmentFilter'

    @classmethod
    def get_form_class(cls):
        return 'documents.forms.GovernmentForm'

class ComType(models.Model):
    """Model representing a government entity."""
    name = models.CharField(max_length=255, unique=True, verbose_name="الاسم")

    class Meta:
        verbose_name = "نوع شركة"
        verbose_name_plural = "انواع الشركات"

    def __str__(self):
        return self.name

    @classmethod
    def get_table_class(cls):
        return 'documents.tables.ComTypeTable'

    @classmethod
    def get_filter_class(cls):
        return 'documents.filters.ComTypeFilter'

    @classmethod
    def get_form_class(cls):
        return 'documents.forms.ComTypeForm'

class DocType(models.Model):
    """Model representing a government entity."""
    name = models.CharField(max_length=255, unique=True, verbose_name="الاسم")

    class Meta:
        verbose_name = "نوع مستند"
        verbose_name_plural = "انواع المستندات"

    def __str__(self):
        return self.name

    @classmethod
    def get_table_class(cls):
        return 'documents.tables.DocTypeTable'

    @classmethod
    def get_filter_class(cls):
        return 'documents.filters.DocTypeFilter'

    @classmethod
    def get_form_class(cls):
        return 'documents.forms.DocTypeForm'

class DecreeCategory(models.Model):
    """Model representing a government entity."""
    number = models.IntegerField(unique=True, verbose_name="رقم الفئة")
    name = models.CharField(max_length=255, unique=True, verbose_name="اسم الفئة")

    class Meta:
        verbose_name = "الفئة"
        verbose_name_plural = "الفئات"

    def __str__(self):
        return self.name

    @classmethod
    def get_table_class(cls):
        return 'documents.tables.DecreeCategoryTable'

    @classmethod
    def get_filter_class(cls):
        return 'documents.filters.DecreeCategoryFilter'

    @classmethod
    def get_form_class(cls):
        return 'documents.forms.DecreeCategoryForm'
    
    
# Document Models:
##################
class Decree(models.Model):
    """Model representing a minister decree."""
    number = models.IntegerField(blank=False, null=False, verbose_name="رقم القرار")
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
    number_applied = models.IntegerField(blank=False, null=False, verbose_name="رقم القيد")
    
    ar_brand = models.CharField(max_length=255, blank=False, verbose_name="العلامة (عربي)")
    en_brand = models.CharField(max_length=255, blank=False, verbose_name="العلامة (انجليزي)")
    category = models.IntegerField(blank=True, verbose_name="الفئة")
    
    pdf_file = models.FileField(upload_to=generate_random_filename, blank=True, verbose_name="ملف القرار")
    attach = models.FileField(upload_to=generate_random_filename, blank=True, verbose_name="المرفقات")
    notes = models.TextField(max_length=999, blank=True, verbose_name="ملاحظات")
    
    is_published = models.BooleanField(default=False, verbose_name="تم اشهاره مبدئيا")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return str(self.number)
    
    @property
    def get_model_name(self):
        return "قرارات"

class Publication(models.Model):
    """Model representing a minister decree."""
    year = models.IntegerField(null=True, blank=True)
    number = models.IntegerField(blank=False, null=False, verbose_name="رقم التسجيل")
    decree = models.IntegerField(blank=False, null=False, verbose_name="رقم القرار")
    
    applicant = models.CharField(max_length=255, blank=False, verbose_name="طالب التسجيل")
    owner = models.CharField(max_length=255, blank=False, verbose_name="مالك العلامة")
    country = models.CharField(max_length=50, choices=Countries, verbose_name="الدولة")
    address = models.CharField(max_length=255, blank=False, verbose_name="العنوان")
    date_applied = models.DateField(blank=False, verbose_name="تاريخ التقديم")
    
    ar_brand = models.CharField(max_length=255, blank=False, verbose_name="العلامة (عربي)")
    en_brand = models.CharField(max_length=255, blank=False, verbose_name="العلامة (انجليزي)")
    category = models.IntegerField(blank=True, verbose_name="الفئة")
    
    img_file = models.ImageField(upload_to=generate_random_filename, blank=True, verbose_name="الصورة")
    attach = models.FileField(upload_to=generate_random_filename, blank=True, verbose_name="المرفقات")
    e_number = models.IntegerField(blank=False, null=False, verbose_name="رقم النشرية")
    status = models.CharField(max_length=50, choices=[
        ('initial', 'نشر مبدئي'),
        ('conflict', 'متنازع عليه'),
        ('final', 'نشر نهائي')
    ], verbose_name="حالة التسجيل")
    
    is_hidden = models.BooleanField(default=False, verbose_name="مخفي")
    notes = models.TextField(max_length=999, blank=True, verbose_name="ملاحظات")
    
    objection_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الاعتراض")
    is_objected = models.BooleanField(default=False, verbose_name="تم الاعتراض عليه")
    
    created_at = models.DateTimeField(default=default_created_at, verbose_name="تاريخ النشر")
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return str(self.number)
    
    @property
    def get_model_name(self):
        return "اشهارات"

class Objection(models.Model):
    """Model representing a minister decree."""
    number = models.IntegerField(unique=True, blank=False, null=False, verbose_name="رقم المعارضة")
    pub = models.ForeignKey(Publication, on_delete=models.PROTECT, verbose_name="الاشهار")
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name="اسم ولقب مقدم الشكوى")
    job = models.CharField(max_length=24, blank=False, null=False, verbose_name="المهنة")
    nationality = models.CharField(max_length=50, choices=Countries, verbose_name="الجنسية")
    address = models.CharField(max_length=255, blank=False, verbose_name="محل الاقامة")
    phone = models.CharField(max_length=10, blank=False, verbose_name="رقم الهاتف")
    
    com_name = models.CharField(max_length=255, blank=False, verbose_name="اسم الشركة المقدمة للشكوى")
    com_job = models.CharField(max_length=24, choices=ComTypes, verbose_name="غرض الشركة")
    com_address = models.CharField(max_length=255, blank=False, verbose_name="عنوان الشركة")
    com_og_address = models.CharField(max_length=255, blank=False, verbose_name="عنوان المقر الرئيسي للشركة")
    com_mail_address = models.CharField(max_length=255, blank=False, verbose_name="عنوان البريد الرئيسي لاستلام المكاتبات المتعلقة بالمعارضة")
    
    status = models.CharField(max_length=50, choices=[
        ('pending', 'معلق'),
        ('accepted', 'موافقة'),
        ('rejected', 'رفض')
    ], verbose_name="حالة الاعتراض")
    reason = models.CharField(max_length=100, verbose_name="اسباب الرفض", blank=True)
    pdf_file = models.FileField(upload_to=generate_random_filename, blank=True, verbose_name="ملف الاعتراض")
    notes = models.TextField(max_length=999, blank=True, verbose_name="تفاصيل")
    
    is_paid = models.BooleanField(default=False, verbose_name="تم دفع الرسوم")
    unique_code = models.CharField(max_length=13, unique=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاعتراض")
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.number:  # Only assign if not already set
            last_objection = Objection.objects.order_by('-number').first()
            if last_objection:
                self.number = last_objection.number + 1
            else:
                self.number = 1  # Start from 1 if there are no objections

        # Generate a unique code only if the object is being created (not updated)
        if not self.unique_code:
            self.unique_code = generate_unique_code()
            # Ensure the code is unique
            while Objection.objects.filter(unique_code=self.unique_code).exists():
                self.unique_code = generate_unique_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.number)
    
    @property
    def get_model_name(self):
        return "اعتراضات"
    
    @classmethod
    def get_table_class(cls):
        return 'documents.tables.ObjectionTable'

    @classmethod
    def get_filter_class(cls):
        return 'documents.filters.ObjectionFilter'

    @classmethod
    def get_form_class(cls):
        return 'documents.forms.ObjectionForm'

class FormPlus(models.Model):
    """Ambiguous Model representing a report of some sort."""
    number = models.CharField(max_length=20, blank=True, null=True, verbose_name="الرقم")
    date = models.DateField(blank=True, verbose_name="التاريخ")
    government = models.ForeignKey(Government, on_delete=models.PROTECT, verbose_name="الحكومة")
    type = models.CharField(max_length=50, choices=DocTypes, verbose_name="النوع")
    title = models.CharField(max_length=255, blank=False, verbose_name="العنوان")
    keywords = models.TextField(max_length=999, blank=True, verbose_name="التفاصيل")
    pdf_file = models.FileField(upload_to=generate_random_filename, blank=True)
    word_file = models.FileField(upload_to=generate_random_filename, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    @property
    def get_model_name(self):
        return "نماذج وقرارات"


