<div align="center">

<img src="assets/logo.svg" alt="pa-reviewer" width="396">

**Revisione del codice per la Pubblica Amministrazione italiana.**
Una skill che verifica il codice rispetto alle linee guida AgID e agli obblighi del Codice dell'Amministrazione Digitale.

[![CI](https://github.com/engineering87/pa-reviewer/actions/workflows/ci.yml/badge.svg)](https://github.com/engineering87/pa-reviewer/actions/workflows/ci.yml)
[![Licenza: EUPL-1.2](https://img.shields.io/badge/licenza-EUPL--1.2-0A4FA3.svg)](./LICENSE)
[![Fonti registrate](https://img.shields.io/badge/fonti-24%20registrate-1B6FD4.svg)](./sources.yml)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-5A6B7D.svg)](./SKILL.md)

*Progetto indipendente. Non affiliato, promosso né approvato da AgID, dal Dipartimento per la trasformazione digitale o da altre istituzioni. Non è uno strumento di certificazione.*

</div>

---

## Il problema

Un repository di software pubblico dichiara questo:

```yaml
# publiccode.yml
it:
  conforme:
    gdpr: yes
    misureMinimeSicurezza: yes
  piattaforme:
    spid: yes
```

Il validatore ufficiale lo accetta senza obiezioni, ed è corretto che sia così: il suo
compito è verificare che quelle chiavi esistano e siano ben formate.

**Nessuno verifica che siano vere.** Il repository può non contenere una sola riga di
integrazione SPID. Può scrivere codici fiscali nei log mentre dichiara il rispetto del
GDPR. Può tenere una stringa di connessione in chiaro mentre dichiara conformità alle
misure minime di sicurezza.

Lo stesso vale un livello più in alto. Un componente di interfaccia riscritto a mano al
posto di quello di Bootstrap Italia compila, sembra plausibile in una revisione
distratta, e perde silenziosamente la gestione da tastiera che il componente ufficiale
garantiva. Una specifica OpenAPI supera il checker del ModI mentre il controller che
dovrebbe realizzarla espone tre rotte non documentate.

`pa-reviewer` esiste per questo spazio: **la distanza fra ciò che un progetto dichiara
di essere e ciò che il codice è.**

## Cosa fa, e cosa deliberatamente non fa

| Fa | Non fa |
| --- | --- |
| Invoca i validatori ufficiali e ne cita l'output | Non ne riscrive la logica |
| Verifica la coerenza fra autodichiarazioni e codice | Non emette giudizi di conformità |
| Copre i domini privi di validatore, a partire dal design system | Non sostituisce uno strumento indisponibile con un'impressione |
| Ancora ogni rilievo a una fonte pubblica e a un `file:line` | Non deduce comportamenti dai nomi delle variabili |
| Dichiara sempre cosa non ha guardato | Non tratta procedure di gara, DPIA o conservazione documentale |

Dove esistono strumenti deterministici ufficiali, questo progetto **si toglie di
mezzo**: `publiccode-parser-go` per i metadati del riuso, `api-oas-checker-rules` per
le specifiche OpenAPI secondo il ModI, axe-core per l'accessibilità a runtime. Il
valore aggiunto sta in ciò che quegli strumenti, per costruzione, non possono vedere.

## Esempio di rilievo

> Output illustrativo del formato, non risultato di un'esecuzione reale.

```
Profilo rilevato: riuso, sicurezza | esclusi: design-system (nessuna interfaccia)
Copertura: 0 moduli stable, 1 beta, 5 stub

Sintesi: 1 important, 1 nit

-- riuso ---------------------------------------------------------------
[!]  RIU-005  src/api/UserController.cs:88
     Il progetto dichiara il rispetto del GDPR (publiccode.yml,
     it.conforme.gdpr), ma questa riga emette il codice fiscale
     dell'utente nel log applicativo.
     Fonte: Lo Standard publiccode.yml, estensioni nazionali.
     Evidenza: inferita dal codice.

[.]  RIU-006  publiccode.yml:41  (it.piattaforme.spid)
     Integrazione SPID dichiarata, nessun riscontro nel repository.
     Ricerca effettuata in: manifest delle dipendenze, configurazioni,
     variabili d'ambiente, manifest di deploy, client HTTP.
     Formulato come mancato riscontro: l'integrazione potrebbe risiedere
     in un componente esterno non incluso qui.

-- Adempimenti non verificabili dal codice -----------------------------
  *  Pubblicazione nel catalogo del riuso (art. 69 CAD): il codice non
     può dimostrarla.

-- Limiti di questa revisione ------------------------------------------
  *  Modulo riuso in stato beta: rilievi non ancora validati su campione.
  *  spectral non disponibile: verifica delle specifiche OpenAPI non
     eseguita.
```

La sezione che conta di più è l'ultima. Un revisore che non dichiara cosa non ha
guardato non è utilizzabile in sede di collaudo.

## Installazione

```bash
git clone https://github.com/engineering87/pa-reviewer.git \
  ~/.claude/skills/pa-reviewer
```

La skill si attiva quando si rivede codice destinato a un ente pubblico italiano, o
quando il repository presenta segnali riconoscibili: `publiccode.yml`, dipendenza da
`bootstrap-italia`, riferimenti a PDND, SPID, CIE, ANPR, pagoPA.

Strumenti opzionali, invocati se presenti: `publiccode-parser`, `spectral`, `pa11y`,
oppure `docker`. Quando mancano, la skill lo dichiara nel report.

## Stato dei moduli

| Modulo | Maturità | Copertura |
| --- | --- | --- |
| `riuso` | **beta** | coerenza `publiccode.yml` e codice, 12 regole |
| `design-system` | stub | perimetro mappato, nessun validatore esistente altrove |
| `accessibilita` | stub | perimetro mappato |
| `interoperabilita` | stub | perimetro mappato |
| `sicurezza` | stub | perimetro mappato |
| `dati-aperti` | stub | perimetro mappato |
| `ia` | stub | in attesa dell'adozione definitiva delle linee guida AgID |

**Uno stub non emette mai rilievi.** Dichiara che il dominio è applicabile e che la
copertura non è implementata. Il perimetro può essere completo anche quando
l'implementazione non lo è, purché la differenza sia visibile a chi legge il report.

Nessun modulo passa a `stable` senza precisione misurata e pubblicata in
[`evaluation/`](./evaluation/README.md).

## I quattro principi

**Provenienza pubblica.** Ogni regola poggia su una fonte pubblicamente accessibile,
registrata in [`sources.yml`](./sources.yml) con documento, atto, data, URL e livello
di verifica. Una regola senza fonte fa fallire la build. Nessun contributo può basarsi
su documentazione contrattuale o conoscenza interna di un'organizzazione: una regola
non verificabile da un terzo non serve a nessuno in collaudo.

**Nessun giudizio di conformità.** Il progetto produce evidenze e scostamenti. La
conformità richiede attestazioni formali che nessuno strumento automatico può
sostituire. Lo stesso limite è dichiarato dal checker ufficiale AgID per le API, che si
definisce esplicitamente non uno strumento di certificazione.

**Evidenza prima dell'affermazione.** Un'affermazione sul comportamento del codice
richiede una citazione `file:line`. Un mancato riscontro va formulato come tale,
dichiarando dove si è cercato, così che l'autore possa smentirlo in una riga anziché
litigare con lo strumento.

**Ancoraggio al codice.** Un dominio entra nel perimetro solo se produce rilievi
riferibili a una posizione nel codice. Il resto sono adempimenti, e stanno in una
sezione separata del report.

Politica completa: [`NORMATIVE_BASELINE.md`](./NORMATIVE_BASELINE.md).

## Manutenzione della baseline

Le fonti normative invecchiano, e in questo dominio lo fanno in fretta. La CI esegue un
controllo settimanale che **fa fallire la build** quando una fonte non è verificata da
oltre 180 giorni o quando una scadenza di revisione registrata è superata.

```bash
pip install pyyaml
python scripts/check_sources.py --sources sources.yml --rules rules/
```

La freschezza non è affidata alla buona volontà del manutentore.

## Struttura

```
pa-reviewer/
├── SKILL.md                  profilo, delega, contratto di output
├── sources.yml               registro delle fonti, unica fonte di verità
├── NORMATIVE_BASELINE.md     politica di provenienza e manutenzione
├── references/               un file per modulo, caricato su richiesta
├── rules/                    regole operative, ognuna con la sua fonte
├── schema/                   formato dei rilievi
├── scripts/                  gate di CI e delega agli strumenti ufficiali
├── evaluation/               metodo e risultati di validazione
└── assets/                   logo
```

## Licenza

Rilasciato sotto **[EUPL-1.2](./LICENSE)**, la European Union Public Licence.

In breve: puoi usare, studiare, modificare e ridistribuire il progetto, anche in ambito
commerciale; se distribuisci una versione modificata devi renderne disponibile il
sorgente sotto EUPL-1.2 o sotto una delle licenze compatibili elencate nella licenza
stessa; l'uso interno senza distribuzione a terzi non fa scattare alcun obbligo di
rilascio.

La scelta non è casuale. EUPL-1.2 è la licenza adottata dagli strumenti ufficiali
dell'ecosistema, è fra quelle certificate da Open Source Initiative come richiesto dalle
Linee guida su acquisizione e riuso di software per le PA, ed è un copyleft con un
elenco esplicito di licenze compatibili, quindi non crea isole per chi voglia
integrarlo. Le ragioni estese sono in [`NOTICE.md`](./NOTICE.md).

## Contribuire

Vedi [`CONTRIBUTING.md`](./CONTRIBUTING.md). Il vincolo di provenienza pubblica vale per
chiunque ed è verificato meccanicamente: non è una dichiarazione d'intenti.
