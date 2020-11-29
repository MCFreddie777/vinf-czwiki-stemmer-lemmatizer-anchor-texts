# CZWiki - Lematizer, Stemmer založený na anchor textoch

## Motivácia 

Úspešné vypracovanie zadania obnáša lematizovanie a stemmovanie linkov na českej wikipédií. Linky sú označené ako anchor texty, a budeme pracovať s textami v ich vnútri.

## Návrh riešenia

Celý dátový súbor preparsujeme pomocou Regulárnych výrazov a ęxtrahujeme z neho anchor linky a texty do DataFramu v Pythone.

Po vytiahnutí datasetu očistíme dáta - whitespace, preparsujeme HTML encoded string na klasický string a pod.

Následne dataset pretransformuje cez tokenizér, ktorý nam odstráni stopslová a interpunkciu a daný dataset ešte pretransformujeme pomocou lemantizéru.
Tokenizér využijem z python knižnice nltk a lemmatizér českého jazyka [Majka](https://nlp.fi.muni.cz/czech-morphology-analyser) 

Výsledkom práce bude dataframe s pretransformovanými slovami na základe ktorých budeme môcť vytvárať rozličné štatistiky a analýzy.

Riešenie plánujem vypracovať v grafickom rozšírení pythonu s názvom Jupyter Notebook, v ktorom je možné vizualizovať štatistiky a analýzy pomocou grafov.
K práci s datasetom budem využívať python knižnice `pandas`, `scikit learn`, `numpy`.

#### Diagram architektúry
![Návrh architektúry](navrh_architektury.jpg)

#### Pseudokód

```python
funkcia parsuj(data):
    dataset = []
    pre kazdy riadok(data):
        ak zhoda = riadok.match(RegexAnchoru):
            dataset.pridaj(zhoda)
    return dataset
    
funkcia cisti(dataframe):
    pre kazdy zaznam(dataframe):
        dataframe.zaznam = ostran_whitespace(zaznam).decodeHTMLString()
    return dataframe     
    
funkcia tokenizuj(dataframe):
    pre kazdy zaznam(dataframe):
        dataframe.zaznam = odstran_interpunkciu(zaznam)
        dataframe.zaznam = odstran_stopslova(zaznam)
    return dataframe

funkcia lemmatizuj(df):
    pre kazdy zaznam(dataframe):
        dataframe.zaznam = Lemmatizer.lemmatize(zaznam)
    return dataframe
    
df = parsuj(subor.xml)
df = cisti(df)
df = tokenizuj(df)
df = lemmatizuj(df)    
```

## Súčasné riešenia



Pri hľadaní podobných riešení na danú tému som nenarazil na moc vecí s podobným riešením. 

- Zaradil by som sem však podobnú tému lematizácie - ktorej sa venuje napríklad [verejné API FIIT](http://text.fiit.stuba.sk/lemmatizer/), kde je možné poslať text na lematizáciu - funguje však iba pre slovenčinu. 
- Takisto, téme a extrakcií článkov z wikipédie sa zaoberá aj NLP python knižnica [Gensim](https://radimrehurek.com/gensim/index.html), konkrétne [metódy na extrakciu z wiki dumpov](https://radimrehurek.com/gensim/corpora/wikicorpus.html), ktorá dokáže za cca *~8h* spracovať celú anglickú wikipédiu.
- Za zmienku taktiež stojí [riešenie](https://github.com/drusac/Wikipedia_Keywords_Extractor) autora *drusac* ktoré spracováva daný článok z wikipedie a spracováva a lemmatizuje obsah a extrahuje kľúčové slová.
- Taktiež by som sem zaradil [článok](http://ikt.ui.sav.sk/publications/sk_wikipedia_slovko-2013.pdf) z FIIT z roku 2013 od autorského tria *Laclavík, Dlugolinský a Blanárik*, ktorý sa venoval používaním wikipédie ako primárneho zdroja pre spracovávanie textu.

## Vypracovanie 

Moje vypracované riešenie je dostupné na [https://github.com/MCFreddie777/vinf-czwiki-stemmer-lemmatizer-anchor-texts](https://github.com/MCFreddie777/vinf-czwiki-stemmer-lemmatizer-anchor-texts).

Ako sme už mali možnosť vidieť na obrázku vyššie, vypracovanie som rozdelil na menšie časti - bloky, korešpondujúce k jednotlivým funkciám - `parse_xml_file`, `clear_data`, `tokenize`, `lemmatize`.
Každý z týchto blokov vykoná určitú funkcionalitu nad určeným súborom a výsledok zapisuje do iného súboru, čo nám umožňuje jednak pracovať s malým množstvom dát naraz v pamäti, keďže dáta sa čítajú v chunkoch (malých častiach).

V prvej časti sa načítava pôvodný wiki dump a funkciami obsahujúcimi regex sa z neho extrahujú iba anchor linky a texty.
Tieto dáta sa následne zapíšu do výsledného súboru.
Bližšia implementáciá parsovacích funkcií je možná k nazhladnutiu v súbore `src/parser.py`.

V druhej časti - čistenie dát a tokenizácia sa z výstupného súboru druhej časti načítajú všetky slovné spojenia a vety tokenizujú a čistia. V čistiacej funkci `clear_data` sa odstraňujú nežiadúce znaky, html zakódované żnaky ako `&gt;` alebo `&amp;`, sa prekladajú na ich pôvodné znakové alternatívy.
Vyčistené dáta sa následne rozdelia na tokeny pomocou knižnice *nltk* a ponechajú sa iba tie tokeny, ktoré nie sú v balíčku českých stop slov. Následne sa vyfiltrované tokeny uložia opäť do nového výstupného súboru.

V tretej časti skriptu sa načítajú tokeny zo súboru tokenov a pomocou funkcie `lemmatize` sa lematizujú. V prípade že nejaký token nie je možné lemmatizovat (napríklad neexistuje v slovníku), tak sa skontroluje, koľkýkrát sa toto slovo už nachádzalo v daných tokenoch. v prípade že toto slovo sa tam nachádzalo viackrát ako je nejaký vopred určený limit, tak slovo bude zapísané do výsledného súboru spolu s lematizovanými slovami.
Posledná časť sa venuje už len analýze a štatistikám. Uvádza, koľko slov bolo dokopy vo výslednom súbore, koľko z nich bolo lematizovaných a koľko, naopak bolo pridaných aj bez lematizácie (ich nájdenie nebola náhoda, nachádzali sa tam veľakrát).

Medzi problémy na ktoré som narazil počas vývoja cyklu bolo vytvorenie správneho regexu - čo mi zabralo pár emailových konzultácií s prednášajúcim - nedarilo sa mi vytvoriť skript ktorý by zachytil všetky unicode znaky - akcenty a podobne. Nakoniec sme prišli k triviálnemu riešeniu - benevolentnej bodke (akýkoľvek znak).
Medzi ďalšie problémy by som zaradil problém s pamäťou, ktorý nakoniec nebol problémom. Bál som sa, či udržiavanie unikátnych slov, alebo nelematizovateľných slov bude byť realizovateľné v pamäti - nakoľko najpouživanejšie slová ako "wikipedie" sa tam nachádza niekoľko stotisíckrát.
Na vytvorenie štatistík a grafov však všetky dáta musia byť uložené v pamäti čo sa však nakoniec úkazalo že to nebude až taký problém.

## Dataset

Na oficiálnej stránke wikipédie [https://dumps.wikimedia.org/cswiki/latest/](https://dumps.wikimedia.org/cswiki/latest/) sme z dumpov stiahli archív dát s názvom [cswiki-latest-pages-articles.xml.bz2](https://dumps.wikimedia.org/cswiki/latest/cswiki-latest-pages-articles.xml.bz2). Rozbalené dáta obsahovali XML súbor s danými stránkami a podstránkami wikipédie.

Root elementom daného XML súboru je tag `mediawiki`. 
Ten obsahuje element `siteinfo` a množstvo elementov typu `page`, ktoré majú každý svoj `title`, `id`, `revision`.

Nás budú hlavne zaujímať práve posledné, `revision`. Tento element obsahuje poslednú revíziu - verziu danej stránky. V prípade, že by sme stiahli dump s kompletnou históriou, tých tagov `revision` vrámci tagu `page` by bolo viac.

Každá revízia obsahuje element `text`. V danom elemente sa nachádza kompletný text v syntaxi [Wikitext](https://en.wikipedia.org/wiki/Help:Wikitext).
V tejto syntaxi sa anchor (kotvy) oznacuju zaciatok -  `[[` a koniec - `]]`. 

V anchore sa mozu nachadzat dva texty - prvy je cesta (ci uz absolutna alebo relativna), a text danej kotvy. Tieto dva texty su oddelene znakom `|`. Preto nas bude zaujimat text za tymto znakom.
V pripade ze dany anchor obsahuje len text, ktory sa zhoduje s cestou, anchor neobsahuje znak `|` a 
musime teda vyparsovat cely text.
 
Dany text vyzera byt este zakodovany ako html string - cize napr. znaky `"` su oznacene ako `&quot;`. Toto bude treba preparsovat.

Na extrahovanie anchorov teda pouzijeme RegEx, matchneme vsetok obsah medzi znackami `[[` a `]]`.

#### Sample data:

```xml
<mediawiki xmlns="http:`www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http:`www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http:`www.mediawiki.org/xml/export-0.10/ http:`//`www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="cs">\
  <siteinfo>
  ...
   </siteinfo>
  <page>
  <page>
    ...
    <revision>
      ...
      <text ... >
'''Červenka''' ({{Vjazyce|de}} ''Schwarzbach bei Olmütz'') je [[obec]] v [[Olomoucký kraj|Olomouckém kraji]], 
18&amp;nbsp;km severozápadně od [[Olomouc]]e a 3 km severně od [[Litovel|Litovle]]. 
Leží na levém břehu potoka Čerlinky, který se u [[Tři Dvory (Litovel)|Tří Dvorů]] 
vlévá do bývalého ramene řeky [[Morava (řeka)|Morava]]. 
Žije zde {{Počet obyvatel}} obyvatel.
== Historie =
      </text>
    </revision>
  </page>
</mediawiki>
```


## Vyhodnotenie 

TBA: vyhodnotenie slovné subjektívne na nejakých konkrétnych príkladoch. Vo vačšine projektov aj vyhodnotenie pomocou presnosti a pokrytia (precision a recall) (0,5-1 strana)

## Použitie

### Prerekvizity

- [python >= 3.8](https://www.python.org/downloads/) 
- [pipenv](https://pypi.org/project/pipenv/)

### Inštalácia a spustenie 

1. Nainštalujte závislosti použitím   

    ```
    pipenv install
    ```
    
1. Spustite Jupyter Notebook
  
    ```
    pipenv run jupyter notebook
    ```
