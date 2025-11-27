# Pharma Classifier

Solution complète permettant de classifier automatiquement un catalogue de produits en distinguant les médicaments de la parapharmacie. Elle repose sur un pipeline Python (FastAPI) et une interface React moderne pour piloter les traitements, visualiser les résultats et suivre l'historique des décisions.

## Architecture en un coup d'œil
- **Backend FastAPI (`backend/`)** : expose les endpoints d'upload (`/upload`), d'exécution du pipeline (`/run`), de consultation des résultats (`/results`, `/download`) et de l'historique (`/history`).
- **Pipeline métier (`backend/src/`)** : enchaîne plusieurs étapes (matching historique, règles sur libellés, vérification via l'API BDPM REST, classification OpenAI) puis exporte les résultats V2 et met à jour l'historique global.
- **Frontend React + Vite (`frontend/`)** : interface permettant de déposer un CSV, lancer le pipeline, afficher les métriques, explorer les résultats tabulaires et l'historique consolidé.
- **Répertoire `data/`** (monté en volume) :
  - `data/uploaded/` : fichiers utilisateurs importés via l'UI ou l'API.
  - `data/output/v2/` : export `resultat_v2.csv` mis à jour après chaque run.
  - `data/input/base_initiale/` : sources utilisées par le CLI standalone (`python src/main.py`).
  - `data/input/historiques/historique_global.csv` : référentiel pour le matching historique.
  - `data/cache/` : fichiers temporaires (créés automatiquement).

## Pré-requis
- Docker & Docker Compose (recommandé pour l'utilisation standard).
- Option développement local :
  - Python 3.11 + `pip` pour le backend.
  - Node.js 18+ et `npm`/`yarn` pour le frontend.
- Variables d'environnement (à placer dans un fichier `.env` à la racine ou directement dans l'environnement) :
  - `OPENAI_API_KEY` : clé utilisée par la classification IA (**obligatoire** pour l'étape IA).
  - `API_MEDICAMENTS_BASE` *(optionnel)* : URL de l'API BDPM REST (valeur par défaut `https://fr.gouv.medicaments.rest/api/medicaments`).
  - `DATA_DIR` *(optionnel)* : chemin racine des données (par défaut `data`).

Un exemple de configuration est disponible dans `.env.example`. Copiez-le puis renseignez vos valeurs :

```bash
cp .env.example .env
```

## Lancer la solution avec Docker Compose
```bash
# depuis la racine du dépôt
docker compose up --build
```
Cela démarre :
1. `api` (FastAPI) exposée sur [http://localhost:18000](http://localhost:18000).
2. `ui` (Vite/React) exposée sur [http://localhost:18100](http://localhost:18100) et pointant sur l'API via `VITE_API_URL=http://localhost:18000`.

Pour Docker Compose, placez vos variables (dont `OPENAI_API_KEY`) dans un fichier `.env` à la racine du dépôt : il est automatiquement chargé dans le conteneur `api`.

Pendant l'exécution :
- Les fichiers uploadés et résultats restent persistés dans le dossier hôte `data/` (merci au volume partagé).
- Les ports peuvent être ajustés dans `docker-compose.yml` (pensez à synchroniser `VITE_API_URL`).
- Pour arrêter : `Ctrl+C`, puis `docker compose down` si besoin.

## Parcours utilisateur via l'interface
1. Accéder au frontend ([http://localhost:18100](http://localhost:18100)).
2. **Upload CSV** : sélectionner un fichier (UTF-8, séparateur `,`). Le backend le stocke et retourne un `path` local.
3. **Lancer le pipeline** : cliquer sur « Lancer le pipeline ». L'UI appelle `/run` avec le `file_path` précédent.
4. **Suivre les métriques** : après traitement, un encart affiche le nom du fichier résultant et le nombre de lignes classifiées.
5. **Consulter les résultats** :
   - Tableau directement dans la page (endpoint `/results`).
   - Téléchargement du CSV (`/download`).
6. **Historique** : le composant History Viewer lit `/history` pour visualiser les décisions cumulées.

## Structure attendue des fichiers CSV (upload & historique)
Les colonnes suivantes doivent être présentes dans les fichiers importés (upload utilisateur ou historique) afin que le backend puisse normaliser les données :

| Colonne obligatoire | Description | Exemples d'alias acceptés |
|---------------------|-------------|---------------------------|
| `CIP` | Code produit (CIP 13) | `CIP13`, `Code_CIP`, `cip_13` |
| `Libelle` | Libellé complet du produit | `Libellé`, `Libelle_produit`, `Désignation` |
| `Marque` | Marque ou laboratoire |  |
| `Univers` | Univers métier |  |
| `Famille` | Famille associée |  |
| `Tablette` | Catégorie tablette | `Tablettes` |
| `Tablette_consolidee` | Catégorie tablette consolidée | `Tablette consolidée` |

Les noms ci-dessus correspondent aux clés utilisées par le pipeline (`EXPECTED_COLUMNS`). Lors du chargement, le backend tente de renommer automatiquement les colonnes grâce aux alias les plus courants (par exemple `cip`, `libellé`, `tablette consolidée`, etc.). Si une colonne obligatoire manque, le backend lèvera une erreur « Colonnes manquantes ». Assurez-vous donc que chaque fichier comporte bien ces informations, même si certaines cellules sont vides.

## Utilisation avancée / développement local
### Backend FastAPI hors Docker
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Créez un fichier .env si nécessaire (variables ci-dessus)
uvicorn main_api:app --host 0.0.0.0 --port 8000 --reload
```
L'API sera accessible sur `http://localhost:8000`.

### Frontend React hors Docker
```bash
cd frontend
npm install
VITE_API_URL=http://localhost:8000 npm run dev
```
L'interface est servie sur `http://localhost:5173` (modifiable via Vite). Ajustez `VITE_API_URL` pour pointer vers l'API FastAPI démarrée précédemment.

### Lancer le pipeline en mode CLI (batch)
Indépendamment de l'API, il est possible de traiter un lot de fichiers déjà présents dans `data/input/base_initiale/` :
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```
Le script charge tous les CSV admissibles, applique les étapes de nettoyage/normalisation, exécute le pipeline complet puis produit `data/output/v2/pharmacie_classifiee_v2.csv` et met à jour l'historique global.

## Endpoints principaux de l'API
| Méthode | Route      | Description                                     |
|---------|------------|-------------------------------------------------|
| GET     | `/`        | Retourne un message de bienvenue + liens utiles.|
| GET     | `/health`  | Vérifie que le service est opérationnel.        |
| POST    | `/upload`  | Reçoit un fichier CSV (champ `file`).           |
| POST    | `/run`     | Lance le pipeline sur le fichier uploadé.       |
| GET     | `/results` | Retourne les résultats structurés (JSON).       |
| GET     | `/download`| Télécharge le dernier CSV produit.              |
| GET     | `/history` | Liste les historiques consolidés.               |

## Tests rapides
- Vérifier que l'API répond : `curl http://localhost:18000/health` → `{ "status": "ok" }`.
- Importer un fichier de test : `curl -F "file=@mon_fichier.csv" http://localhost:18000/upload`.
- Déclencher un run (avec le `path` retourné) :
  ```bash
  curl -X POST http://localhost:18000/run \
    -H 'Content-Type: application/json' \
    -d '{"file_path": "data/uploaded/mon_fichier.csv"}'
  ```
- Télécharger le résultat : `curl -L -o resultat_v2.csv http://localhost:18000/download`.

## Dépannage & bonnes pratiques
- Vérifiez que `OPENAI_API_KEY` est défini avant de lancer le backend (sinon la classification IA échouera).
- Les logs du pipeline détaillent chaque étape (matching historique, détection règle, appel API, IA) directement dans la sortie du conteneur `api`.
- En cas de changement de structure CSV, adaptez les étapes d'ingestion/validation dans `backend/src/ingestion/`.
- Pour purger les données, supprimez le dossier `data/` (ou un sous-dossier spécifique) avant de relancer `docker compose up`.

Bon run !
