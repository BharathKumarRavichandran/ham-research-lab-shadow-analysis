# Shadow Analysis

## Project Installation Without Docker
1. Install Python (3.9+)
2. Install Python Package Manager (pip/pip3)
3. Set up the environment :
    * Create virtual environment files - `python3 -m venv venv`
    * Activate virtual environment - `source venv/bin/activate`
4. Install dependencies - `pip3 install -r requirements.txt`
5. Configure mongo atlas
   - Create a database - `smart_research`
   - Create a collection - `shadow_matrix` 
6. Copy contents of `.env.example` to a new file `.env` - `cp .env.example .env`
   - Fill `.env` file following [setup-env](#setup-env).
7. Start the server - `flask --app server run`
8. Access the application in port `5000`

## Project Installation With Docker
1. Install `docker`
2. Install `docker-compose`
3. Copy contents of `.env.example` to a new file `.env` - `cp .env.example .env`
   - Fill `.env` file following [setup-env](#setup-env).
4. Build the docker image - `docker-compose build`.
5. Start the container - `docker-compose up -d`.
6. Access the application in port `5000`


### Setup .env
1. Set `APP_SECRET` to random secret string
2. Set `DB_PROTOCOL` to `mongodb+srv` if you are using mongo atlas, otherwise `mongodb` (in most cases).
3. Set `DB_HOST`, `DB_USERNAME`, and `DB_PASSWORD` to your values.
4. If you are using mongo atlas, you won't have `DB_PORT`. Otherwise, fill `DB_PORT`.
