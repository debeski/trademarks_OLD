from django.core.management.base import BaseCommand
from documents.models import Country, Government, ComType, DocType, DecreeCategory

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

Governments = [
    'اللجنة الشعبية العامة',
    'الحكومة الليبية الانتقالية',
    'حكومة الإنقاذ الوطني',
    'حكومة الوفاق الوطني',
    'الحكومة الليبية المؤقتة',
    'حكومة الاستقرار الوطني',
    'حكومة الوحدة الوطنية',
]

ComTypes = [
    'تجارية',
    'صناعية',
    'صناعية - تجارية'
]

DocTypes = [
    'قرار',
    'نموذج',
    'لائحة'
]

DecreeCategories = [
    ('1', 'الفئة الاولى'),
    ('2', 'الفئة الثانية'),
    ('3', 'الفئة الثالثة'),
    ('4', 'الفئة الرابعة'),
    ('5', 'الفئة الخامسة'),
    ('6', 'الفئة السادسة'),
    ('7', 'الفئة السابعة'),
    ('8', 'الفئة الثامنة'),
    ('9', 'الفئة التاسعة'),
    ('10', 'الفئة العاشرة'),
    ('11', 'الفئة الحادية عشر'),
    ('12', 'الفئة الثانية عشر'),
    ('13', 'الفئة الثالثة عشر'),
    ('14', 'الفئة الرابعة عشر'),
    ('15', 'الفئة الخامسة عشر'),
    ('16', 'الفئة السادسة عشر'),
    ('17', 'الفئة السابعة عشر'),
    ('18', 'الفئة الثامنة عشر'),
    ('19', 'الفئة التاسعة عشر'),
    ('20', 'الفئة العشرون'),
    ('21', 'الفئة الواحد والعشرون'),
    ('22', 'الفئة الثانية والعشرون'),
    ('23', 'الفئة الثالثة والعشرون'),
    ('24', 'الفئة الرابعة والعشرون'),
    ('25', 'الفئة الخامسة والعشرون'),
    ('26', 'الفئة السادسة والعشرون'),
    ('27', 'الفئة السابعة والعشرون'),
    ('28', 'الفئة الثامنة والعشرون'),
    ('29', 'الفئة التاسعة والعشرون'),
    ('30', 'الفئة الثلاثون'),
    ('31', 'الفئة الحادية والثلاثون'),
    ('32', 'الفئة الثانية والثلاثون'),
    ('33', 'الفئة الثالثة والثلاثون'),
    ('34', 'الفئة الرابعة والثلاثون'),
    ('35', 'الفئة الخامسة والثلاثون'),
    ('36', 'الفئة السادسة والثلاثون'),
    ('37', 'الفئة السابعة والثلاثون'),
    ('38', 'الفئة الثامنة والثلاثون'),
    ('39', 'الفئة التاسعة والثلاثون'),
    ('40', 'الفئة الاربعون'),
    ('41', 'الفئة الواحد والاربعون'),
    ('42', 'الفئة الثانية والاربعون'),
    ('43', 'الفئة الثالثة والاربعون'),
    ('44', 'الفئة الرابعة والاربعون'),
    ('45', 'الفئة الخامسة والاربعون'),
]


class Command(BaseCommand):
    help = 'Populates the Country, ComType, and DocType tables with predefined lists'

    def handle(self, *args, **kwargs):
        # Populate Countries
        for en_name, ar_name in Countries:
            if not Country.objects.filter(ar_name=ar_name).exists():
                country = Country(ar_name=ar_name, en_name=en_name)
                country.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully added Country: {ar_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Country {ar_name} already exists'))

        # Populate ComTypes
        for name in Governments:
            if not Government.objects.filter(name=name).exists():
                government = Government(name=name)
                government.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully added Government: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Government {name} already exists'))

        # Populate ComTypes
        for name in ComTypes:
            if not ComType.objects.filter(name=name).exists():
                com_type = ComType(name=name)
                com_type.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully added ComType: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'ComType {name} already exists'))

        # Populate DocTypes
        for name in DocTypes:
            if not DocType.objects.filter(name=name).exists():
                doc_type = DocType(name=name)
                doc_type.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully added DocType: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'DocType {name} already exists'))

        # Populate DecreeCategories
        for number, name in DecreeCategories:
            if not DecreeCategory.objects.filter(number=number).exists():
                category = DecreeCategory(number=number, name=name)
                category.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully added DecreeCategory: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'DecreeCategory {name} already exists'))
