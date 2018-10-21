# Generated by Django 2.1.2 on 2018-10-08 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ha', '0003_auto_20181008_2026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='haitem',
            options={'verbose_name': 'haItem', 'verbose_name_plural': 'Hausaufgaben Einträge'},
        ),
        migrations.AddField(
            model_name='haitem',
            name='subject',
            field=models.CharField(choices=[('Bio', 'Biologie'), ('Ch', 'Chemie'), ('D', 'Deutsch'), ('E', 'Englisch'), ('Ek', 'Erdkunde'), ('Fr', 'Französisch'), ('Ge', 'Geschichte'), ('Inf', 'Informatik'), ('Ku', 'Kunst'), ('Lt', 'Latein'), ('M', 'Mathematik'), ('Ph', 'Philosophie'), ('Spo', 'Sport'), ('None', 'keins'), ('kR', 'kath. Religion'), ('eR', 'ev. Religion')], default=None, max_length=100),
            preserve_default=False,
        ),
    ]