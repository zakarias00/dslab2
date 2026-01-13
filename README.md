# Data Science Laboratory 2

This repository hosts materials and code for the Data Science Laboratory 2 subject at the ELTE Data Science Department. It contains exploratory data analysis (EDA) assets, a dataset of courses, and an embedding generation workflow to support downstream tasks like ontology generation and knowledge graph creation.

## Repository structure

```
dslab2/
├─ README.md
├─ requirements.txt
├─ courses_dataset.csv
├─ eda/                 # EDA notebooks, scripts, and outputs (add your analyses here)
└─ embeddings/          # Embedding outputs: .npy vectors and metadata .csv (created by scripts)
```

Direct links:
- Data: [courses_dataset.csv](https://github.com/zakarias00/dslab2/blob/main/courses_dataset.csv)
- EDA directory: [eda/](https://github.com/zakarias00/dslab2/tree/main/eda)
- Embeddings directory: [embeddings/](https://github.com/zakarias00/dslab2/tree/main/embeddings)
- Requirements: [requirements.txt](https://github.com/zakarias00/dslab2/blob/main/requirements.txt)

## Getting started

1) Clone the repository
```bash
git clone https://github.com/zakarias00/dslab2.git
cd dslab2
```

2) Create a virtual environment (recommended)
```bash
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3) Install dependencies
```bash
pip install -r requirements.txt
```

Alternatively, core packages used by the embedding workflow include:
- sentence-transformers
- pandas
- numpy
- tqdm

You can install them directly if you prefer:
```bash
pip install sentence-transformers pandas numpy tqdm
```

## Data

- [courses_dataset.csv](https://github.com/zakarias00/dslab2/blob/main/courses_dataset.csv) is a CSV containing course-related fields. Use it for EDA and embedding generation examples.
- Store additional datasets in the repository root or create a dedicated `data/` directory if your workflow grows.

## EDA

Use the [eda/](https://github.com/zakarias00/dslab2/tree/main/eda) folder for:
- Inspecting dataset quality and distributions
- Text cleaning and feature engineering
- Visualizations (e.g., word clouds, topic histograms)
- Preparing combined text fields (e.g., title + description) prior to embedding


## Embeddings

This repository uses a SentenceTransformers-based workflow to create vector embeddings for text. The following script description outlines the capabilities and usage pattern for generating embeddings from CSV files or pandas DataFrames using `SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')` (384-dimensional vectors).

Script summary:
- Modes:
  - row: concatenate selected text columns per row into one string and embed per row (default)
  - cell: embed each non-empty cell of selected text columns
- Auto-detect text columns if none are specified (object/string/category)
- Batching, optional normalization, and optional max char trimming per text
- Saves:
  - {output_prefix}_embeddings.npy (NumPy array of shape [N, 384])
  - {output_prefix}_metadata.csv (mapping info and the embedded text)

Requirements:
```bash
pip install sentence-transformers pandas numpy tqdm
```

Usage examples:
```bash
# Embed one vector per row by concatenating selected columns
python create_embeddings.py \
  --input ./courses_dataset.csv \
  --output-prefix embeddings/eda_embeddings \
  --mode row \
  --batch-size 64 \
  --normalize

# Embed each non-empty cell of specific columns
python create_embeddings.py \
  --input ./courses_dataset.csv \
  --output-prefix embeddings/cell_embeddings \
  --mode cell \
  --columns "course_title,combined_description"
```

Outputs:
- `embeddings/eda_embeddings_embeddings.npy` — Float32 NumPy array shaped `[N, 384]`
- `embeddings/eda_embeddings_metadata.csv` — CSV mapping rows/cells to texts and indices

## Troubleshooting

- Memory usage: Reduce `--batch-size` if you face memory constraints.
- Long texts: Consider trimming inputs to a reasonable maximum to improve throughput.
- Column selection: Ensure the `--columns` argument matches CSV headers; otherwise rely on auto-detection.
- Unicode/CSV parsing: Load with an explicit encoding if necessary, e.g., `encoding="utf-8"`.
