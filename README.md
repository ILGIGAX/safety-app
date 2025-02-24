# safety
Safety è un’applicazione che fornisce funzionalità di sicurezza urbana come mappe di pericolosità, pulsanti di emergenza e percorsi sicuri

Struttura del progetto

*Frontend*

Cartelle principali:
public/: Contiene i file statici principali, come l’HTML della pagina principale (index.html) e il foglio di stile CSS (style.css), che vengono serviti direttamente al browser.
src/: Può ospitare i file di codice sorgente JavaScript modularizzati, componenti aggiuntivi, o altre risorse che verranno elaborate e servite al browser.
File principali:
index.html:
È la pagina principale del progetto. Contiene il markup base per l’interfaccia utente, incluse le sezioni di registrazione, login e recupero password. Definisce la struttura visibile al cliente.
style.css:
Gestisce l’aspetto visivo della pagina. Qui si trovano le regole di stile che determinano l’aspetto delle sezioni, dei form e di altri elementi HTML.
script.js:
Contiene la logica di interazione dell’utente. Si occupa di gestire eventi come la selezione delle schede di registrazione e login, la visualizzazione delle password, e l’invio di dati ai servizi del backend.


#Backend

File principali:

main.py:
È il file principale dell’applicazione FastAPI. Contiene tutte le route e i modelli per le varie operazioni, come la registrazione degli utenti, il login, l’attivazione degli allarmi di emergenza, e la restituzione di percorsi sicuri.
requirements.txt:
Elenca le dipendenze Python necessarie per eseguire il backend. Contiene, ad esempio, fastapi, uvicorn, e asyncpg, che sono essenziali per il funzionamento dell’API e la connessione al database.
Dockerfile:
Definisce come creare un’immagine Docker del backend. Imposta l’ambiente Python, installa le dipendenze, copia i file necessari e specifica il comando per avviare il server con uvicorn.
Architettura:
Il backend è basato su FastAPI, un framework Python ad alte prestazioni per la creazione di API. Utilizza la convalida degli input tramite Pydantic e implementa endpoint RESTful per registrazione, login, invio di alert e recupero dati. La comunicazione con il database avviene attraverso asyncpg, che consente query asincrone per ottenere migliori performance.

#Database

Tabelle principali:
utenti:
Questa tabella memorizza gli utenti registrati al sistema. I campi principali includono:
id: Identificativo univoco dell’utente.
email: L’indirizzo email usato per accedere.
password: La password (idealmente hashata per sicurezza).
nome e cognome: Informazioni personali di base.
data_nascita: La data di nascita dell’utente.
genere: Indica il genere dell’utente.
motivo_iscrizione: Campo opzionale che descrive la ragione dell’iscrizione.
Questa struttura permette di gestire le informazioni degli utenti in modo semplice, supportando sia le operazioni di login che di registrazione.
Flusso di lavoro

Frontend -> Backend:
L’utente interagisce con l’interfaccia nel browser. Ad esempio, inserisce i dati di registrazione in un form. Questi dati vengono inviati al backend tramite una richiesta HTTP, utilizzando il metodo POST.

Backend -> Database:
Quando il backend riceve la richiesta, valida i dati ricevuti e, in caso positivo, interagisce con il database. Per esempio, inserisce i dati di un nuovo utente nella tabella utenti.

Database -> Backend:
Il database restituisce un risultato (ad esempio, un nuovo record creato o un messaggio di errore se l’email è già registrata).

Backend -> Frontend:
Il backend prende il risultato del database e lo trasforma in una risposta HTTP. Questa risposta viene inviata al frontend, che aggiorna l’interfaccia utente di conseguenza (ad esempio, mostrando un messaggio di successo o un errore).
