# GLAUX AI — Sito di presentazione

Sito statico a singola pagina per presentare GLAUX AI. Nessun build step: è puro HTML/CSS, pronto per GitHub Pages.

## Pubblicare su GitHub Pages

1. Crea un repository su GitHub (es. `glaux-ai-website`) e carica il contenuto di questa cartella nella **root** del repo (oppure in una cartella `docs/`).
2. Su GitHub: **Settings → Pages**.
3. In **Build and deployment**, scegli **Deploy from a branch**.
4. Seleziona il branch (es. `main`) e la cartella (`/ (root)` o `/docs`, in base a dove hai copiato i file).
5. Salva: dopo circa un minuto il sito sarà online su `https://<tuo-utente>.github.io/<nome-repo>/`.

## Prima di pubblicare

- Il form "Richiedi una demo" invia a un indirizzo mascherato nel sorgente di `index.html` (cerca `_EU`/`_ED` in fondo al file) — apre il client di posta del visitatore, non è un invio silenzioso lato server. Se in futuro vuoi l'invio automatico senza aprire il client di posta, serve un servizio come Formspree (richiede un account gratuito).
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
