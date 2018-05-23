# flake8: noqa

# This is an auto-generated Django model module. It helps the Django ORM map to
# the legacy database. You probably shouldn't change anything here.

from django.db import models


class Sebi(models.Model):
    pers_som_soks = models.IntegerField(primary_key=True)
    pers_som_soker = models.IntegerField(blank=True, null=True)
    hittad = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SEBI'


class AktPers(models.Model):
    akt = models.ForeignKey('Aktivitet', models.DO_NOTHING)
    pers = models.ForeignKey('Person', models.DO_NOTHING)
    svar = models.CharField(max_length=1)
    kommentar = models.TextField()

    class Meta:
        managed = False
        db_table = 'akt_pers'
        unique_together = (('akt', 'pers'),)


class AktPobel(models.Model):
    id = models.BigIntegerField(primary_key=True)
    akt_id = models.IntegerField()
    pobel_id = models.IntegerField()
    svar = models.CharField(max_length=1)
    kommentar = models.TextField()

    class Meta:
        managed = False
        db_table = 'akt_pobel'
        unique_together = (('akt_id', 'pobel_id'),)


class AktPobelPerson(models.Model):
    fnamn = models.CharField(max_length=63)
    enamn = models.CharField(max_length=63)
    epost = models.CharField(max_length=127)
    senast_anv = models.DateField()

    class Meta:
        managed = False
        db_table = 'akt_pobel_person'
        unique_together = (('fnamn', 'enamn', 'epost'),)


class Aktivitet(models.Model):
    arrangor = models.ForeignKey('Person', models.DO_NOTHING)
    aktivitet = models.CharField(max_length=127)
    plats = models.CharField(max_length=127)
    koordinat = models.ForeignKey(
        'Coord', models.DO_NOTHING, db_column='koordinat', blank=True, null=True)
    fritext = models.TextField()
    tid = models.DateTimeField()
    sluttid = models.DateTimeField()
    sistasvarstid = models.DateTimeField()
    sluten = models.CharField(max_length=1)
    anonym = models.CharField(max_length=3)
    meddela = models.CharField(max_length=41)

    class Meta:
        managed = False
        db_table = 'aktivitet'


class ArrPers(models.Model):
    arr_id = models.IntegerField(blank=True, null=True)
    pers_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arr_pers'


class Arrangemang(models.Model):
    arr = models.CharField(max_length=63, blank=True, null=True)
    fritext = models.TextField(blank=True, null=True)
    datum = models.DateField(blank=True, null=True)
    slutdatum = models.DateField(blank=True, null=True)
    barstat = models.CharField(max_length=3, blank=True, null=True)
    maillist = models.ForeignKey(
        'Mailadress', models.DO_NOTHING, db_column='maillist', blank=True, null=True)
    mapcolor = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arrangemang'


class BarenStat(models.Model):
    pers = models.IntegerField(primary_key=True)
    datum = models.DateField()
    cl = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'baren_stat'
        unique_together = (('pers', 'datum'),)


class Barskulder(models.Model):
    blasar_id = models.IntegerField()
    belopp = models.FloatField()
    datum = models.DateField(blank=True, null=True)
    fritext = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'barskulder'


class Blasbaslog(models.Model):
    logid = models.AutoField(primary_key=True)
    time = models.DateTimeField(blank=True, null=True)
    query = models.TextField(blank=True, null=True)
    editby = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blasbaslog'


class Bokning(models.Model):
    resurs_id = models.IntegerField()
    startdt = models.DateTimeField()
    slutdt = models.DateTimeField()
    person = models.CharField(max_length=63, blank=True, null=True)
    fritext = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bokning'


