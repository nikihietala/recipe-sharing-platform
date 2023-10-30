# Reseptien jakamisalusta (RecipeRealm)

Sovelluksen avulla voi jakaa omia ruokareseptejä. 

Sovelluksen ominaisuuksia ovat:

* Kaikki pystyvät katsomaan sovellukseen jaettuja reseptejä.
* Sovellukseen voi luoda käyttäjätunnuksen jolla kirjautua sisään.
* Käyttäjä voi jakaa ruokareseptejä (annoksen hinta, raaka-aineet, ravinto-arvot).
* Käyttäjä voi kirjoittaa kommentteja resepteihin (esim., ruuan valmistusohjeet).
* Käyttäjä voi arvostella ruokareseptin (1-5 tähteä, reseptit näkyvät sovelluksessa arvosanan mukaan - korkein ensin).
* Käyttäjä voi merkata halutun reseptin omien suosikkien joukkoon (tai poistaa omasta suosikki-listasta).
* Käyttäjä voi käyttää hakupalvelua etsiäkseen reseptejä (hakuperusteina raaka-aine tai hinta).
* Käyttäjä voi halutessaan poistaa jakamansa reseptin.

**Huom:**
Mahdollinen kehitysidea olisi yhdistää sovellukseen jokin internetistä valmiiksi löytyvä ruuan ravintoarvo-taulukko (esim. tämän tyylinen https://www.kilokalori.net/ravinto/kaloritaulukko?sortBy=totalCount&sortOrder=desc&page=1). Eli käyttäjä voisi jakaa oman reseptinsä, listata tarvittavat raaka-aineet ja sovellus automaattisesti antaisi reseptin ravintoarvot. Tämä muutos antaisi sovellukselle jotain oikeaa käyttöarvoa. Tämänhetkiseen sovellukseen käyttäjän täytyy itse arvioida annoksen ravinto-arvot(proteiini, hiilarit, rasva).

## Sovelluksen asentamisen ohjeet (paikallisesti):
**Huom:**
Asentamisen ohjeet ovat hieman erilaisia riippuen käyttöjärjestelmästä (Linux/Windows/Mac). Seuraavat esimerkkiohjeet ovat Linuxille. Oletus on että käytössäsi on Python3 ja PostgreSQL.

1. Lataa sovelluksen GitHub-repository

2. Luo .env tiedosto kyseiseen kansioon ja lisää sinne seuraavat tiedot:
* DATABASE_URL=postgresql:///user
* SECRET_KEY=<your_secret_key>

3. Aktivoi virtuaaliympäristö terminaalissa
```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

4. Huolehdi että sinulla on requirements.txt tiedostosta löytyvät paketit

```bash
pip install -r ./requirements.txt
```

5. Luo tietokanta psql:ssä
```bash
psql < schema.sql
```

6. Käynnistä sovellus
```bash
flask run
```




