# Baseline normativa

Questo documento definisce **da dove viene ogni regola** di questo progetto e **come si
mantiene allineata** nel tempo. Non contiene regole: contiene la politica che governa la
loro ammissibilità.

Data della baseline: **2026-08-12**
Registro delle fonti: [`sources.yml`](./sources.yml)

---

## 1. Vincolo di provenienza pubblica

Una regola di questo progetto può basarsi **esclusivamente** su fonti pubblicamente
accessibili: normativa, linee guida, determinazioni, documentazione tecnica ufficiale e
repository aperti.

Sono espressamente escluse, indipendentemente da chi le proponga:

- documentazione contrattuale, capitolati, requisiti di gara, propri o di terzi
- codice, architetture, convenzioni o nomi di progetto non pubblicati
- fixture di test derivate da sistemi reali, anche se anonimizzate
- conoscenza del funzionamento interno di una specifica amministrazione o fornitore,
  quando tale conoscenza derivi da un rapporto professionale anziché da fonte pubblica

Il vincolo non è soltanto deontologico. Una regola giustificata da conoscenza non
pubblica non è verificabile da un terzo, e una regola non verificabile non è citabile in
un verbale di collaudo. Il vincolo e l'obiettivo del progetto coincidono.

Il rispetto del vincolo non è affidato alla buona fede: è verificato in CI
(sezione 4).

---

## 2. Livelli di verifica

Ogni fonte in `sources.yml` porta un livello di verifica esplicito.

| Livello | Significato | Uso ammesso |
| --- | --- | --- |
| `verified` | Documento o pagina primaria consultata direttamente. L'affermazione associata è attestata da quella pagina. | Può fondare regole in moduli `stable` |
| `cited` | Riferimento riportato da una fonte secondaria attendibile; la primaria non è stata ancora consultata. | Può fondare regole solo in moduli `beta`, con avviso nel report |
| `unverified` | Segnaposto di perimetro. | Nessuna regola può basarsi su di esso |

**Regola dura:** un modulo non può essere dichiarato `stable` se una qualsiasi delle sue
regole poggia su una fonte `cited` o `unverified`.

---

## 3. Maturità dei moduli

Ogni modulo dichiara il proprio stato, nel frontmatter della skill e in coda a ogni
report.

| Stato | Significato | Comportamento |
| --- | --- | --- |
| `stable` | Regole verificate su campione reale, precisione misurata e pubblicata | Emette finding |
| `beta` | Regole scritte, non ancora validate empiricamente | Emette finding contrassegnati come non validati |
| `stub` | Perimetro mappato, nessun controllo attivo | **Non emette mai finding.** Dichiara nel report: dominio applicabile, copertura non ancora implementata |

Uno stub silenzioso è vietato. Il perimetro dichiarato può essere completo anche quando
l'implementazione non lo è, purché la differenza sia visibile a chi legge il report.

Stato al 2026-08-12:

| Modulo | Maturità |
| --- | --- |
| `riuso` | beta |
| `accessibilita` | stub |
| `design-system` | stub |
| `interoperabilita` | stub |
| `sicurezza` | stub |
| `dati-aperti` | stub |
| `ia` | stub |

---

## 4. Gate di provenienza in CI

Ogni regola porta un campo `source` obbligatorio che riferisce un `id` presente in
`sources.yml`:

```yaml
- id: BI-COMP-001
  source: DES-BI-DOCS
  severity: warning
```

Lo script [`scripts/check_sources.py`](./scripts/check_sources.py) fa fallire la build quando:

1. una regola non dichiara `source`, oppure riferisce un `id` inesistente
2. una fonte manca di uno dei campi obbligatori (`document`, `url`, `verification`, `retrieved`)
3. un `url` non usa schema `https`
4. una regola in un modulo `stable` poggia su una fonte `cited` o `unverified`
5. una fonte ha `retrieved` più vecchio di 180 giorni, o un `review_by` superato

Il controllo di raggiungibilita' degli URL (`--check-urls`) e' separato e piu'
prudente: fallisce solo su `404` e `410`, cioe' su fonti effettivamente sparite. I
portali istituzionali sono spesso protetti da un WAF che risponde `403` alle richieste
automatiche pur servendo regolarmente la pagina a un browser: quello e' un avviso da
verificare a mano, non un collegamento morto. Una fonte che blocchi stabilmente le
verifiche puo' dichiarare `url_check: skip` con `url_check_reason`.

