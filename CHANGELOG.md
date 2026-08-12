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
- Sei moduli in stato beta, per un totale di 51 regole, ciascuna riconducibile a una
  fonte registrata e dotata di una guardia esplicita contro i falsi positivi:
  `riuso` (12), `accessibilita` (9), `design-system` (8), `interoperabilita` (8),
  `sicurezza` (8), `dati-aperti` (6).
- Modulo `ia` in stato stub: le fonti risultavano in iter di adozione alle date di
  verifica, e la regola del progetto impedisce di derivarne controlli finche' lo stato
  non e' confermato.
- Delega agli strumenti ufficiali dell'ecosistema: `publiccode-parser-go`,
  `api-oas-checker-rules`, pa11y.
- Schema dei rilievi (`schema/finding.schema.json`), con obbligo di riferimento
  `file:line` per i rilievi inferiti e di elenco dei luoghi ispezionati per i mancati
  riscontri.
- Metodo di validazione empirica sul catalogo del riuso (`evaluation/README.md`), con
  criterio di promozione e criterio di abbandono fissati prima della prima esecuzione.
- Controllo di raggiungibilita' delle fonti che distingue il collegamento morto
  (404, 410, errore) dall'accesso automatico negato dai portali istituzionali
  (403 e simili, avviso), con possibilita' di dichiarare `url_check: skip`.
- Suite di 106 test sugli invarianti dell'artefatto (`tests/`), eseguita su tre versioni
  di Python, con distinzione esplicita rispetto alla validazione empirica dei giudizi,
  e soglia minima di copertura del codice eseguibile imposta in integrazione continua.
- Licenza EUPL-1.2 con nota esplicativa (`NOTICE.md`), codice di condotta, politica di
  sicurezza, identita' visiva.
