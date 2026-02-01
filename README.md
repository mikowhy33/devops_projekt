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
