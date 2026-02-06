# Projekt Zaliczeniowy DevOps

Aplikacja Flask z pipeline CI/CD do Azure App Service.

## Endpoints
- `/` – strona główna
- `/products` – przykładowe dane
- `/version` – aktualna wersja aplikacji (pochodzi z pliku `version.txt` generowanego w CI)
- `/health` – prosty health-check (użyj tej ścieżki w Azure Health Check)

## Testy i Quality Gate
- Testy: `pytest` (raport w Actions)
- Quality Gate: `flake8` (krytyczne reguły); błąd lintu zatrzymuje pipeline

## Deployment (CD)
- GitHub Actions `azure/webapps-deploy@v2`
- Sekrety: `AZURE_WEBAPP_PUBLISH_PROFILE` (Publish Profile)

## Co to jest "Wdrożenie do Azure"?
- **Opis:** Drugi job w workflow, który po udanym "Build i Test" publikuje aplikację do Azure Web App.
- **Jak działa:** Akcja `azure/webapps-deploy@v2` loguje się danymi z sekretu Publish Profile i przesyła pliki aplikacji (w folderze projektu) na serwer.
- **Gdzie jest:** Zobacz job "Wdrożenie do Azure" w [devops_projekt/.github/workflows/main.yml](devops_projekt/.github/workflows/main.yml).
- **Warunek:** Startuje tylko jeśli job "Build i Test" jest zielony.

## Region i platforma (Windows vs Linux) — prosto i chronologicznie
- **Problem:** Polityka Azure dopuszcza tylko wybrane regiony. Dodatkowo Python działa stabilnie na planie Linux, nie na Windows.
- **Jak powinno być:** Resource Group, App Service Plan i Web App w tym samym, dozwolonym regionie (np. `swedencentral`). Plan powinien być Linux (`--is-linux`) z runtime `PYTHON|3.11`.
- **Naprawa:** Przenieśliśmy zasoby do `swedencentral`, utworzyliśmy Linux App Service Plan i Web App z `PYTHON:3.11`. W CI ustawiliśmy Pythona 3.11, by pasował do środowiska.
- **Skutek:** Polityki nie blokują, runtime jest wspierany, deploy kończy się sukcesem.
- **Komendy pomocnicze:**
	```powershell
	az policy assignment list --query "[?parameters.listOfAllowedLocations != null]"   # (lista dozwolonych regionów)
	az webapp show --name app-devops-zaliczenie-7780 --resource-group rg-devops-zaliczenie --query location -o tsv  # (aktualny region aplikacji)
	```

## Quality Gate (lint + testy)
- **Cel:** Zatrzymać wdrożenie, jeśli kod ma krytyczne błędy lub testy nie przechodzą.
- **Jak działa:** W jobie "Build i Test" najpierw `flake8` (łapie najgroźniejsze błędy), potem `pytest` (sprawdza endpointy). Porażka któregokolwiek blokuje pipeline.
- **Urywki z workflow:**
	- `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics` ("szuka baboli": błędna składnia, trefne importy itp.)
	- `pytest --junitxml=test-results.xml` (uruchamia testy i zapisuje raport)

### Notatka: Quality Gate — jak działa i jak jest zainicjowane tutaj
- **Gdzie:** Job "Build i Test" w pliku [devops_projekt/.github/workflows/main.yml](devops_projekt/.github/workflows/main.yml).
- **Co uruchamia:** `flake8` (reguły: E9, F63, F7, F82) oraz `pytest` dla testów z [devops_projekt/test_app.py](devops_projekt/test_app.py).
- **Kiedy:** Automatycznie na `push` i `pull_request` do gałęzi `main` (zdefiniowane w sekcji `on:` workflow).
- **Warunek deployu:** Job "Wdrożenie do Azure" startuje tylko, gdy Quality Gate (Build i Test) zakończy się sukcesem.
- **Sprawdzenie lokalne:**
	```powershell
	flake8 devops_projekt        # lint: krytyczne błędy
	pytest -q devops_projekt/test_app.py   # testy endpointów
	```
- **Po co:** Chroni przed publikacją wadliwego kodu (prosto: "nie wypychaj bubla").

## Wersjonowanie (9)
- **Cel:** Prosta, widoczna wersja aplikacji.
- **Jak działa:** Actions zapisuje numer przebiegu (`github.run_number`) do `version.txt`; endpoint `/version` zwraca tę wartość.
- **Gdzie:** Zapis w [devops_projekt/.github/workflows/main.yml](devops_projekt/.github/workflows/main.yml), odczyt w [devops_projekt/app.py](devops_projekt/app.py).


## Opcjonalne zadania
- 11. Sekrety – użyty GitHub Secret (bez haseł w repo)
- 13. Quality Gate – lint + testy w CI
- 9. Automatyczne wersjonowanie – `version.txt` tworzony w kroku CI z numeru `github.run_number` i eksponowany pod `/version`
- 8. Monitoring i logi – endpoint `/health`; włącz Health Check w Portalu (Configuration → General settings → Health Check path `/health`)

## Uruchomienie lokalne
```bash
pip install -r requirements.txt
python devops_projekt/app.py
```

## Krótki przewodnik sprawdzenia (lokalnie i w Actions)
- **Lokalnie:**
	```powershell
	pip install -r devops_projekt/requirements.txt
	flake8 devops_projekt   # (sprawdza krytyczne błędy w kodzie)
	pytest -q devops_projekt/test_app.py   # (uruchamia testy endpointów)
	```
- **W Actions:** Otwórz ostatni przebieg na `main` — najpierw "Build i Test", potem "Wdrożenie do Azure". Zielony build ⇒ startuje deploy.
