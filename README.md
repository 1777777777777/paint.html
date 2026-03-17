# paint.html

Sivu on toteutettu täysin ilman JavaScriptiä. Sivulta löytyy kynätyökalu sekä maalipurkki, joka simuloi alueen flood fillin SVG-filttereiden avulla.

Vaikka sainkin SVG-filtterit lopulta toimimaan millä tahansa värillä[^1], aion kuitenkin rajoittaa värit mustavalkoiseen esteettisten käsitysten vuoksi. Samalla myös bugien määrä, joihin käyttäjä muuten väistämättä törmäisi. Ongelma on pitkälti ihan vain siinä, miten SVG-filtterit toimivat.

Tällä hetkellä piirroksia ei pysty tallentamaan. Tämän voisi kuitenkin tulevaisuudessa toteuttaa lähettämällä jokaisesta pikselistä erikseen `background-image`-kutsun palvelimelle. Maalipurkkityökalun voisi hoitaa samalla tavalla, jossa palvelimella ajettavan BFS-simulaation perusteella tulokset tallennettaisiin SQLite-tietokantaan.

Aion tietenkin lisätä myös kaikki muut tehtävänannon vaatimat ominaisuudet.

[^1]: Filtterin tyypiksi piti `table`:n sijaan laittaa `discrete`...
