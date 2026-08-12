---
name: pa-reviewer
description: >
  Revisione del codice di progetti destinati alla Pubblica Amministrazione italiana
  rispetto alle linee guida AgID e agli obblighi del Codice dell'Amministrazione
  Digitale: riuso e publiccode.yml, design system Bootstrap Italia, accessibilita'
  (EAA, EN 301 549, WCAG), interoperabilita' ModI e PDND, sviluppo sicuro, dati
  aperti DCAT-AP_IT. Usa questa skill ogni volta che si rivede, si scrive o si
  verifica codice per un ente pubblico italiano, o quando compaiono termini come
  AgID, CAD, publiccode.yml, Bootstrap Italia, Designers Italia, PDND, ModI, SPID,
  CIE, ANPR, pagoPA, riuso, catalogo del riuso, dichiarazione di accessibilita',
  Legge Stanca, Piano Triennale. Usala anche quando l'utente chiede genericamente
  una revisione di codice e il repository contiene un publiccode.yml, una
  dipendenza da bootstrap-italia, o riferimenti a piattaforme abilitanti nazionali.
license: EUPL-1.2
---

# pa-reviewer

Revisione di codice per progetti della Pubblica Amministrazione italiana.

Questa skill **non e' uno strumento di certificazione** e **non emette mai un
giudizio di conformita'**. Produce evidenze e scostamenti, ciascuno ancorato a una
fonte pubblica e a una posizione nel codice.

## 1. Prima di tutto: determina il profilo

Nessun progetto e' soggetto all'intero perimetro. Ispeziona il repository e attiva
solo i moduli pertinenti.

| Segnale rilevato | Modulo da attivare |
| --- | --- |
| `publiccode.yml` presente, o repository di titolarita' pubblica | `riuso` |
| dipendenza `bootstrap-italia`, kit React/Angular Italia, UI Kit | `design-system` |
| qualunque interfaccia web o mobile rivolta all'utenza | `accessibilita` |
| file OpenAPI, integrazione PDND, e-service | `interoperabilita` |
| sempre, se il progetto e' destinato a un ente pubblico | `sicurezza` |
| esposizione di cataloghi dati, endpoint dataset, metadati | `dati-aperti` |
| componenti di intelligenza artificiale nel perimetro del servizio | `ia` |

**Dichiara sempre nel report i moduli che hai escluso e perche'.** Un revisore che
non spiega cosa non ha guardato non e' utilizzabile in collaudo.

Se il profilo e' ambiguo, chiedi all'utente anziche' indovinare.

## 2. Delega agli strumenti ufficiali

Dove esiste un validatore deterministico ufficiale, **invocalo e cita il suo
output**. Non replicarne la logica: produrresti un risultato peggiore e destinato a
divergere.

| Dominio | Strumento | Script |
| --- | --- | --- |
| `riuso` | `italia/publiccode-parser-go` | `scripts/run_publiccode_parser.sh` |
| `interoperabilita` | `italia/api-oas-checker-rules` | `scripts/run_oas_checker.sh` |
| `accessibilita` | axe-core / pa11y | `scripts/run_axe.sh` |

Se lo strumento non e' disponibile nell'ambiente, dichiaralo nel report come
copertura mancante. Non sostituirlo con un giudizio a occhio presentato come
equivalente.

Il valore aggiunto di questa skill sta in cio' che quegli strumenti non possono
fare: la coerenza fra cio' che il progetto **dichiara** di essere e cio' che il
codice **e'**.

## 3. Leggi il modulo prima di applicarlo

Ogni modulo ha un file di riferimento in `references/`. Caricalo solo quando il
profilo lo richiede.

| Modulo | Riferimento | Maturita' |
| --- | --- | --- |
| `riuso` | `references/riuso.md` | beta |
| `design-system` | `references/design-system.md` | stub |
| `accessibilita` | `references/accessibilita.md` | stub |
| `interoperabilita` | `references/interoperabilita.md` | stub |
| `sicurezza` | `references/sicurezza.md` | stub |
| `dati-aperti` | `references/dati-aperti.md` | stub |
| `ia` | `references/ia.md` | stub |

**Un modulo `stub` non emette mai finding.** Dichiara nel report che il dominio e'
applicabile e che la copertura non e' ancora implementata. Un modulo `beta` emette
finding contrassegnati come non validati empiricamente.

## 4. Contratto di output

Ogni finding porta obbligatoriamente:

- `rule`: identificativo della regola
- `source`: identificativo della fonte in `sources.yml`, che va citata per esteso
  nel testo (documento, atto, data)
- `location`: `file:line`, oppure `file` quando il rilievo riguarda l'assenza di un
  file
- `evidence`: uno fra
  - `deterministic` — prodotto da uno strumento ufficiale, ne riporti l'output
  - `inferred` — dedotto dalla lettura del codice, con la citazione che lo sostiene
  - `not_verifiable` — adempimento che il codice non puo' dimostrare
- `severity`: `important`, `nit`, `pre_existing`, resi nel report rispettivamente con i
  marcatori `[!]`, `[·]`, `[~]`

Regola di evidenza, non negoziabile: **un'affermazione sul comportamento del codice
richiede una citazione `file:line`, mai un'inferenza dai nomi.** Se non riesci a
indicare la riga che lo dimostra, non emettere il finding.

I rilievi `not_verifiable` non sono finding. Vanno in una sezione separata del
report intitolata "Adempimenti non verificabili dal codice", come promemoria.

Formato completo in `schema/finding.schema.json`.

## 5. Struttura del report

```
Profilo rilevato: <moduli attivi> | esclusi: <moduli> (motivo)
Copertura: <moduli stable> stable, <n> beta, <n> stub

Sintesi: N important, M nit, K pre-esistenti

[finding, raggruppati per modulo]

Adempimenti non verificabili dal codice
[promemoria, senza severita']

Limiti di questa revisione
[strumenti non disponibili, moduli stub, fonti non verificate]
```

La sezione sui limiti e' obbligatoria anche quando non ci sono finding.

## 6. Vincoli non negoziabili

1. **Mai un giudizio di conformita'.** Non scrivere "conforme", "non conforme",
   "adeguato alle linee guida". Scrivi cosa hai osservato e a quale fonte si
   riferisce.
2. **Mai una regola senza fonte pubblica.** Se un rilievo non e' riconducibile a un
   `id` presente in `sources.yml`, non appartiene a questa skill.
3. **Mai il silenzio sulla copertura mancante.** Uno stub dichiarato vale piu' di
   una copertura implicita.
4. **Mai sostituire uno strumento ufficiale indisponibile** con un giudizio
   presentato come equivalente.

Politica completa in `NORMATIVE_BASELINE.md`.
