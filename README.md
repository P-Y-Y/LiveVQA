# LIVEVQA

## NEWS

### **1. `collectors`: News Collector**
This module is responsible for gathering news hot topics. It fetches articles and their associated data, serving as the initial data acquisition pipeline for the entire project.

### **2. `ranking`: Image Filter**
The `ranking` module acts as an intelligent image filter. It processes the collected news topics, evaluating the relevance of associated images to the article's core content. This step helps ensure that only high-quality, contextually relevant images are passed down the pipeline.

### **3. `qa_makers`: Level 1 Question Generator**
This component specializes in creating "**Level 1**" questions. These are foundational questions generated directly from the filtered images and their corresponding news content.

### **4. `test_set`: Level 1 Question Filter**
The `test_set` module is crucial for maintaining question quality. It evaluates the Level 1 questions generated by `qa_makers` against a strict set of criteria, filtering out any questions that are ambiguous, too simple, lack temporal context, or violate other quality standards.

### **5. `qa_makers_mh`: Level 2 Question Generator**
Building on the filtered Level 1 questions, the `qa_makers_mh` (multi-hop) module generates "**Level 2**" questions. These questions are designed to be more complex, often requiring multi-step reasoning and leveraging the answers from Level 1 questions to create challenging, multi-hop queries.

---

### How to Run

To execute the entire pipeline, simply run the `start.py` script from your project's root directory:

```bash
pip install -r requirements.txt
python start.py
```

## VIDEO

QAs pipeline for video is the same as the news pipeline.

But you should install the following Github Repositories:
- https://github.com/opendatalab/DocLayout-YOLO
- https://github.com/zcczhang/UVD

### How to run?

```bash
bash video_pipeline.sh
```

## ARXIV

### Dataset Preprocessing

- **direct_download.py**: Downloads arXiv papers by year-month and ID range with support for multi-processing and multi-threading.
- **cate.py**: Categorizes papers based on their date.
- **get_article.py**: Extracts images, paragraphs, and association information from HTML files of arXiv papers.
- **select_best_images.py**: Uses GPT-4 to analyze and rank figures from papers, selecting the most representative images.
- **streamlit_viewer.py**: Provides a web interface for annotating selected images.

### Dataset Construction

- **construct_level1.py**: Generates level 1 QA pairs focused on basic paper identification from images.
- **construct_level2.py**: Generates level 2 QA pairs that require deeper understanding of the paper content.



## Usage Instructions

### Downloading Papers

```bash
python direct_download.py --yearmonth 2405 --start-id 1 --end-id 100 --concurrent 5 --processes 4
```

Parameters:
- `--yearmonth`: Year and month in format YYMM (e.g., 2405 for May 2024)
- `--start-id`, `--end-id`: Range of paper IDs to download
- `--concurrent`: Number of concurrent downloads per process
- `--processes`: Number of processes to use

### Categorizing Papers

```bash
python cate.py
```

### Extracting Paper Content

```bash
python get_article.py --dir /path/to/html/files --output /path/to/output --workers 4
```

Parameters:
- `--dir`: Directory containing HTML files
- `--output`: Output directory for processed data
- `--workers`: Number of parallel processes
- `--force`: Force reprocessing of already processed files
- `--limit`: Limit number of files to process

### Selecting Best Images

```bash
python select_best_images.py --input_dir /path/to/json/files --output_dir /path/to/output --workers 4
```

Parameters:
- `--input_dir`: Directory containing JSON files
- `--output_dir`: Directory to output results
- `--workers`: Number of worker processes
- `--start_index`, `--end_index`: Range of folders to process
- `--force`: Force reprocessing files with existing results

### Viewing Papers and Images

```bash
streamlit run streamlit_viewer.py
```

### Generating QA Datasets

For Level 1 QA pairs (basic paper identification):
```bash
python construct_level1.py --input-path /path/to/json/files --output-file output.jsonl --workers 4
```

For Level 2 QA pairs (deeper paper understanding):
```bash
python construct_level2.py --input-file output.jsonl --output-file output_with_level2.jsonl --processes 4
```

## Environmental Variables

- `OPENAI_API_KEY`: Your OpenAI API key for GPT-4 interaction
