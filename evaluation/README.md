# Validazione empirica

Nessun modulo passa a `stable` senza numeri pubblicati qui.

## Corpus

Il catalogo del riuso di Developers Italia indicizza repository contenenti
`publiccode.yml`. Quel corpus esiste perche' l'art. 69 comma 1 del CAD impone alle
amministrazioni titolari di software realizzato su specifiche indicazioni del
committente pubblico di renderne disponibile il codice sorgente in repertorio pubblico
sotto licenza aperta.

Ne discendono due proprieta' utili:

1. Il campione e' **pubblico per obbligo di legge**, quindi coerente con il vincolo di
   provenienza del progetto.
2. Chiunque puo' **riprodurre** la misura, che e' la condizione perche' i numeri
   significhino qualcosa.

## Metodo

1. Selezione di un campione casuale di repository dal catalogo, con seme registrato.
2. Riferimento ai repository tramite URL e hash di commit. **Le fixture non vengono
   copiate nel progetto:** le licenze dei repository del catalogo variano, e un
   riferimento immutabile evita sia il problema di licenza sia la deriva del campione.
3. Esecuzione del modulo su ciascun repository.
4. Verifica manuale di ogni rilievo, in cieco rispetto all'esito atteso.
5. Calcolo di precisione e richiamo per singola regola, non solo aggregati: una regola
   rumorosa va disattivata anche se la media complessiva regge.

## Criterio di promozione a stable

Da fissare prima della prima esecuzione, non dopo aver visto i risultati. La soglia
proposta, da confermare: precisione per regola non inferiore a 0,80 sui rilievi
`important`, con nessuna regola sotto 0,60.

## Criterio di abbandono

Se dopo due cicli di affinamento il modulo `riuso` non raggiunge la soglia, il
presupposto del progetto e' sbagliato e va dichiarato apertamente qui, non nascosto in
una issue.

## Risultati

Nessuna esecuzione completata.
