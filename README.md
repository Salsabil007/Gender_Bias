# Equity in Science Journalism: Gender Disparities in News Coverage — Code & Reproduction

This repository contains code and notebooks for a large-scale study of gender disparities in U.S. news media coverage of scientific research (2018–2022). The workflow links Scopus metadata, Altmetric news mentions, Crossref DOIs, Science-Metrix journal/field taxonomies, outlet typologies, and outlet ideology scores; it then constructs matched control groups (CEM), analyzes media selection and counts, and runs sentence-level sentiment analysis on scraped news text.

> **Paper:** Arabi et al., 2025 — *Equity in Science Journalism: Investigating Gender Disparities in News Media Coverage of Scientific Research* (see `paper.pdf` included with this project).

---

## TL;DR

- **Goal:** Quantify how corresponding-author gender relates to (i) probability of being cited by news, (ii) how often papers are cited, (iii) which outlet types cite them, (iv) outlet ideology, and (v) sentiment of associated news text.  
- **Data:** Scopus (paper metadata + gender inferences), Altmetric (news mentions + URLs), Crossref (DOIs), Science-Metrix (fields), publicly curated outlet lists and ideology scores.  
- **Methods:** Coarsened Exact Matching (CEM) for media-cited vs. matched control; logistic/Poisson regressions with covariates; RoBERTa-based sentence-level sentiment; stratification by outlet type/ideology.

---

## Repository structure

Gender_Bias/

├── Analysis_files_databricks/ # (archived) intermediate analysis notebooks / exports

├── Dunning_Log_Likelihood_test/ # keyness tests / word-salience experiments

├── Vader_sentiment/ # rule-based sentiment baselines / utilities

├── databricks_files_May18/ # additional exploratory notebooks/data (legacy)

├── preprocess/ # cleaning, field mapping, filters

├── CEM_implement.ipynb # coarsened exact matching setup & diagnostics

├── Categorical_Jul27.ipynb # categorical analysis / plots

├── Journal_select.ipynb # journal filtering to top news-mentioned per field

├── collecting_news_outlet.py # outlet taxonomy + ideology integration

├── cross_ref_doi_json.py # Crossref DOI harvesting by ISSN

├── data_collection_cycle2.py # Altmetric + Scopus collection orchestration

├── data_dump2.py # bulk persistence / checkpointing

├── news_citation_analysis.ipynb # regression models (OR/RR), figures

├── news_outlet_name_analysis.ipynb # outlet-type and ideology analyses

├── sentence_extraction.ipynb # URL scraping → sentence segmentation

├── testing_altmetric_api.ipynb # probing Altmetric endpoints

├── web_scrapping.ipynb # news page parsing (HTML cleanup, quote masking)

└── run_chtc.txt # sample HTCondor batch spec (UW CHTC)




## Environment

- **Python:** 3.9–3.11  
- **Core packages:**  
  `pandas`, `numpy`, `scikit-learn`, `statsmodels`, `requests`, `tqdm`,  
  `beautifulsoup4`, `lxml`, `newspaper3k` (or `trafilatura`), `regex`,  
  `matplotlib`, `seaborn`, `torch`, `transformers`, `pyreadstat` (optional).


# Create & activate env
conda create -n genderbias python=3.10 -y
conda activate genderbias

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt

# If requirements.txt is missing, export a minimal one after running the notebooks:
pip freeze | grep -E '^(pandas|numpy|scikit-learn|statsmodels|requests|tqdm|beautifulsoup4|lxml|newspaper3k|trafilatura|regex|matplotlib|seaborn|torch|transformers)=' > requirements.txt


## External data & access

You will need access/credentials for:

*1 Scopus: per-DOI metadata (author list, corresponding-author name, affiliation country, SJR, OA flags, etc.).

*2 Altmetric: per-DOI news mentions and article URLs.

*3 Crossref: DOI harvesting by ISSN (open).

*4 Science-Metrix: journal/field taxonomy to define domains/fields.

*5 U.S. news outlet taxonomy & ideology: outlet type (local/national/international/specialty) and ideology scores used for stratification.

# Configuration

Create a config.yaml (or .env) to centralize paths and credentials:

paths:
  journals_csv: data/journals.csv
  dois_jsonl: data/dois.jsonl
  altmetric: data/altmetric_mentions.parquet
  scopus: data/scopus_metadata.parquet
  outlet_meta: data/outlet_meta.parquet
  sentences: data/news_sentences.parquet

altmetric:
  api_key: "YOUR_ALTMETRIC_KEY"

scrape:
  user_agent: "your-email@institution.edu"
  timeout_s: 20
  max_retries: 3

# Reproduce the pipeline

Scope: U.S.-affiliated, English-language papers published 2018–2022 in journals selected by high news mentions within each field (top quantile).

### Prepare data/journals.csv with at least: issn, journal_title, field.

python cross_ref_doi_json.py \
  --issn_csv data/journals.csv \
  --out data/dois.jsonl


### Collect Altmetric news mentions

Provide Altmetric credentials via config.yaml or environment variables.

python data_collection_cycle2.py \
  --dois data/dois.jsonl \
  --out data/altmetric_mentions.parquet

### Join Scopus metadata

Export per-DOI Scopus metadata from your institutional access and save as:

data/scopus_metadata.parquet


Key merge columns: normalize doi (lower-case, trimmed). Include: corresponding-author gender (with confidence), affiliation country, OA, SJR, publication year, author count, field/subfield.

### Filter the analytic cohort

In notebooks under preprocess/ and Journal_select.ipynb:

Keep U.S. affiliation (corresponding author) and English-language items.

Apply gender confidence thresholds; drop unresolved cases.

For multi-corresponding-author papers, select the first listed.

Restrict to 2018–2022.

Persist the filtered cohort to data/analytic_cohort.parquet.

### Outlet classification & ideology

Map news URLs → outlet domains; attach outlet type and ideology:

python collecting_news_outlet.py \
  --in data/altmetric_mentions.parquet \
  --out data/outlet_meta.parquet \
  --outlet_map assets/outlet_typology.csv \
  --ideology_map assets/outlet_ideology.csv


### Scrape article text & segment sentences

Use web_scrapping.ipynb to fetch article HTML safely, then sentence_extraction.ipynb to:

Strip boilerplate and ads

Mask quoted speech to focus on narration

Deduplicate and segment into sentences (retain ~5–100 sentences/article)

### Construct matched controls (CEM)

Open CEM_implement.ipynb and define coarsening over:

subfield, venue, OA status

binned years (e.g., 2018–2020, 2021–2022)

author-count bands (1, 2–4, 5–7, 8–10, 11–15, 16–20, >20)

Export CEM weights to data/cem_weights.parquet.

### Selection & intensity models

In news_citation_analysis.ipynb:

Selection (media-cited vs not): weighted logistic regressions by field/domain with covariates (year, author count, subfield, SJR, OA).

Intensity (counts for cited papers): Poisson regressions; same covariates.

In news_outlet_name_analysis.ipynb:

Stratify by outlet type and ideology; compute women-over-men odds ratios.

### Sentiment analysis

In sentence_extraction.ipynb:

Apply a RoBERTa sentiment model (e.g., tweet-trained variant) for sentence-level pos/neu/neg scores.

Run regressions at the sentence level on gender, controlling for year, journal quantile, and field.

Optionally compare against VADER in Vader_sentiment/.
