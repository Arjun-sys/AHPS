# Generated by Django 3.0.3 on 2022-03-05 07:56

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='consultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultation_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=20)),
                ('amount', models.IntegerField(default=200)),
                ('payment_completed', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='diseaseinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diseasename', models.CharField(max_length=200)),
                ('no_of_symp', models.IntegerField()),
                ('symptomsname', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None)),
                ('confidence', models.DecimalField(decimal_places=2, max_digits=5)),
                ('consultdoctor', models.CharField(max_length=200)),
                ('consulthospital', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=400), size=None)),
                ('precaution', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('consulthospital1', models.CharField(max_length=200)),
                ('consulthospital2', models.CharField(max_length=200)),
                ('consulthospital3', models.CharField(max_length=200)),
                ('consulthospital4', models.CharField(max_length=200)),
                ('consulthospital5', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='doctor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_patient', models.BooleanField(default=False)),
                ('is_doctor', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('mobile_no', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=10)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='doc_pics')),
                ('registration_no', models.CharField(max_length=20)),
                ('year_of_registration', models.DateField()),
                ('qualification', models.CharField(max_length=20)),
                ('practicinghospital', models.CharField(max_length=200)),
                ('specialization', models.CharField(max_length=30)),
                ('start_time', models.CharField(max_length=10)),
                ('end_time', models.TimeField()),
                ('rating', models.IntegerField(default=0)),
                ('status', models.BooleanField(default=False)),
                ('paying', models.IntegerField(default=0)),
                ('bank', models.CharField(max_length=100)),
                ('accountno', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_patient', models.BooleanField(default=True)),
                ('is_doctor', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='pics/')),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('mobile_no', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=10)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='reportupload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(max_length=500)),
                ('report_pics', models.FileField(blank=True, null=True, upload_to='report_pics')),
                ('diseaseinfo', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.diseaseinfo')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.patient')),
            ],
        ),
        migrations.CreateModel(
            name='rating_review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('review', models.TextField(blank=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.patient')),
            ],
        ),
        migrations.CreateModel(
            name='notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(max_length=500)),
                ('consultationDateTime', models.DateTimeField()),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.patient')),
            ],
        ),
        migrations.AddField(
            model_name='diseaseinfo',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.patient'),
        ),
        migrations.CreateModel(
            name='consultingpayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('paying', models.IntegerField(default=0)),
                ('bank', models.TextField(blank=True)),
                ('accountno', models.IntegerField(default=0)),
                ('description', models.TextField(max_length=500)),
                ('status', models.CharField(max_length=20)),
                ('payment_method', models.CharField(choices=[('By Website', ' By Website'), ('Khalti', 'Khalti'), ('Esewa', 'Esewa')], default='By Website', max_length=20)),
                ('consultation', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.consultation')),
                ('diseaseinfo', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.diseaseinfo')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.patient')),
            ],
        ),
        migrations.AddField(
            model_name='consultation',
            name='diseaseinfo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.diseaseinfo'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.doctor'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.patient'),
        ),
        migrations.CreateModel(
            name='approval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultation_date', models.DateField()),
                ('status', models.CharField(max_length=20)),
                ('diseaseinfo', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.diseaseinfo')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.patient')),
            ],
        ),
    ]