I punti 4 e 5 sono la parte che conta: rendono la manutenzione della baseline un
fallimento di build anziché un proposito.

---

## 5. Delega agli strumenti ufficiali

Dove esiste un validatore deterministico ufficiale, la skill **lo invoca e ne cita
l'output**; non ne replica la logica. Le fonti con `delegation: true` in `sources.yml`
segnano questi confini.

| Dominio | Strumento ufficiale | Ruolo residuo della skill |
| --- | --- | --- |
| Interoperabilità API | `italia/api-oas-checker-rules` (Spectral) | Scostamento tra specifica OpenAPI e implementazione |
| Riuso | `italia/publiccode-parser-go` | Verità delle autodichiarazioni rispetto al codice |
| Accessibilità | axe-core, pa11y | Semantica su diff, componenti custom, overlay |

Replicare un linter ufficiale produce output peggiore e obsolescenza garantita.

---

## 6. Perimetro negativo

Un dominio entra nel perimetro solo se produce almeno un finding ancorabile a
`file:line`. Se il migliore enunciato possibile è un adempimento organizzativo, il
dominio resta fuori e compare al più come promemoria in coda al report.

L'elenco vincolante è in `sources.yml`, sezione `out_of_scope`.

**La skill non emette mai un giudizio di conformità.** Produce evidenze e scostamenti.
La conformità, dove prevista, richiede attestazioni formali che nessuno strumento
automatico può sostituire. Lo stesso limite è dichiarato dal checker ufficiale AgID per
le API, che si definisce esplicitamente non uno strumento di certificazione.

---

## 7. Processo di aggiornamento

- **Trimestrale:** rilettura delle fonti con `retrieved` più vecchio di 180 giorni.
- **Su evento:** pubblicazione di una nuova determinazione AgID nei domini mappati.
- **Scadenze note:** le fonti con `review_by` valorizzato vanno ricontrollate entro quella
  data. Al 2026-08-12 riguardano l'aggiornamento atteso della norma armonizzata
  EN 301 549 e lo stato di adozione delle linee guida AgID sull'intelligenza artificiale.

Ogni aggiornamento della baseline produce una voce nel `CHANGELOG.md` che cita la
determinazione o la versione che lo ha motivato. La cronologia di manutenzione è parte
della credibilità del progetto quanto le regole stesse.

---

## 8. Verifiche aperte

Stato delle questioni note alla data della baseline. Non sono difetti da correggere ma
punti la cui risoluzione dipende da eventi esterni al progetto.

| Questione | Effetto | Scadenza |
| --- | --- | --- |
| La documentazione di Bootstrap Italia indica la versione 2.18.2, npm pubblica la 2.18.3 | Le regole che dipendono dalla versione usano npm come riferimento e tollerano lo scarto minore | nessuna |
| Aggiornamento atteso della norma armonizzata EN 301 549, con possibile passaggio del riferimento web alle WCAG 2.2 AA | Il modulo `accessibilita` non puo' passare a beta prima della verifica | 2026-11-30 |
| Le linee guida AgID sull'intelligenza artificiale risultano in iter di adozione alle date di verifica registrate | Il modulo `ia` resta stub, nessuna regola puo' derivarne | 2026-09-30 |
| Estremi delle determinazioni di adozione non ancora reperiti per alcune fonti (linee guida di design, ModI, sviluppo del software sicuro, raccomandazioni TLS) | Quelle fonti restano `cited`, quindi non possono fondare moduli `stable` | nessuna |

Le scadenze sono registrate nel campo `review_by` delle rispettive fonti e vengono fatte
valere dal controllo settimanale in integrazione continua.

## 9. Indipendenza

Questo progetto non è affiliato, promosso né approvato da AgID, dal Dipartimento per la
trasformazione digitale, dall'Agenzia per la Cybersicurezza Nazionale o da qualsiasi
altra istituzione. Non è uno strumento di certificazione. È un ausilio alla revisione del
codice, e le sue segnalazioni non sostituiscono alcuna verifica formale prevista dalla
normativa.
