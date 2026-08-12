# Modulo `riuso`

Maturita': **beta**
Fonti: `RIU-CAD-68-69`, `RIU-LG-SW`, `RIU-PUBLICCODE-SCHEMA`, `RIU-PUBLICCODE-PARSER`

## Perche' questo modulo esiste

L'art. 69 comma 1 del CAD impone alle amministrazioni titolari di software realizzato
su specifiche indicazioni del committente pubblico di renderne disponibile il codice
sorgente, completo della documentazione, in repertorio pubblico sotto licenza aperta.
Lo strumento operativo di quell'obbligo e' il file `publiccode.yml`, che alimenta il
catalogo del riuso.

L'estensione nazionale italiana dello schema contiene chiavi come `it.conforme.gdpr`,
`it.conforme.misureMinimeSicurezza`, `it.conforme.interoperabile`,
`it.piattaforme.spid`, `it.piattaforme.pagopa`. Sono **autodichiarazioni booleane**.

Il parser ufficiale `publiccode-parser-go` verifica che quelle chiavi esistano e siano
ben formate. **Non verifica che siano vere.** Un repository puo' dichiarare
`spid: yes` senza una riga di integrazione, o `misureMinimeSicurezza: yes` con
credenziali in chiaro.

Questo modulo verifica la corrispondenza fra dichiarazione e codice. E' l'unico
controllo del genere che conosciamo, ed e' il nucleo del progetto.

## Sequenza operativa

1. **Delega.** Esegui `scripts/run_publiccode_parser.sh`. Se il file e'
   sintatticamente invalido, riporta l'output del parser come finding
   `deterministic` e fermati: verificare la coerenza di un file malformato non ha
   senso.
2. **Inventario del codice.** Prima di valutare qualunque dichiarazione, costruisci
   l'inventario delle evidenze: manifest di dipendenze, file di configurazione,
   endpoint, client HTTP, librerie di autenticazione. Le regole seguenti si applicano
   a questo inventario, non a impressioni.
3. **Applica le regole** in `rules/riuso.yml`.
4. **Riporta.** Ogni scostamento cita la chiave dichiarata, il valore, e la riga di
   codice che lo contraddice o l'assenza documentata di evidenze.

## Come valutare una dichiarazione

Per ogni chiave dichiarata `yes`, cerca evidenza positiva nel codice. L'esito e' uno
di tre, e vanno tenuti distinti con rigore:

| Esito | Significato | Azione |
| --- | --- | --- |
| **Confermata** | evidenza trovata, con `file:line` | nessun finding |
| **Non riscontrata** | nessuna evidenza trovata dopo ricerca documentata | finding `nit`, formulato come assenza di riscontro |
| **Contraddetta** | evidenza che dimostra il contrario | finding `important` |

La distinzione fra "non riscontrata" e "contraddetta" e' la difesa principale contro
i falsi positivi. L'assenza di evidenza non e' evidenza di assenza: un'integrazione
puo' vivere in un modulo esterno al repository. Quando riporti un mancato riscontro,
**dichiara sempre dove hai cercato**, cosi' che l'autore possa smentirti in una riga.

## Versioni dello standard

Il modulo deve funzionare su repository che dichiarano qualunque versione accettata dal
parser ufficiale, non solo l'ultima. Le versioni supportate sono registrate nel campo
`supported_versions` della fonte `RIU-PUBLICCODE-PARSER` in `sources.yml`, rilevate dal
sorgente del parser e non da documentazione di terze parti.

Regole operative:

1. **Leggi `publiccodeYmlVersion` prima di qualunque altra chiave.** La struttura del
   file cambia fra versioni: risolvi i percorsi delle chiavi secondo la versione
   dichiarata, non secondo l'ultima.
2. **Una versione precedente non invalida il file.** Un repository che dichiara 0.2 o
   0.4 e' legittimo. Applica comunque tutte le regole di coerenza; segnala la versione
   superata come rilievo distinto, di severita' minima (RIU-012).
3. **Se una chiave attesa non esiste in quella versione, non emettere il rilievo.**
   Segnalare l'assenza di una chiave introdotta dopo la versione dichiarata e' un falso
   positivo, ed e' il modo piu' rapido per far disinstallare lo strumento.
4. **Il valore `"0"` significa "ultima versione".** Trattalo come tale, non come una
   versione anomala.

## Guardie contro i falsi positivi

- **Monorepo e microservizi.** Un `publiccode.yml` puo' descrivere una soluzione piu'
  ampia del singolo repository. Se il README o la chiave `dependsOn` indicano
  componenti esterni, declassa i mancati riscontri a informativi.
- **Codice di test e fixture.** Segreti apparenti in file di test o esempi non sono
  violazioni delle misure minime. Verifica il percorso prima di segnalare.
- **Integrazioni mediate.** SPID puo' arrivare tramite un proxy di autenticazione o
  un gateway dell'ente, senza codice SAML nel repository. Cerca anche configurazioni,
  variabili d'ambiente e manifest di deploy prima di concludere.
- **Repository archiviati.** Se `developmentStatus` e' `obsolete`, riporta solo i
  rilievi `important`.

## Cosa questo modulo non fa

- Non giudica se l'amministrazione sia titolare del software ai sensi dell'art. 69:
  e' una valutazione contrattuale, fuori perimetro.
- Non verifica l'avvenuta pubblicazione nel catalogo del riuso: e' un adempimento,
  non un fatto del codice. Compare al piu' fra i promemoria.
- Non sceglie la licenza. Le Linee guida definiscono al par. 3.5.3 un albero
  decisionale, e la licenza va scelta fra quelle certificate da Open Source
  Initiative: il modulo verifica la coerenza interna fra quanto dichiarato e i file
  presenti, non la correttezza della scelta.

## Campione di validazione

Il catalogo del riuso e' un corpus pubblico di repository contenenti `publiccode.yml`,
pubblico per obbligo di legge. E' il banco di prova per misurare precisione e richiamo
di questo modulo prima di promuoverlo a `stable`. Metodo e risultati in
`evaluation/README.md`.
