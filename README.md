# paint.html

Sivu on toteutettu täysin ilman JavaScriptiä. Sivulta löytyy kynätyökalu sekä maalipurkki, joka simuloi alueen flood fillin SVG-filttereiden avulla.

Vaikka sainkin SVG-filtterit lopulta tukemaan eri värejä[^1], pitäydyn ehkä mustavalkoisessa tyylissä esteettisistä syistä. Samalla vähenee myös bugien määrä, joihin käyttäjä muuten väistämättä törmäisi. Ongelmat johtuvat pitkälti siitä, miten SVG-filtterit toimivat.

Tällä hetkellä piirroksia ei pysty tallentamaan. Sen voisi kuitenkin toteuttaa lähettämällä jokaisesta pikselistä erillisen `background-image`-kutsun palvelimelle. Maalipurkkityökalun voisi toimia samalla tavalla. Palvelin ajaisi BFS-simulaation ja tallentaisi tulokset SQLite-tietokantaan

Aion tietenkin lisätä myös kaikki muut tehtävänannon vaatimat ominaisuudet.

[^1]: Filtterin tyypiksi piti `table`:n sijaan laittaa `discrete`...
