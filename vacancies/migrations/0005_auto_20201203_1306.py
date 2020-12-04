# Generated by Django 3.1.2 on 2020-12-03 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0004_auto_20201202_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(verbose_name='Информация о компании'),
        ),
        migrations.AlterField(
            model_name='company',
            name='employee_count',
            field=models.IntegerField(verbose_name='Количество человек в компании'),
        ),
        migrations.AlterField(
            model_name='company',
            name='location',
            field=models.CharField(max_length=70, verbose_name='География'),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(height_field='height_field', upload_to='company_images', verbose_name='Логотип', width_field='width_field'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=70, verbose_name='Название компании'),
        ),
    ]
