# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 12:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adres',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('kod_pocztowy', models.TextField()),
                ('miasto', models.TextField()),
                ('ulica', models.TextField()),
            ],
            options={
                'db_table': 'adres',
            },
        ),
        migrations.CreateModel(
            name='AdresBudynek',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('kod_pocztowy', models.TextField()),
                ('miasto', models.TextField()),
                ('ulica', models.TextField()),
            ],
            options={
                'db_table': 'adresbudynek',
            },
        ),
        migrations.CreateModel(
            name='Budynek',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'budynek',
            },
        ),
        migrations.CreateModel(
            name='Faktura',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('wartosc_netto', models.FloatField()),
            ],
            options={
                'db_table': 'faktura',
            },
        ),
        migrations.CreateModel(
            name='Licznik',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('typ', models.TextField()),
                ('cena_netto', models.FloatField()),
            ],
            options={
                'db_table': 'licznik',
            },
        ),
        migrations.CreateModel(
            name='Mieszkanie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('metraz', models.FloatField()),
                ('liczba_pokoi', models.IntegerField()),
                ('piwnica', models.BooleanField()),
                ('nr_mieszkania', models.IntegerField()),
                ('budynek', models.ForeignKey(db_column='budynek', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.Budynek')),
            ],
            options={
                'db_table': 'mieszkanie',
            },
        ),
        migrations.CreateModel(
            name='Nadgodziny',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ilosc', models.FloatField()),
            ],
            options={
                'db_table': 'nadgodziny',
            },
        ),
        migrations.CreateModel(
            name='Pracownik',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('budynek', models.IntegerField(null=True)),
                ('imie', models.TextField()),
                ('nazwisko', models.TextField()),
                ('telefon', models.TextField()),
                ('email', models.TextField()),
                ('adres', models.ForeignKey(db_column='adres', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.Adres')),
            ],
            options={
                'db_table': 'pracownik',
            },
        ),
        migrations.CreateModel(
            name='StanLicznik',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stan', models.FloatField()),
                ('mieszkanie', models.ForeignKey(db_column='mieszkanie', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.Mieszkanie')),
                ('typ', models.ForeignKey(db_column='typ', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.Licznik')),
            ],
            options={
                'db_table': 'stan_licznik',
            },
        ),
        migrations.CreateModel(
            name='Stanowisko',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa', models.TextField()),
                ('pensja', models.IntegerField()),
            ],
            options={
                'db_table': 'stanowisko',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pracownik', models.TextField(blank=True, null=True)),
                ('zglaszajacy', models.TextField(blank=True, default=None, null=True)),
                ('opis', models.TextField()),
                ('data', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'ticket',
            },
        ),
        migrations.CreateModel(
            name='Wlasciciel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('imie', models.TextField()),
                ('nazwisko', models.TextField()),
                ('telefon', models.TextField()),
                ('email', models.TextField()),
                ('mieszkanie', models.ForeignKey(blank=True, db_column='mieszkanie', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.Mieszkanie')),
            ],
            options={
                'db_table': 'wlasciciel',
            },
        ),
        migrations.CreateModel(
            name='Wydarzenie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa', models.TextField()),
                ('opis', models.TextField()),
                ('data', models.DateField()),
                ('budynek', models.ForeignKey(blank=True, db_column='budynek', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.Budynek')),
            ],
            options={
                'db_table': 'wydarzenie',
            },
        ),
        migrations.CreateModel(
            name='Wystawca',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa', models.TextField()),
                ('kod_pocztowy', models.TextField()),
                ('miasto', models.TextField()),
                ('ulica', models.TextField()),
                ('telefon', models.TextField()),
                ('email', models.TextField()),
            ],
            options={
                'db_table': 'wystawca',
            },
        ),
        migrations.AddField(
            model_name='pracownik',
            name='stanowisko',
            field=models.ForeignKey(db_column='stanowisko', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.Stanowisko'),
        ),
        migrations.AddField(
            model_name='nadgodziny',
            name='pracownik',
            field=models.ForeignKey(db_column='pracownik', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.Pracownik'),
        ),
        migrations.AddField(
            model_name='faktura',
            name='wlasciciel',
            field=models.ForeignKey(blank=True, db_column='wlasciciel', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.Wlasciciel'),
        ),
        migrations.AddField(
            model_name='faktura',
            name='wystawca',
            field=models.ForeignKey(db_column='wystawca', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.Wystawca'),
        ),
        migrations.AddField(
            model_name='budynek',
            name='administrator',
            field=models.ForeignKey(db_column='administrator', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.Pracownik'),
        ),
        migrations.AddField(
            model_name='budynek',
            name='adres',
            field=models.ForeignKey(db_column='adresbudynek', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.AdresBudynek'),
        ),
    ]
