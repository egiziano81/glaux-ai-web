# GLAUX AI — Sito di presentazione

Sito statico a singola pagina per presentare GLAUX AI. Nessun build step: è puro HTML/CSS, pronto per GitHub Pages.

## Pubblicare su GitHub Pages

1. Crea un repository su GitHub (es. `glaux-ai-website`) e carica il contenuto di questa cartella nella **root** del repo (oppure in una cartella `docs/`).
2. Su GitHub: **Settings → Pages**.
3. In **Build and deployment**, scegli **Deploy from a branch**.
4. Seleziona il branch (es. `main`) e la cartella (`/ (root)` o `/docs`, in base a dove hai copiato i file).
5. Salva: dopo circa un minuto il sito sarà online su `https://<tuo-utente>.github.io/<nome-repo>/`.

## Prima di pubblicare

- **Collega il form "Richiedi una demo" a Formspree** (invio silenzioso, l'email di destinazione non è mai nel sorgente):
  1. Vai su [formspree.io](https://formspree.io) e crea un account gratuito (piano free: 50 invii/mese, form illimitati, nessuna carta di credito richiesta).
  2. Nella dashboard: **+ Add New → New Form**, imposta come destinatario l'email che vuoi ricevere (es. la tua).
  3. Copia l'endpoint del form, tipo `https://formspree.io/f/abcdwxyz`.
  4. In `index.html`, cerca la costante `FORMSPREE_ENDPOINT` (in fondo al file) e sostituisci `https://formspree.io/f/XXXXXXX` con il tuo endpoint.
  5. Pubblica il sito, poi fai un invio di prova dal form: la prima volta Formspree potrebbe chiederti di confermare il form dalla dashboard prima che i messaggi arrivino davvero.
- Copia il PDF della brochure (vedi cartella `brochure/`) come `brochure.pdf` in questa stessa cartella — i link "Scarica la brochure" puntano a `brochure.pdf` accanto a `index.html`.
- Se pubblichi in una sottocartella (es. repo che non è `<utente>.github.io`), verifica che i percorsi relativi (`assets/...`, `brochure.pdf`) restino corretti.

## Struttura

```
website/
├── index.html      ← pagina unica del sito
├── assets/
│   ├── logo.png
│   └── owl.png
└── brochure.pdf     ← da copiare qui prima della pubblicazione (vedi sopra)
```
