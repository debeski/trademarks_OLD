# Generated by Django 5.1.4 on 2025-02-06 10:49

import django.db.models.deletion
import documents.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('is_attached', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Decree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, verbose_name='رقم القرار')),
                ('date', models.DateField(verbose_name='تاريخ القرار')),
                ('status', models.CharField(choices=[('accepted', 'قبول'), ('rejected', 'رفض'), ('withdraw', 'سحب'), ('canceled', 'الغاء')], max_length=50, verbose_name='حالة القرار')),
                ('applicant', models.CharField(max_length=255, verbose_name='مقدم الطلب')),
                ('company', models.CharField(max_length=255, verbose_name='صاحب العلامة')),
                ('country', models.CharField(choices=[('Afghanistan', 'أفغانستان'), ('Albania', 'ألبانيا'), ('Algeria', 'الجزائر'), ('Andorra', 'أندورا'), ('Angola', 'أنغولا'), ('Antigua and Barbuda', 'أنتيغوا وباربودا'), ('Argentina', 'الأرجنتين'), ('Armenia', 'أرمينيا'), ('Australia', 'أستراليا'), ('Austria', 'النمسا'), ('Azerbaijan', 'أذربيجان'), ('Bahamas', 'باهاماس'), ('Bahrain', 'البحرين'), ('Bangladesh', 'بنغلاديش'), ('Barbados', 'بربادوس'), ('Belarus', 'بيلاروسيا'), ('Belgium', 'بلجيكا'), ('Belize', 'بليز'), ('Benin', 'بنين'), ('Bhutan', 'بوتان'), ('Bolivia', 'بوليفيا'), ('Bosnia and Herzegovina', 'البوسنة والهرسك'), ('Botswana', 'بوتسوانا'), ('Brazil', 'البرازيل'), ('Brunei', 'بروناي'), ('Bulgaria', 'بلغاريا'), ('Burkina Faso', 'بوركينا فاسو'), ('Burundi', 'بوروندي'), ('Cabo Verde', 'كابو فيردي'), ('Cambodia', 'كمبوديا'), ('Cameroon', 'الكاميرون'), ('Canada', 'كندا'), ('Central African Republic', 'جمهورية أفريقيا الوسطى'), ('Chad', 'تشاد'), ('Chile', 'تشيلي'), ('China', 'الصين'), ('Colombia', 'كولومبيا'), ('Comoros', 'جزر القمر'), ('Congo (Congo-Brazzaville)', 'جمهورية الكونغو'), ('Costa Rica', 'كوستاريكا'), ('Croatia', 'كرواتيا'), ('Cuba', 'كوبا'), ('Cyprus', 'قبرص'), ('Czechia (Czech Republic)', 'تشيكيا'), ('Denmark', 'الدنمارك'), ('Djibouti', 'جيبوتي'), ('Dominica', 'دومينيكا'), ('Dominican Republic', 'جمهورية الدومينيكان'), ('Ecuador', 'الإكوادور'), ('Egypt', 'مصر'), ('El Salvador', 'السلفادور'), ('Equatorial Guinea', 'غينيا الاستوائية'), ('Eritrea', 'إريتريا'), ('Estonia', 'إستونيا'), ('Eswatini', 'إسواتيني'), ('Ethiopia', 'إثيوبيا'), ('Fiji', 'فيجي'), ('Finland', 'فنلندا'), ('France', 'فرنسا'), ('Gabon', 'الغابون'), ('Gambia', 'غامبيا'), ('Georgia', 'جورجيا'), ('Germany', 'ألمانيا'), ('Ghana', 'غانا'), ('Greece', 'اليونان'), ('Grenada', 'غرينادا'), ('Guatemala', 'غواتيمالا'), ('Guinea', 'غينيا'), ('Guinea-Bissau', 'غينيا بيساو'), ('Guyana', 'غيانا'), ('Haiti', 'هايتي'), ('Honduras', 'هندوراس'), ('Hungary', 'المجر'), ('Iceland', 'آيسلندا'), ('India', 'الهند'), ('Indonesia', 'إندونيسيا'), ('Iran', 'إيران'), ('Iraq', 'العراق'), ('Ireland', 'أيرلندا'), ('Italy', 'إيطاليا'), ('Jamaica', 'جامايكا'), ('Japan', 'اليابان'), ('Jordan', 'الأردن'), ('Kazakhstan', 'كازاخستان'), ('Kenya', 'كينيا'), ('Kiribati', 'كيريباتي'), ('Kuwait', 'الكويت'), ('Kyrgyzstan', 'قيرغيزستان'), ('Laos', 'لاوس'), ('Latvia', 'لاتفيا'), ('Lebanon', 'لبنان'), ('Lesotho', 'ليسوتو'), ('Liberia', 'ليبيريا'), ('Libya', 'ليبيا'), ('Liechtenstein', 'ليختنشتاين'), ('Lithuania', 'ليتوانيا'), ('Luxembourg', 'لوكسمبورغ'), ('Madagascar', 'مدغشقر'), ('Malawi', 'مالاوي'), ('Malaysia', 'ماليزيا'), ('Maldives', 'جزر المالديف'), ('Mali', 'مالي'), ('Malta', 'مالطا'), ('Marshall Islands', 'جزر مارشال'), ('Mauritania', 'موريتانيا'), ('Mauritius', 'موريشيوس'), ('Mexico', 'المكسيك'), ('Micronesia', 'ميكرونيسيا'), ('Moldova', 'مولدوفا'), ('Monaco', 'موناكو'), ('Mongolia', 'منغوليا'), ('Montenegro', 'الجبل الأسود'), ('Morocco', 'المغرب'), ('Mozambique', 'موزمبيق'), ('Myanmar (Burma)', 'ميانمار'), ('Namibia', 'ناميبيا'), ('Nauru', 'ناورو'), ('Nepal', 'نيبال'), ('Netherlands', 'هولندا'), ('New Zealand', 'نيوزيلندا'), ('Nicaragua', 'نيكاراغوا'), ('Niger', 'النيجر'), ('Nigeria', 'نيجيريا'), ('North Korea', 'كوريا الشمالية'), ('North Macedonia', 'مقدونيا الشمالية'), ('Norway', 'النرويج'), ('Oman', 'عُمان'), ('Pakistan', 'باكستان'), ('Palau', 'بالاو'), ('Palestine', 'فلسطين'), ('Panama', 'بنما'), ('Papua New Guinea', 'بابوا غينيا الجديدة'), ('Paraguay', 'باراغواي'), ('Peru', 'بيرو'), ('Philippines', 'الفلبين'), ('Poland', 'بولندا'), ('Portugal', 'البرتغال'), ('Qatar', 'قطر'), ('Romania', 'رومانيا'), ('Russia', 'روسيا'), ('Rwanda', 'رواندا'), ('Saint Kitts and Nevis', 'سانت كيتس ونيفيس'), ('Saint Lucia', 'سانت لوسيا'), ('Saint Vincent and the Grenadines', 'سانت فنسنت والغرينادين'), ('Samoa', 'ساموا'), ('San Marino', 'سان مارينو'), ('Sao Tome and Principe', 'ساو تومي وبرينسيبي'), ('Saudi Arabia', 'المملكة العربية السعودية'), ('Senegal', 'السنغال'), ('Serbia', 'صربيا'), ('Seychelles', 'سيشل'), ('Sierra Leone', 'سيراليون'), ('Singapore', 'سنغافورة'), ('Slovakia', 'سلوفاكيا'), ('Slovenia', 'سلوفينيا'), ('Solomon Islands', 'جزر سليمان'), ('Somalia', 'الصومال'), ('South Africa', 'جنوب أفريقيا'), ('South Korea', 'كوريا الجنوبية'), ('South Sudan', 'جنوب السودان'), ('Spain', 'إسبانيا'), ('Sri Lanka', 'سريلانكا'), ('Sudan', 'السودان'), ('Suriname', 'سورينام'), ('Sweden', 'السويد'), ('Switzerland', 'سويسرا'), ('Syria', 'سوريا'), ('Tajikistan', 'طاجيكستان'), ('Tanzania', 'تنزانيا'), ('Thailand', 'تايلاند'), ('Timor-Leste', 'تيمور الشرقية'), ('Togo', 'توغو'), ('Tonga', 'تونغا'), ('Trinidad and Tobago', 'ترينيداد وتوباغو'), ('Tunisia', 'تونس'), ('Turkey', 'تركيا'), ('Turkmenistan', 'تركمانستان'), ('Tuvalu', 'توفالو'), ('Uganda', 'أوغندا'), ('Ukraine', 'أوكرانيا'), ('United Arab Emirates', 'الإمارات العربية المتحدة'), ('United Kingdom', 'المملكة المتحدة'), ('United States of America', 'الولايات المتحدة الأمريكية'), ('Uruguay', 'أوروغواي'), ('Uzbekistan', 'أوزبكستان'), ('Vanuatu', 'فانواتو'), ('Vatican City', 'الفاتيكان'), ('Venezuela', 'فنزويلا'), ('Vietnam', 'فيتنام'), ('Yemen', 'اليمن'), ('Zambia', 'زامبيا'), ('Zimbabwe', 'زيمبابوي')], max_length=50, verbose_name='الدولة')),
                ('date_applied', models.DateField(verbose_name='تاريخ التقديم')),
                ('number_applied', models.CharField(max_length=10, verbose_name='رقم القيد')),
                ('ar_brand', models.CharField(max_length=255, verbose_name='العلامة التجارية عربي')),
                ('en_brand', models.CharField(max_length=255, verbose_name='العلامة التجارية انجليزي')),
                ('category', models.CharField(blank=True, max_length=255, verbose_name='الفئة')),
                ('pdf_file', models.FileField(blank=True, upload_to=documents.models.get_pdf_upload_path, verbose_name='ملف القرار')),
                ('attach', models.FileField(blank=True, upload_to=documents.models.get_attach_upload_path, verbose_name='المرفقات')),
                ('notes', models.TextField(blank=True, max_length=999, verbose_name='ملاحظات')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Government',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=20, null=True)),
                ('date', models.DateField(blank=True)),
                ('title', models.CharField(max_length=255)),
                ('keywords', models.TextField(blank=True, max_length=999)),
                ('pdf_file', models.FileField(blank=True, upload_to=documents.models.get_pdf_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Incoming',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('orig_number', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('orig_date', models.DateField(blank=True)),
                ('title', models.CharField(max_length=255)),
                ('keywords', models.TextField(blank=True, max_length=999)),
                ('pdf_file', models.FileField(blank=True, upload_to=documents.models.get_pdf_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('dept_from', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incoming_affiliates', to='documents.affiliate')),
                ('dept_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incoming_departments', to='documents.department')),
            ],
        ),
        migrations.CreateModel(
            name='Internal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=10, null=True)),
                ('date', models.DateField(blank=True)),
                ('title', models.CharField(max_length=255)),
                ('keywords', models.TextField(blank=True, max_length=999)),
                ('pdf_file', models.FileField(blank=True, upload_to=documents.models.get_pdf_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('dept_from', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='internal_departments_from', to='documents.department')),
                ('dept_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='internal_departments_to', to='documents.department')),
            ],
        ),
        migrations.CreateModel(
            name='Minister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('government', models.ManyToManyField(related_name='minister_on_duty', to='documents.government')),
            ],
        ),
        migrations.CreateModel(
            name='Outgoing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=255)),
                ('keywords', models.TextField(blank=True, max_length=999)),
                ('pdf_file', models.FileField(blank=True, upload_to=documents.models.get_pdf_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('dept_from', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='outgoing_departments', to='documents.department')),
                ('dept_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='outgoing_affiliates', to='documents.affiliate')),
            ],
        ),
    ]
