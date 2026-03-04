# Kebab Manager Enterprise 🥙

Una web application modulare e in tempo reale per la gestione degli ordini in un ristorante o locale fast-food. Progettata con un'architettura client-server per reti locali (LAN), offre due interfacce Single Page Application (SPA) separate per clienti e titolari.

## 🚀 Caratteristiche Principali

* **Dashboard Cliente:** Interfaccia multi-step per la selezione dei menù, gestione dinamica delle varianti e invio degli ordini (Asporto / Consumazione al tavolo).
* **Dashboard Titolare (Real-Time):** Ricezione istantanea dei nuovi ordini tramite connessione bidirezionale **WebSocket**, eliminando la necessità di polling o aggiornamenti manuali della pagina.
* **Architettura Stateless & State Hydration:** Recupero dello storico ordini all'avvio dell'interfaccia admin e successiva sottoscrizione agli eventi in tempo reale.
* **Esecuzione Zero-Config:** Progettata per girare in locale tramite SQLite, senza necessità di configurare server database esterni come PostgreSQL o MySQL.

## 🛠️ Stack Tecnologico

L'applicazione si basa su un moderno stack Python per il backend e tecnologie web standard per il frontend, garantendo leggerezza e manutenibilità.

* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) - Framework web asincrono ad altissime prestazioni per la creazione di API REST e gestione WebSockets.
* **Server ASGI:** [Uvicorn](https://www.uvicorn.org/) - Server per l'esecuzione del codice asincrono Python in produzione.
* **Database & ORM:** [SQLite](https://www.sqlite.org/) gestito tramite [SQLAlchemy](https://www.sqlalchemy.org/) per mappare gli oggetti Python in tabelle relazionali.
* **Frontend:** HTML5, Vanilla JavaScript (Fetch API) e [Tailwind CSS](https://tailwindcss.com/) (tramite CDN) per una prototipazione rapida e responsive.
* **Templating:** Jinja2 per il serving delle interfacce.

## ⚙️ Prerequisiti

* [Python 3.8+](https://www.python.org/downloads/) installato e aggiunto al PATH di sistema.
* Una rete locale (LAN) funzionante per consentire la comunicazione tra i dispositivi (es. PC del titolare e Tablet del cliente).

## 🚀 Installazione e Avvio Rapido (Windows)

Il progetto include uno script Batch per automatizzare completamente la creazione dell'infrastruttura locale.

1. Clona la repository:
   ```bash
   git clone [https://github.com/tuo-username/nome-repository.git](https://github.com/tuo-username/nome-repository.git)
   cd nome-repository