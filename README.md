<div align="center">

<img src="assets/logo.svg" alt="pa-reviewer" width="396">

### Revisione del codice per la Pubblica Amministrazione italiana

Una *agent skill* che verifica il codice destinato agli enti pubblici rispetto alle linee guida nazionali e agli obblighi del Codice dell'Amministrazione Digitale.

[![CI](https://github.com/engineering87/pa-reviewer/actions/workflows/ci.yml/badge.svg)](https://github.com/engineering87/pa-reviewer/actions/workflows/ci.yml)
[![Licenza](https://img.shields.io/badge/licenza-EUPL--1.2-0A4FA3.svg)](./LICENSE)
[![Fonti](https://img.shields.io/badge/fonti-24%20registrate-1B6FD4.svg)](./sources.yml)
[![Stato](https://img.shields.io/badge/stato-development-5A6B7D.svg)](./CHANGELOG.md)

<sub>Progetto indipendente. Non affiliato, promosso né approvato da AgID, dal Dipartimento per la trasformazione digitale o da altre istituzioni.<br>**Non è uno strumento di certificazione e non emette giudizi di conformità.**</sub>

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

Lo stesso vale un livello più in alto. Un componente riscritto a mano al posto di quello
di Bootstrap Italia compila, sembra plausibile in una revisione distratta, e perde
silenziosamente la gestione da tastiera che il componente ufficiale garantiva. Una
specifica OpenAPI supera il checker del ModI mentre il controller che dovrebbe
realizzarla espone tre rotte non documentate.

`pa-reviewer` lavora esattamente in questo spazio: **la distanza fra ciò che un progetto
dichiara di essere e ciò che il codice è.**

## Come funziona

```mermaid
flowchart LR
    A[Repository] --> B{Profilo}
    B -->|publiccode.yml| C[riuso]
    B -->|bootstrap-italia| D[design-system]
    B -->|OpenAPI, PDND| E[interoperabilita]
    B -->|interfaccia| F[accessibilita]
    C & D & E & F --> G[Delega ai<br/>validatori ufficiali]
    G --> H[Verifica di coerenza<br/>dichiarazione ↔ codice]
    H --> I[Report]
    I --> J[Rilievi con fonte<br/>e file:line]
    I --> K[Adempimenti non<br/>verificabili dal codice]
    I --> L[Limiti della<br/>revisione]
```

**1. Determina il profilo.** Nessun progetto è soggetto all'intero perimetro. La skill
ispeziona il repository, attiva solo i moduli pertinenti e dichiara quali ha escluso.

**2. Delega dove esiste uno strumento ufficiale.** `publiccode-parser-go` per i metadati
del riuso, `api-oas-checker-rules` per le specifiche OpenAPI secondo il ModI, axe-core
per l'accessibilità a runtime. Questo progetto non ne riscrive la logica: li invoca e ne
cita l'output.

**3. Verifica ciò che quegli strumenti non possono vedere.** La coerenza fra
autodichiarazioni e codice, i domini privi di validatore, lo scostamento fra specifica di
interfaccia e implementazione.

## Esempio di rilievo

> Output illustrativo del formato, non risultato di un'esecuzione reale.

```text
Profilo rilevato: riuso, sicurezza | esclusi: design-system (nessuna interfaccia)
Copertura: 0 moduli stable, 1 beta, 5 stub

Sintesi: 1 important, 1 nit

── riuso ───────────────────────────────────────────────────────────────
[!] RIU-005   src/api/UserController.cs:88
    Il progetto dichiara il rispetto del GDPR (publiccode.yml,
    it.conforme.gdpr), ma questa riga emette il codice fiscale
    dell'utente nel log applicativo.
    Fonte: Lo Standard publiccode.yml, estensioni nazionali.
    Evidenza: inferita dal codice.

[·] RIU-006   publiccode.yml:41  (it.piattaforme.spid)
    Integrazione SPID dichiarata, nessun riscontro nel repository.
    Ricerca effettuata in: manifest delle dipendenze, configurazioni,
    variabili d'ambiente, manifest di deploy, client HTTP.
    Formulato come mancato riscontro: l'integrazione potrebbe risiedere
    in un componente esterno non incluso qui.

── Adempimenti non verificabili dal codice ─────────────────────────────
    Pubblicazione nel catalogo del riuso (art. 69 CAD).

── Limiti di questa revisione ──────────────────────────────────────────
    Modulo riuso in stato beta: rilievi non ancora validati su campione.
    spectral non disponibile: specifiche OpenAPI non verificate.
```

La sezione che conta di più è l'ultima. Un revisore che non dichiara cosa non ha
guardato non è utilizzabile in sede di collaudo.

## Installazione

**Nel repository del progetto** (consigliata per il lavoro di squadra: la skill viaggia
con il codice e resta disponibile anche nelle sessioni cloud e nelle routine, dove le
skill personali non vengono caricate):

```bash
git clone https://github.com/engineering87/pa-reviewer.git \
  .claude/skills/pa-reviewer
```

**Nella libreria personale** (disponibile in tutti i progetti della tua macchina):

```bash
git clone https://github.com/engineering87/pa-reviewer.git \
  ~/.claude/skills/pa-reviewer
```

Per aggiornare, `git pull` nella cartella. Per disinstallare, rimuoverla.

Verifica che sia stata riconosciuta chiedendo quali skill sono disponibili, oppure con
`/doctor`.

### Strumenti opzionali

La skill funziona senza, ma delega volentieri dove può. Quando uno strumento manca, lo
dichiara nel report anziché sostituirlo con un'impressione.

| Strumento | Serve per | Installazione |
| :--- | :--- | :--- |
| `publiccode-parser` | validazione di `publiccode.yml` | `go install github.com/italia/publiccode-parser-go/v5/publiccode-parser@latest` |
| `spectral` | specifiche OpenAPI secondo il ModI | `npm install -g @stoplight/spectral-cli` |
| `pa11y` | accessibilità a runtime | `npm install -g pa11y` |

In alternativa basta `docker`: gli script di delega usano le immagini ufficiali quando
il binario non è presente.

## Uso

La skill si attiva da sola quando il contesto lo richiede: codice destinato a un ente
pubblico italiano, oppure un repository che presenta segnali riconoscibili come
`publiccode.yml`, una dipendenza da `bootstrap-italia`, riferimenti a PDND, SPID, CIE,
ANPR o pagoPA.

Per invocarla esplicitamente basta chiederlo:

```text
/pa-reviewer

Rivedi le modifiche di questo branch per il progetto di un ente pubblico.
Verifica la coerenza del publiccode.yml con il codice.
```

Funziona su un diff, su un branch o sull'intero repository. Su un repository grande
conviene restringere il campo: la revisione è tanto più utile quanto più è specifica.

### Come si legge il report

Il report ha sempre tre sezioni, nell'ordine: i rilievi, gli adempimenti che il codice
non può dimostrare, i limiti della revisione stessa.

Ogni rilievo porta una **severità**:

| | Severità | Significato |
| :--- | :--- | :--- |
| `[!]` | **important** | scostamento che andrebbe risolto prima del rilascio |
| `[·]` | **nit** | rilievo minore, utile ma non bloccante |
| `[~]` | **pre_existing** | preesistente nel codice, non introdotto dalla modifica in esame |

e un **livello di evidenza**, che dice quanto puoi fidarti del rilievo:

| Evidenza | Significato | Come trattarla |
| :--- | :--- | :--- |
| `deterministic` | prodotta da uno strumento ufficiale, con il suo output | affidabile, discutine con lo strumento |
| `inferred` | dedotta dal codice, con citazione `file:line` | verifica la riga citata |
| `not_verifiable` | adempimento che il codice non può dimostrare | non è un rilievo, è un promemoria |

I mancati riscontri elencano sempre **dove la skill ha cercato**. Se l'integrazione che
cerca vive altrove, quella riga ti basta per smentirla senza discutere.

### Risoluzione dei problemi

<details>
<summary><b>La skill non si attiva</b></summary>

Verifica che sia visibile con `/doctor` o chiedendo quali skill sono disponibili. Se non
compare, controlla che il percorso sia `.claude/skills/pa-reviewer/SKILL.md` oppure
`~/.claude/skills/pa-reviewer/SKILL.md`: il file deve stare dentro una cartella con il
nome della skill, non nella radice.

Se è visibile ma non interviene, cita nel messaggio uno dei termini che la attivano
(`publiccode.yml`, linee guida, PA, PDND) oppure invocala esplicitamente.

</details>

<details>
<summary><b>La skill non compare in una sessione cloud o in una routine</b></summary>

Le skill personali non vengono caricate in quelle sessioni. Installala nel repository,
sotto `.claude/skills/`, oppure abilitala per il tuo account.

</details>

<details>
<summary><b>Un rilievo è sbagliato</b></summary>

Apri una issue citando la riga del report e il `file:line` contestato. Un falso positivo
è un difetto della regola, non un caso limite da tollerare: ogni regola deve avere una
guardia esplicita, e se non ha funzionato va corretta o disattivata.

</details>

<details>
<summary><b>Il report dice che uno strumento non è disponibile</b></summary>

È il comportamento previsto, non un errore. Installa lo strumento dalla tabella qui
sopra, oppure accetta la copertura ridotta: resta dichiarata nella sezione sui limiti,
così chi legge il report sa cosa non è stato verificato.

</details>

### Compatibilità con altri agenti

`SKILL.md` non è un formato proprietario: è la specifica aperta Agent Skills, e diversi
agenti oltre a Claude Code la leggono, con cartelle analoghe (`.openclaw/skills/`,
`~/.agents/skills/` e altre a seconda dello strumento).

Questa skill è scritta per essere portabile: il frontmatter usa solo campi della
specifica, il corpo è markdown senza funzionalità legate a un singolo agente, e i
riferimenti ai moduli sono percorsi relativi ordinari. **Non è però stata provata al di
fuori di Claude Code**, quindi il progetto non dichiara una compatibilità che non ha
verificato. Riscontri di funzionamento altrove sono benvenuti in una issue.

Un vincolo vale comunque, indipendentemente dall'agente: la delega agli strumenti
ufficiali richiede l'esecuzione di comandi di shell. Dove non è disponibile, la parte
deterministica non gira e resta la sola verifica di coerenza per lettura del codice. La
differenza compare nella sezione sui limiti del report, come ogni altra copertura
mancante.

## Moduli

| Modulo | Stato | Copertura |
| :--- | :--- | :--- |
| `riuso` | **beta** | coerenza fra `publiccode.yml` e codice, 12 regole |
| `design-system` | stub | perimetro mappato, nessun validatore esistente altrove |
| `accessibilita` | stub | perimetro mappato |
| `interoperabilita` | stub | perimetro mappato |
| `sicurezza` | stub | perimetro mappato |
| `dati-aperti` | stub | perimetro mappato |
| `ia` | stub | in attesa dell'adozione definitiva delle linee guida |

Uno **stub** non emette mai rilievi: dichiara che il dominio è applicabile e che la
copertura non è implementata. Il perimetro può essere completo anche quando
l'implementazione non lo è, purché la differenza sia visibile a chi legge il report.

Il passaggio a **stable** richiede precisione misurata e pubblicata in
[`evaluation/`](./evaluation/README.md). Nessuna promozione senza numeri.

## Principi

> **Provenienza pubblica.** Ogni regola poggia su una fonte pubblicamente accessibile,
> registrata in [`sources.yml`](./sources.yml) con documento, atto, data, URL e livello
> di verifica. Una regola senza fonte fa fallire la build.

> **Nessun giudizio di conformità.** Il progetto produce evidenze e scostamenti. La
> conformità richiede attestazioni formali che nessuno strumento automatico può
> sostituire.

> **Evidenza prima dell'affermazione.** Un'affermazione sul comportamento del codice
> richiede una citazione `file:line`. Un mancato riscontro va formulato come tale,
> dichiarando dove si è cercato, così che l'autore possa smentirlo in una riga.

> **Ancoraggio al codice.** Un dominio entra nel perimetro solo se produce rilievi
> riferibili a una posizione nel codice. Procedure di gara, DPIA, conservazione
> documentale e qualificazione cloud restano fuori: sono adempimenti.

Politica completa in [`NORMATIVE_BASELINE.md`](./NORMATIVE_BASELINE.md).

## Manutenzione della baseline

Le fonti normative invecchiano, e in questo dominio lo fanno in fretta. La CI esegue un
controllo settimanale che **fa fallire la build** quando una fonte non è verificata da
oltre 180 giorni o quando una scadenza di revisione registrata è superata. La freschezza
non è affidata alla buona volontà del manutentore.

```bash
pip install pyyaml
python scripts/check_sources.py --sources sources.yml --rules rules/
python scripts/check_sources.py --sources sources.yml --check-urls
```

<details>
<summary><b>Struttura del repository</b></summary>

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
└── assets/                   identità visiva
```

</details>

<details>
<summary><b>Perimetro escluso, e perché</b></summary>

Un dominio entra solo se produce rilievi ancorabili a una posizione nel codice. Restano
deliberatamente fuori:

| Escluso | Motivo |
| :--- | :--- |
| Procedure di gara, valutazione comparativa ex art. 68 CAD | non ancorabili a `file:line` |
| Valutazione d'impatto sulla protezione dei dati | adempimento organizzativo |
| Processi di conservazione documentale | organizzativi, non di codice |
| Qualificazione dei servizi cloud | procedura amministrativa presso ACN |
| Attestazioni e dichiarazioni di accessibilità | richiedono sottoscrizione formale |

L'elenco vincolante è in [`sources.yml`](./sources.yml), sezione `out_of_scope`.

</details>

## Licenza

Rilasciato sotto **[EUPL-1.2](./LICENSE)**, la European Union Public Licence.

Puoi usare, studiare, modificare e ridistribuire il progetto, anche in ambito
commerciale. Se distribuisci una versione modificata devi renderne disponibile il
sorgente sotto EUPL-1.2 o sotto una delle licenze compatibili elencate nella licenza
stessa; l'uso interno senza distribuzione a terzi non fa scattare alcun obbligo.

La scelta non è casuale: EUPL-1.2 è adottata dagli strumenti ufficiali dell'ecosistema,
è fra quelle certificate da Open Source Initiative come richiesto dalle Linee guida su
acquisizione e riuso di software per le PA, ed è un copyleft con un elenco esplicito di
licenze compatibili, quindi non crea isole per chi voglia integrarlo. Le ragioni estese
sono in [`NOTICE.md`](./NOTICE.md).

## Contribuire

Le regole si aggiungono partendo dalla fonte, mai dal codice: prima la voce in
`sources.yml`, poi la regola che la riferisce, sempre con una guardia esplicita contro i
falsi positivi. Il vincolo di provenienza pubblica vale per chiunque ed è verificato
meccanicamente in CI: non è una dichiarazione d'intenti.

Dettagli in [`CONTRIBUTING.md`](./CONTRIBUTING.md), regole di convivenza in
[`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md), segnalazioni di sicurezza in
[`SECURITY.md`](./SECURITY.md).