class Bokresurs(models.Model):
    namn = models.CharField(max_length=63, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bokresurs'


class Coord(models.Model):
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    namn = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coord'


class CoordArr(models.Model):
    coordid = models.ForeignKey(Coord, models.DO_NOTHING, db_column='coordid')
    arrid = models.ForeignKey(Arrangemang, models.DO_NOTHING, db_column='arrid')
    datum = models.DateField(blank=True, null=True)
    tid = models.TimeField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coord_arr'


class Deletelog(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=255)
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'deletelog'


class Et05(models.Model):
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'et05'


class ExtraSida(models.Model):
    sidnamn = models.CharField(primary_key=True, max_length=255)
    text = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'extra_sida'


class Extramail(models.Model):
    addr = models.OneToOneField('Mailadress', models.DO_NOTHING, db_column='addr', primary_key=True)
    password = models.CharField(max_length=63, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'extramail'


class Flumm(models.Model):
    flummid = models.AutoField(primary_key=True)
    link = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flumm'


class FragaKat(models.Model):
    beskrivning = models.CharField(max_length=85, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fraga_kat'


class Funk(models.Model):
    funkid = models.AutoField(primary_key=True)
    namn = models.CharField(max_length=31)
    styr = models.CharField(max_length=1)
    beskr = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funk'


class Gb(models.Model):
    tstamp = models.IntegerField()
    author = models.CharField(max_length=255, blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    gb_id = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'gb'


class Identitet(models.Model):
    idtyp = models.IntegerField(blank=True, null=True)
    pers = models.IntegerField(blank=True, null=True)
    varde = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'identitet'


class Identitetstyp(models.Model):
    namn = models.CharField(max_length=32, blank=True, null=True)
    skapare = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'identitetstyp'


class Image(models.Model):
    path = models.CharField(max_length=63)
    url = models.CharField(max_length=63)
    height = models.SmallIntegerField(blank=True, null=True)
    width = models.SmallIntegerField(blank=True, null=True)
    alt = models.TextField(blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    readacc = models.IntegerField(blank=True, null=True)
    writeacc = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    changed = models.DateTimeField(blank=True, null=True)
    access = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'image'


class Instrument(models.Model):
    instrid = models.AutoField(primary_key=True)
    lnamn = models.CharField(max_length=31)
    knamn = models.CharField(max_length=31, blank=True, null=True)
    sekt = models.ForeignKey('Sektion', models.DO_NOTHING, db_column='sekt')
    hemsida = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instrument'


class Karta(models.Model):
    fil = models.CharField(max_length=63, blank=True, null=True)
    beskrivning = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'karta'


class Kartplats(models.Model):
    kartplatsid = models.AutoField(primary_key=True)
    kartid = models.IntegerField(blank=True, null=True)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    plats = models.CharField(max_length=63, blank=True, null=True)
    typ = models.CharField(max_length=8, blank=True, null=True)
    startdt = models.DateTimeField(blank=True, null=True)
    slutdt = models.DateTimeField(blank=True, null=True)
    fritext = models.TextField(blank=True, null=True)
    linkkartid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kartplats'


class Kort(models.Model):
    nummer = models.CharField(max_length=16)
    persid = models.IntegerField()
    aktiv = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'kort'


class Kres(models.Model):
    resid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kres'


class KresPers(models.Model):
    persid = models.IntegerField()
    kresid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kres_pers'


class Logkort(models.Model):
    ts = models.DateTimeField()
    kortid = models.CharField(max_length=16)
    felid = models.IntegerField()
    resid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'logkort'


class Logresurs(models.Model):
    resid = models.IntegerField()
    status = models.IntegerField()
    ts = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'logresurs'


class Mailadress(models.Model):
    mailadress = models.CharField(primary_key=True, max_length=31)

    class Meta:
        managed = False
        db_table = 'mailadress'


class Maillist(models.Model):
    maillistid = models.AutoField(primary_key=True)
    namn = models.ForeignKey(
        Mailadress, models.DO_NOTHING, db_column='namn', blank=True, null=True)
    beskr = models.CharField(max_length=63, blank=True, null=True)
    slutdatum = models.DateField(blank=True, null=True)
    sluten = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maillist'


class Medlem(models.Model):
    medlemid = models.AutoField(primary_key=True)
    pers = models.ForeignKey('Person', models.DO_NOTHING, db_column='pers')
    datum = models.DateField()
    typ = models.CharField(max_length=7)
    instr = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'medlem'


class Misslyckadeadd(models.Model):
    musid = models.IntegerField(blank=True, null=True)
    typ = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=15, blank=True, null=True)
    ts = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'misslyckadeadd'


class MsStat(models.Model):
    pers = models.OneToOneField('Person', models.DO_NOTHING, primary_key=True)
    datum = models.DateField()
    tillstand = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'ms_stat'
        unique_together = (('pers', 'datum'),)


class Musik(models.Model):
    filnamn = models.CharField(max_length=255)
    titel = models.CharField(max_length=127)
    artist = models.CharField(max_length=127)
    ip = models.CharField(max_length=15, blank=True, null=True)
    antal = models.IntegerField()
    ts = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'musik'


class Offyellow2005(models.Model):
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'offyellow2005'


class Oldmusik(models.Model):
    filnamn = models.CharField(max_length=255)
    titel = models.CharField(max_length=127)
    artist = models.CharField(max_length=127)
    ip = models.CharField(max_length=15, blank=True, null=True)
    antal = models.IntegerField()
    ts = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oldmusik'


class Oldspellista(models.Model):
    musid = models.IntegerField()
    status = models.CharField(max_length=5)
    ts = models.DateTimeField()
    ip = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oldspellista'


class Pagang(models.Model):
    plats = models.CharField(max_length=63, blank=True, null=True)
    dag = models.DateField(blank=True, null=True)
    tid = models.TimeField(blank=True, null=True)
    fritext = models.TextField(blank=True, null=True)
    koordinat = models.ForeignKey(
        Coord, models.DO_NOTHING, db_column='koordinat', blank=True, null=True)
    kontakt = models.CharField(max_length=63, blank=True, null=True)
    kontakttel = models.CharField(max_length=31, blank=True, null=True)
    kontaktmail = models.CharField(max_length=31, blank=True, null=True)
    kontaktbetyg = models.TextField(blank=True, null=True)
    pris = models.CharField(max_length=31, blank=True, null=True)
    kommentar = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pagang'


class Page(models.Model):
    parent = models.IntegerField(blank=True, null=True)
    access = models.IntegerField()
    title = models.CharField(max_length=63)
    scriptid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'page'


class Persfunk(models.Model):
    pers = models.ForeignKey('Person', models.DO_NOTHING, db_column='pers')
    funk = models.ForeignKey(Funk, models.DO_NOTHING, db_column='funk')
    startdatum = models.DateField()
    slutdatum = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'persfunk'


class Perslist(models.Model):
    perslistid = models.AutoField(primary_key=True)
    pers = models.ForeignKey('Person', models.DO_NOTHING, db_column='pers')
    maillist = models.ForeignKey(Maillist, models.DO_NOTHING, db_column='maillist')
    admin = models.CharField(max_length=1, blank=True, null=True)
    request = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'perslist'


class Person(models.Model):
    persid = models.AutoField(primary_key=True)
    fnamn = models.CharField(max_length=63, blank=True, null=True)
    enamn = models.CharField(max_length=63, blank=True, null=True)
    smek = models.CharField(max_length=63, blank=True, null=True)
    fodd = models.DateField(blank=True, null=True)
    pnr_sista = models.CharField(max_length=4, blank=True, null=True)
    gatuadr = models.CharField(max_length=63, blank=True, null=True)
    postnr = models.CharField(max_length=15, blank=True, null=True)
    ort = models.CharField(max_length=63, blank=True, null=True)
    land = models.CharField(max_length=63, blank=True, null=True)
    epost = models.CharField(max_length=63, blank=True, null=True)
    studentid = models.CharField(max_length=8, blank=True, null=True)
    hemnr = models.CharField(max_length=20, blank=True, null=True)
    mobilnr = models.CharField(max_length=31, blank=True, null=True)
    jobbnr = models.CharField(max_length=20, blank=True, null=True)
    icqnr = models.CharField(max_length=20, blank=True, null=True)
    fritext = models.TextField(blank=True, null=True)
    blasmail = models.OneToOneField(
        Mailadress, models.DO_NOTHING, db_column='blasmail', blank=True, null=True)
    gras_medlem_till = models.DateField(blank=True, null=True)
    arbete = models.CharField(max_length=63, blank=True, null=True)
    icke_blasare = models.CharField(max_length=1, blank=True, null=True)
    password = models.CharField(max_length=32, blank=True, null=True)
    nomail = models.CharField(max_length=1, blank=True, null=True)
    veg = models.CharField(max_length=1, blank=True, null=True)
    gluten = models.CharField(max_length=1, blank=True, null=True)
    nykter = models.CharField(max_length=1, blank=True, null=True)
    allergi = models.TextField(blank=True, null=True)
    admin = models.CharField(max_length=7, blank=True, null=True)
    sedd_av_anv = models.DateField(blank=True, null=True)
    latlong = models.CharField(max_length=63, blank=True, null=True)
    kon = models.CharField(max_length=1, blank=True, null=True)
    epost_utskick = models.CharField(max_length=8, blank=True, null=True)
    senast_kollad = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'


class Persres(models.Model):
    persid = models.IntegerField(primary_key=True)
    resid = models.IntegerField()
    startdt = models.DateTimeField()
    slutdt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'persres'
        unique_together = (('persid', 'resid'),)


class Resurs(models.Model):
    namn = models.CharField(max_length=63)
    aktiv = models.CharField(max_length=1)
    script = models.CharField(max_length=63)
    device = models.CharField(max_length=63, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resurs'


class Resursio(models.Model):
    resid = models.IntegerField()
    success = models.CharField(max_length=1)
    port = models.CharField(max_length=4, blank=True, null=True)
    mask = models.IntegerField()
    tid = models.SmallIntegerField()
    waitport = models.CharField(max_length=4, blank=True, null=True)
    waitmask = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resursio'


class Saxsekten(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    freetext = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'saxsekten'


class Script(models.Model):
    showscript = models.CharField(max_length=63, blank=True, null=True)
    editscript = models.CharField(max_length=63, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'script'



class Sektion(models.Model):
    sektid = models.AutoField(primary_key=True)
    lnamn = models.CharField(max_length=31)
    knamn = models.CharField(max_length=31, blank=True, null=True)
    hemsida = models.CharField(max_length=255, blank=True, null=True)
    listordning = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sektion'


class Spellista(models.Model):
    musid = models.IntegerField()
    status = models.CharField(max_length=5)
    ts = models.DateTimeField()
    ip = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spellista'


class Svar(models.Model):
    id = models.IntegerField(primary_key=True)
    svar = models.TextField(blank=True, null=True)
    katid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'svar'


class T2S(models.Model):
    id = models.IntegerField(primary_key=True)
    msg = models.TextField()
    username = models.CharField(max_length=255)
    ts = models.IntegerField()
    ip = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 't2s'


class Test(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'


class Uppslag(models.Model):
    id = models.IntegerField(primary_key=True)
    ord = models.CharField(max_length=255)
    betydelse = models.TextField()
    godkand = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uppslag'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    persid = models.IntegerField(blank=True, null=True)
    login = models.CharField(max_length=63)
    pwd = models.CharField(max_length=16)
    access = models.IntegerField()
    ts = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'
