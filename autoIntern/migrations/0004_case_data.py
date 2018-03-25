# Generated by Django 2.0.2 on 2018-03-23 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autoIntern', '0003_auto_20180320_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('case_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('documents', models.ManyToManyField(to='autoIntern.Document')),
                ('user_permissions', models.ManyToManyField(to='autoIntern.User')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('data_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('value', models.CharField(max_length=255)),
                ('label', models.CharField(max_length=255)),
                ('line', models.CharField(max_length=255)),
                ('index', models.CharField(max_length=255)),
                ('current', models.NullBooleanField()),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoIntern.Case')),
                ('creator_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoIntern.User')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoIntern.Document')),
            ],
        ),
    ]