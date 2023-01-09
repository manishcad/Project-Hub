# Generated by Django 4.1.5 on 2023-01-06 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_alter_profile_other_skills'),
        ('Home', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=50)),
                ('skill_bio', models.TextField(blank=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.profile')),
            ],
        ),
    ]