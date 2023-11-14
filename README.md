# Gene Pathways and Compounds Analysis

This script utilizes the KEGG API to analyze the association between specific genes and pathways related to the compound of interest, choline. The selected genes were manually curated using Ensemble and IGV, while the compounds were chosen based on their relevance to the study.

## Usage

1. Clone this repository to your local machine:

    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

    Replace `<repository-url>` with the URL of your forked repository.

2. Run the script:

    ```bash
    python script_name.py
    ```

    Replace `script_name.py` with the actual name of your Python script.

3. Check the output:

    The script generates a CSV file, `choline_gene_pathways_and_compounds.csv`, containing information about the selected genes, pathways, and the presence or absence of compounds in those pathways.

## Notes

- **Genes of Interest:**
  - YDL077C
  - YDR207C
  - YGR202C
  - YHL020C
  - YLL010C
  - YOR058C
  - YDL075W
  - YDR039C
  - YDR208W
  - YEL070W
  - YGR200C
  - YHL017W
  - YLL008W
  - YOR041C
  - YOR054C
  - YOR043W
  - YCR067C
  - YDR150W
  - YDR420W
  - YPL188W

## Output

The generated CSV file contains columns for Gene ID, Pathway ID, and binary indicators for the presence or absence of each compound of interest in the corresponding pathway.

## Disclaimer

This script is tailored for a specific study, and the selected genes and compounds are based on manual curation. Adjustments may be needed for different research contexts.
