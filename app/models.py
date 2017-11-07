# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Adres(models.Model):
    id = models.AutoField(primary_key=True)
    kod_pocztowy = models.TextField()
    miasto = models.TextField()
    ulica = models.TextField()
    telefon = models.TextField()
    email = models.TextField()

    class Meta:
        db_table = 'adres'


class Budynek(models.Model):
    id = models.AutoField(primary_key=True)
    adres = models.ForeignKey(Adres, models.DO_NOTHING, db_column='adres', related_name='+')
    administrator = models.ForeignKey('Pracownik', models.DO_NOTHING, db_column='administrator', related_name='+')

    class Meta:
        db_table = 'budynek'


class Faktura(models.Model):
    id = models.AutoField(primary_key=True)
    wartosc_netto = models.FloatField()
    wystawca = models.ForeignKey('Wystawca', models.DO_NOTHING, db_column='wystawca', related_name='+')
    adres = models.IntegerField()
    wlasciciel = models.ForeignKey('Wlasciciel', models.DO_NOTHING, db_column='wlasciciel', related_name='+')

    class Meta:
        db_table = 'faktura'


class Licznik(models.Model):
    id = models.AutoField(primary_key=True)
    typ = models.TextField()
    cena_netto = models.FloatField()

    class Meta:
        db_table = 'licznik'


class Mieszkanie(models.Model):
    id = models.AutoField(primary_key=True)
    budynek = models.IntegerField()
    metraz = models.FloatField()
    liczba_pokoi = models.IntegerField()
    piwnica = models.BooleanField()
    wlasciciel = models.ForeignKey('Wlasciciel', models.DO_NOTHING, db_column='wlasciciel', blank=True, null=True, related_name='+')

    class Meta:
        db_table = 'mieszkanie'


class Nadgodziny(models.Model):
    id = models.AutoField(primary_key=True)
    pracownik = models.ForeignKey('Pracownik', models.DO_NOTHING, db_column='pracownik', related_name='+')
    ilosc = models.FloatField()

    class Meta:
        db_table = 'nadgodziny'


class Pracownik(models.Model):
    id = models.AutoField(primary_key=True)
    stanowisko = models.ForeignKey('Stanowisko', models.DO_NOTHING, db_column='stanowisko', related_name='+')
    budynek = models.IntegerField(null=True)
    imie = models.TextField()
    nazwisko = models.TextField()
    adres = models.ForeignKey(Adres, models.DO_NOTHING, db_column='adres', related_name='+')

    class Meta:
        db_table = 'pracownik'


class StanLicznik(models.Model):
    id = models.AutoField(primary_key=True)
    typ = models.ForeignKey('self', models.DO_NOTHING, db_column='typ')
    mieszkanie = models.ForeignKey(Mieszkanie, models.DO_NOTHING, db_column='mieszkanie', related_name='+')
    stan = models.FloatField()

    class Meta:
        db_table = 'stan_licznik'


class Stanowisko(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.TextField()
    pensja = models.IntegerField()

    class Meta:
        db_table = 'stanowisko'


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    kto = models.ForeignKey(Pracownik, models.DO_NOTHING, db_column='kto', related_name='+')
    mieszkanie = models.IntegerField()
    opis = models.TextField()

    class Meta:
        db_table = 'ticket'


class Wlasciciel(models.Model):
    id = models.AutoField(primary_key=True)
    imie = models.TextField()
    nazwisko = models.TextField()
    adres = models.ForeignKey(Adres, models.DO_NOTHING, db_column='adres', related_name='+')

    class Meta:
        db_table = 'wlasciciel'


class Wydarzenie(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.TextField()
    opis = models.TextField()
    data = models.DateField()
    budynek = models.ForeignKey(Budynek, models.DO_NOTHING, db_column='budynek', blank=True, null=True, related_name='+')

    class Meta:
        db_table = 'wydarzenie'


class Wystawca(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.TextField()
    adres = models.ForeignKey(Adres, models.DO_NOTHING, db_column='adres', related_name='+')

    class Meta:
        db_table = 'wystawca'
