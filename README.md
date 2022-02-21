# muusi

client library for a certain musician website

## getting started

### install `muusi`

```
$ pip install git+https://github.com/santerj/muusi.git
```

### import `muusi` in your project

```
from muusi.search import Search

s = Search(url=my_search_url)
```

## whats `muusi`

tällä kirjastolla tehdään ohjelmallisesti hakuja muusikoiden.netin Torille. koska torissa ei ole mitään valmista tapaa luoda esim. hakuvahtia, tämän kirjaston voi integroida omaan ajastettuun notari/maili/yms toteutukseen ja kytätä hakuja automatisoidusti.

## how to

1. navigoi sivulle https://muusikoiden.net/tori/haku.php
2. räätälöi kälissä itsellesi mieleinen haku (mutta älä käytä osastona omaa valintaa).
3. tee haku ja kopioi url taltee  selaimen osoitepalkista
4. tee haku `muusi`lla:
    ```
    url = "https://muusikoiden.net/tori/haku.php?keyword=earthquaker+devices&category=56&type=sell"
    s = Search(url=url)
    pprint(json.dumps(s))  # view listings in json format
    ```
5. `muusi` palauttaa hakutulokset muodossa `list[dict]`. alla ilmoitus-objektin referenssitaulukko.


## object reference

| **Field** | **Type**        | **Explanation**                          |
|-----------|-----------------|------------------------------------------|
| link      | _String_        | URL of the listing                       |
| type      | _String_        | Selling, buying, etc                     |
| title     | _String_        |                                          |
| text      | _String_        | Body text. UNIX newlines                 |
| category  | _String_        |                                          |
| location  | _String_        |                                          |
| price     | _String_        | _Optional_ Trailing currency sign (€)    |
| images    | _Array[String]_ | Array of image URLs                      |
| created   | _String_        | DD.MM.YYYY                               |
| expires   | _String_        | DD.MM.YYYY                               |

## still here?

santerj ei ole yhteistyössä Muusikoiden Net ry:n tai sen jäsenten kanssa. santerj ei myöskään anna minkäänlaisia takuita tämän kirjaston toiminnasta. bugeista voi halutessaan tehdä issueita. älä ole pöljä.
