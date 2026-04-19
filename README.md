# paint.html

paint.html on toteutettu täysin ilman JavaScriptiä. 

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään.
* Käyttäjä pystyy luomaan piirroksia kynää ja maalipurkkia käyttäen.
* Käyttäjä pystyy myös nimeämään uudelleen tai poistamaan piirroksiaan.
* Käyttäjä näkee sovellukseen lisätyt piirrokset.
* Käyttäjä pystyy etsimään piirroksia hakusanalla.
* Sovelluksessa ei vielä ole käyttäjäsivuja eikä piirrosten luokittelua...
* Käyttäjä pystyy tykkäämään piirroksista. Tykkäyksiä klikkaamalla avautuu lista kaikista kyseisestä piirroksesta tykänneistä käyttäjistä. (CSS vielä kesken, joten näyttää paremmalta kun tykkää muiden kuin omien piirroksista)

Asenna ensin Flask: `pip install flask`

Luo database.db: `sqlite3 database.db < schema.sql`

Käynnistä sitten sovellus: `python app.py`

Jos maalipurkki ei toimi, vähennä iteraatioiden määrää esim. `python app.py --iterations 10`

---

Sovelluksesta löytyy piirtoalusta, kynätyökalu sekä maalipurkki, joka simuloi alueen flood fillin SVG-filttereiden avulla. Kynä on puolestaan toteutettu `:has()`-pseudoluokan avulla, joka seuraa työkalun tilaa ja hiiren liikkeitä.

Piirtäessä sovellus ns. generoi merkkijonon, johon on koodattuna käyttäjän värittämät pikselit[^1]. Käyttäjä sitten raahaa tämän merkkijonon tekstikenttään ja lähettää piirtoalustan tilan näin palvelimelle. Koska maalipurkin värittämiä alueita ei voi suoraan tallentaa pelkän CSS:n avulla, palvelimen on ajettava oma BFS-simulaatio maalipurkin alkupikselin perusteella. Lopullinen piirros tallentuu SQLite-tietokantaan.

Myös galleria ja piirrosten suurentaminen toimivat ilman JavaScriptiä. Pop-up -ikkunat on toteutettu HTML-ankkureiden ja `:target`-pseudoluokan avulla.

Vaikka sainkin SVG-filtterit lopulta tukemaan eri värejä[^2], pitäydyn ehkä kuitenkin mustavalkoisessa värimaailmassa esteettisistä syistä. Samalla vähenee myös bugien määrä, joihin käyttäjä muuten väistämättä törmäisi. Ongelmat johtuvat pitkälti siitä, miten SVG-filtterit toimivat.

Sivu on testattu Edgellä ja Firefox Developer Editionilla. Koska flood fill on simuloitu SVG-filttereiden avulla ilman rekursiota, iterointi on koodattu suoraan HTML-tiedostoon. DOM-elementtien määrä voi siis olla hyvinkin suuri, ja sivun toimivuus on kiinni käyttäjän koneen tehoista. Esimerkiksi omalla koneella U-kirjaimen muotoisen alueen täyttäminen vaatii vähintään 55 iteraatiota.

~Vanha demo-sivu löytyy [täältä](https://1777777777777.github.io/paint.html/).~

Alla oleva GIF havainnollistaa filttereiden toimintaa.[^3]

![SVGFX](svgfx3.gif)


[^1]: Jokainen pikseli sisältää jo valmiiksi merkit "0", "1" ja "b". CSS:n `:has()`, `visibility` ja `max-width` avulla tarpeettomat merkit saadaan piiloon. Näitä oli pakko käyttää, koska toisin kuin esim. pelkällä `opacity: 0`:lla piilotetut elementit, selaimet *eivät* kopioi merkkejä, jotka ovat `visibility: hidden` **JA**  `max-width: 0`. 

[^2]: Filtterin tyypiksi piti `table`:n sijaan laittaa `discrete`...

[^3]: Käytin filttereiden suunnitteluun [SVGFM](https://svgfm.chriskirknielsen.com/)-työkalua. Generoima koodi oli kuitenkin virheellinen ja vaati korjaamista.
