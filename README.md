# DKJOBS — Søg i det danske jobmarked

AI-drevet jobsøgning over det danske jobmarked. Bygget til at hostes gratis på GitHub Pages.

---

## Hurtig opsætning (GitHub Pages)

### 1. Opret et GitHub-repository

Gå til [github.com/new](https://github.com/new) og opret et **offentligt** repository.  
Navngiv det f.eks. `dkjobs`.

### 2. Upload disse filer

Upload følgende filer og mapper til dit repository:

```
index.html
data/
  manifest.json
  februar_2026.json   ← din konverterede datafil (se nedenfor)
convert_to_json.py    ← bruges lokalt, ikke nødvendig på GitHub
README.md
```

### 3. Aktivér GitHub Pages

1. Gå til dit repository → **Settings** → **Pages**
2. Under *Source*: vælg **Deploy from a branch**
3. Branch: `main` / `master` — Folder: `/ (root)`
4. Klik **Save**

Din side er live på:  
`https://DIT-BRUGERNAVN.github.io/dkjobs/`

Det tager typisk 1–2 minutter før siden er tilgængelig.

---

## Konverter din XLSX/CSV til JSON

Kør scriptet lokalt på din maskine:

```bash
pip install pandas openpyxl
python convert_to_json.py februar_2026.xlsx
```

Scriptet genererer `februar_2026.json` klar til upload.

---

## Opdatering af data (månedlig)

1. Kør `convert_to_json.py` på den nye fil
2. Upload den nye JSON-fil til `data/` i dit repository
3. Opdatér `data/manifest.json` — tilføj den nye fil og fjern den ældste:

```json
{
  "files": [
    {
      "name": "Februar 2026",
      "filename": "februar_2026.json",
      "date": "1. februar 2026"
    },
    {
      "name": "Marts 2026",
      "filename": "marts_2026.json",
      "date": "1. marts 2026"
    }
  ]
}
```

GitHub Pages deployer automatisk inden for ~1 minut efter du pusher.

---

## Dataformat

Følgende kolonner bruges i XLSX/CSV/JSON:

| Kolonne | Bruges til |
|---|---|
| `job_title` | Jobtitel (vises i resultater) |
| `company_name` | Virksomhed (vises i resultater) |
| `job_url` | Link til opslaget (klikbart i app og PDF) |
| `job_category` | Kategori-filter |
| `job_type` | Jobtype |
| `employment_form` | Ansættelsesform-filter |
| `town` | By (vises som lokation-tag) |
| `region` | Region-filter |
| `application_date` | Bruges til at markere udløbne opslag |
| `created_date` | Oprettelsesdato |
| `gpt_context` / `description` | Bruges af AI til rangering |

---

## Funktioner

- 🔍 **Semantisk søgning** — beskriv hvad du leder efter med fri tekst
- 🤖 **AI-rangering** — Claude rangerer de 15 bedste matches (kræver Anthropic API-nøgle)
- ⭐ **Genvejsliste** — markér interessante opslag på tværs af søgninger  
- 📄 **PDF-download** — eksportér din genvejsliste som en klikbar PDF-fil
- 🔎 **Filtre** — region, kategori, ansættelsesform
- ⚠️ **Udløbsdetektering** — opslag med passeret ansøgningsfrist markeres
- ⚙️ **Indstillinger** — tilpas tekster, eksempel-søgninger og AI-prompt

---

## API-nøgle

Søgning uden API-nøgle fungerer med nøgleordsmatch.  
For AI-rangering: hent en nøgle på [console.anthropic.com](https://console.anthropic.com) og indtast den via 🔑-knappen i appen. Nøglen gemmes kun lokalt i brugerens browser.

---

## Datasikkerhed

Datafilerne i `data/` er offentligt tilgængelige via GitHub Pages URL'en, men da data er offentligt tilgængelige jobopslag, er dette acceptabelt for et MVP-showcase. For intern brug med fortrolige data, overvej [Cloudflare Access](https://www.cloudflare.com/zero-trust/products/access/).
