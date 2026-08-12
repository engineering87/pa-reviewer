# Modulo `interoperabilita`

Maturita': **beta**
Fonti: `INT-MODI`, `INT-OAS-CHECKER`

## Perche' questo modulo esiste

Il checker ufficiale legge la specifica. Nessuno legge il codice che dovrebbe
realizzarla. Una specifica puo' superare la verifica con zero errori mentre
l'implementazione espone rotte non documentate, restituisce esiti diversi da quelli
dichiarati o non applica lo schema di sicurezza previsto. Lo scostamento fra i due lati
del contratto e' il contenuto di questo modulo.

## Sequenza operativa

1. **Delega.** Esegui `scripts/run_oas_checker.sh` sulla specifica. Se restituisce
   errori, riportali cosi' come sono e considera che il confronto con il codice poggia
   su un contratto gia' difettoso.
2. **Costruisci i due inventari.** Le rotte dichiarate nella specifica e quelle
   effettivamente esposte dal codice, con metodo, percorso, parametri ed esiti.
3. **Confronta nelle due direzioni.** Implementato e non documentato, documentato e non
   implementato: sono rilievi diversi, con severita' diverse.
4. **Riporta** citando entrambe le posizioni.

## Guardie contro i falsi positivi

- **Rotte tecniche.** Sonde di stato, metriche e diagnostica non appartengono al
  contratto pubblico.
- **Gestione centralizzata.** Esiti ed errori sono spesso prodotti da un gestore comune,
  non dal controller: cercarlo prima di segnalare una divergenza.
- **Sicurezza applicata altrove.** Autenticazione e autorizzazione vivono in filtri,
  intercettori o gateway. Un rilievo si emette solo dopo aver ispezionato la catena, ed
  elencando i punti esaminati.
- **Specifiche generate a compilazione.** Il file versionato puo' non essere quello
  pubblicato: verificare come viene prodotto.

## Cosa questo modulo non fa

Non replica alcuna regola del checker ufficiale. Non valuta la piena aderenza al modello
di interoperabilita', che comprende profili e considerazioni non desumibili dal codice.

## Condizioni per passare a stable

1. Tutte le fonti del modulo portano `verification: verified`.
2. Precisione per regola misurata su campione pubblico e pubblicata in
   `evaluation/`, con nessuna regola sotto la soglia fissata.
3. Nessuna regola con guardia rivelatasi insufficiente durante la validazione.
