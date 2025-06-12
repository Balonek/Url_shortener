# URL Shortener (FastAPI + MongoDB)

Skracacz adresów URL napisany w **FastAPI**. Przechowuje dane w nierelacyjnej bazie danych **MongoDB**. Aplikacja posiada prosty interfejs HTML, jak i w pełni funkcjonalne REST API do zarządzania skróconymi linkami.

---

\## Spis treści

1. [Wymagania](#wymagania)
2. [Instalacja lokalna](#instalacja-lokalna)
3. [Uruchomienie lokalne](#uruchomienie-lokalne)
4. [API](#api)   



---

\## Wymagania

| Warstwa | Technologia | Wersja     |
| ------- | ----------- | ---------- |
| Runtime | Python      | **3.12**   |
| Backend | FastAPI     | **0.111**  |
| Serwer  | Uvicorn     | **0.29.0** |
| Baza    | MongoDB     | **7**      |
|         |  pymongo    | 4.7.3      |
|         |  pydantic   | 2.7.1      |
|         |  Jinja2     | 3.1.3      |

>

---

\## Instalacja lokalna

```bash
# 1. Klonuj repozytorium
git clone https://github.com/Balonek/Url_shortener.git
cd Url_shortener

# 2. Utwórz i aktywuj środowisko wirtualne
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
# source venv/bin/activate

# 3. Zainstalowanie zależności
pip install -r requirements.txt
```

---

\## Uruchomienie lokalne

```bash
uvicorn main:app --reload
```

| Adres                        | Opis                               |
| ---------------------------- | ---------------------------------- |
| `http://127.0.0.1:8000/`     | Formularz HTML do skracania linków |
| `http://127.0.0.1:8000/docs` | Swagger UI / OpenAPI               |

> Parametr `--reload` włącza automatyczny restart serwera przy zmianach w kodzie – przydatne w trakcie developmentu.

---

\## API

\### Tabela endpointów

| Metoda     | Ścieżka                     | Opis                                           |
| ---------- | --------------------------- | ---------------------------------------------- |
| **POST**   | `/api/shorten`              | Utwórz krótki link *(form‑data: ****\`\`****)* |
| **GET**    | `/api/shorten/{code}`       | Zwróć rekord w formacie JSON                   |
| **PUT**    | `/api/shorten/{code}`       | Zaktualizuj docelowy URL                       |
| **DELETE** | `/api/shorten/{code}`       | Usuń link                                      |
| **GET**    | `/api/shorten/{code}/stats` | Pobierz liczbę kliknięć                        |
| **GET**    | `/{code}`                   | Przekierowanie `301` do docelowego URL         |

\#### Przykładowe żądanie cURL

```bash
curl -X POST -F "url=https://example.com" http://127.0.0.1:8000/api/shorten
```

Odpowiedź:

```json
{
  "code": "abc123",
  "target_url": "https://example.com",
  "created_at": "2025-06-12T10:30:00Z",
  "clicks": 0
}
```

---

---



---

