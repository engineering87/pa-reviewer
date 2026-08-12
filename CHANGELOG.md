# Changelog

Il formato segue [Keep a Changelog](https://keepachangelog.com/it-IT/1.1.0/) e il
progetto adotta il versionamento semantico.

Ogni voce che modifica la baseline normativa cita la determinazione, la versione o la
fonte che l'ha motivata.

## [0.1.0] - non ancora pubblicato

Primo rilascio.

- Registro delle fonti (`sources.yml`): 24 fonti su sette domini, ciascuna con ente
  emittente, atto, data, URL pubblico e livello di verifica esplicito.
- Politica di provenienza pubblica (`NORMATIVE_BASELINE.md`) e gate di integrazione
  continua (`scripts/check_sources.py`) che la rende un vincolo di build.
- Modulo `riuso` in stato beta: 12 regole di coerenza fra le autodichiarazioni di
  `publiccode.yml` e il codice, ciascuna con guardia esplicita contro i falsi positivi,
  e supporto a tutte le versioni dello standard accettate dal parser ufficiale.
- Sei moduli in stato stub, con perimetro mappato e condizioni di promozione dichiarate:
  `design-system`, `accessibilita`, `interoperabilita`, `sicurezza`, `dati-aperti`, `ia`.
- Delega agli strumenti ufficiali dell'ecosistema: `publiccode-parser-go`,
  `api-oas-checker-rules`, pa11y.
- Schema dei rilievi (`schema/finding.schema.json`), con obbligo di riferimento
  `file:line` per i rilievi inferiti e di elenco dei luoghi ispezionati per i mancati
  riscontri.
- Metodo di validazione empirica sul catalogo del riuso (`evaluation/README.md`), con
  criterio di promozione e criterio di abbandono fissati prima della prima esecuzione.
- Licenza EUPL-1.2 con nota esplicativa (`NOTICE.md`), codice di condotta, politica di
  sicurezza, identita' visiva.
