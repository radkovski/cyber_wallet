# Generated by Django 4.0.3 on 2022-03-24 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=30)),
                ('value', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('password_hash', models.CharField(max_length=32)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_moment', models.DateTimeField()),
                ('to_moment', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cyber_wallet_application.user')),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('executionMoment', models.DateTimeField()),
                ('accountingMoment', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cyber_wallet_application.user')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_moment', models.DateTimeField()),
                ('to_moment', models.DateTimeField()),
                ('text', models.CharField(max_length=5000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cyber_wallet_application.user')),
            ],
        ),
        migrations.CreateModel(
            name='LocalConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=30)),
                ('value', models.CharField(max_length=5000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cyber_wallet_application.user')),
            ],
        ),
    ]