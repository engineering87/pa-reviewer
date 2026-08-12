# Modulo `dati-aperti`

Maturita': **stub**
Fonti: `DAT-DLGS36`, `DAT-LG-PATRIMONIO`, `DAT-DCAT-AP-IT`

## Stato

Perimetro mappato, nessun controllo attivo. **Questo modulo non emette finding.**
Quando il profilo lo attiva, il report dichiara: dominio applicabile, copertura non
ancora implementata.

## Perimetro previsto

- Conformita' dei metadati esposti al profilo nazionale DCAT-AP_IT, verificabile su serializzazioni JSON-LD, RDF/XML e Turtle.
- Coerenza delle licenze applicate ai dataset esposti con la raccomandazione delle Linee guida.
- Completezza degli elementi obbligatori del profilo negli endpoint di catalogo.

## Condizioni per passare a beta

1. Tutte le fonti del modulo in `sources.yml` portano `verification: verified`.
2. Ogni regola prevista e' ancorabile a `file:line`.
3. Le regole sono scritte in `rules/dati-aperti.yml` con guardia esplicita contro i falsi
   positivi.

## Condizioni per passare a stable

Precisione misurata su campione pubblico e pubblicata in `evaluation/`.
