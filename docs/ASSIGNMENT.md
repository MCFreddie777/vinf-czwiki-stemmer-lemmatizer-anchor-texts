====== CZWiki - Lematizer, Stemmer založený na anchor textoch. ======

==== Motivácia ====

Úspešné vypracovanie zadania obnáša lematizovanie a stemmovanie linkov na českej wikipédií. Linky sú označené ako anchor texty, a budeme pracovať s textami v ich vnútri.

==== Súčasné riešenia ====

TBA: prehľad súčasných riešení daného problému - existujúci softvér, algoritmy, vedecké články, linky (0,5 strany)

==== Vypracovanie ====

TBA: popis riešenia, použitý softvér, použité existujúce riešenia, popis problémov ktoré sa vyskytli, popis prác na projekte (1 strana)

==== Dataset ====
Na oficiálnej stránke wikipédie  [[https://dumps.wikimedia.org/cswiki/latest/|https://dumps.wikimedia.org/cswiki/latest/]] sme z dumpov stiahli archívy dát. Rozbalené dáta obsahovali XML súbory s danými stránkami a podstránkami wikipédie.

Root elementom daného XML súboru je tag //feed//. 
Ten obsahuje množstvo elementov typu //doc//, ktoré majú každý svoj //title//, //url//, //abstract// a pole //links//.

Nás budú hlavne zaujímať práve posledné, //links//. Toto pole obsahuje elementy //sublink// - podlinky.
Samotné kotvy (anchory) s ktorými budeme pracovať  sa nacházajú v značkách //anchor// a cesta na ktorú ukazuje je tag //link//.

==== Vyhodnotenie ====

TBA: vyhodnotenie slovné subjektívne na nejakých konkrétnych príkladoch. Vo vačšine projektov aj vyhodnotenie pomocou presnosti a pokrytia (precision a recall) (0,5-1 strana)

==== Použitie ====
TBA: spustenie, inštalácia softvéru, použitie softvéru. (0,5-1 strana)


