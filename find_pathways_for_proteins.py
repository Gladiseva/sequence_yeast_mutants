import requests
import csv

def search_compound_id(compound_name):
    search_url = "http://rest.kegg.jp/find/compound/{}".format(compound_name)

    response = requests.get(search_url)

    if response.status_code == 200:
        lines = response.text.strip().split('\n')
        if lines:
            # Extract the compound ID from the first line
            compound_id = lines[0].split()[0]
            return compound_id
    else:
        print("Error: Unable to fetch compound information for {}. HTTP Status Code: {}".format(compound_name, response.status_code))
        return None

def get_all_related_compound_ids(compound_name):
    search_url = "http://rest.kegg.jp/find/compound/{}".format(compound_name)

    response = requests.get(search_url)

    if response.status_code == 200:
            # Extract the compound IDs
            compound_ids = [line.split('\t')[0] for line in response.text.split('\n') if line.strip()]
            return compound_ids
    else:
        print("Error: Unable to fetch compound information for {}. HTTP Status Code: {}".format(compound_name, response.status_code))
        return None

def is_compound_in_pathway(compound_name, pathway_id):
    compound_id = search_compound_id(compound_name)
    # KEGG API endpoint for retrieving information about a specific pathway
    pathway_url = "http://rest.kegg.jp/get/{}".format(pathway_id)

    try:
        # Make a request to the KEGG API
        response = requests.get(pathway_url)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Check if the gene ID is present in the pathway information
            return compound_id.replace("cpd:", "") in response.text
        else:
            print("Error: Unable to fetch pathway information. HTTP Status Code: {}".format(response.status_code))
    except Exception as e:
        print("Error: {}".format(e))

    return False

def is_compound_id_in_pathway(compound_id, pathway_id):
    # KEGG API endpoint for retrieving information about a specific pathway
    pathway_url = "http://rest.kegg.jp/get/{}".format(pathway_id)

    try:
        # Make a request to the KEGG API
        response = requests.get(pathway_url)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Check if the gene ID is present in the pathway information
            return compound_id.replace("cpd:", "") in response.text
        else:
            print("Error: Unable to fetch pathway information. HTTP Status Code: {}".format(response.status_code))
    except Exception as e:
        print("Error: {}".format(e))

    return False

def get_pathways_for_gene(gene_id):
    # KEGG API endpoint for retrieving pathway information for a specific gene
    pathway_url = "https://rest.kegg.jp/link/pathway/sce:{}".format(gene_id)

    try:
        response = requests.get(pathway_url)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Extract pathway IDs from the response
            pathway_ids = [line.split('\t')[1] for line in response.text.split('\n') if line.strip()]
            return pathway_ids
        else:
            print("Error: Unable to fetch pathway information. HTTP Status Code: {}".format(response.status_code))
    except Exception as e:
        print("Error: {}".format(e))

    return []

#compounds_of_interest = ['inositol', 'choline', 'phosphatidic acid', 'diglyceride', 'triglyceride', 'cytidine diphosphate diacilglycerol',
#                         'CDP-diacylglycerol', 'phosphatidylserine', 'phosphatidylethanolamine', 'lipid']
compounds_of_interest = ['inositol']
gene_ids_to_check = ['YDL077C','YDR207C','YGR202C','YHL020C','YLL010C','YOR058C','YDL075W','YDR039C','YDR208W',
                        'YEL070W','YGR200C','YHL017W','YLL008W','YOR041C','YOR054C','YOR043W','YCR067C','YDR150W',
                        'YDR420W','YDR420W','YDR420W','YDR490C','YPL188W']

# Open a CSV file for writing
with open('inositol_gene_pathways_and_compounds.csv', 'w') as csvfile:
    # Define the CSV writer
    csv_writer = csv.writer(csvfile)

    # Write the header row
    header_row = ['Gene_ID', 'Pathway_ID'] + ["Compound_{}:{}".format(compound_name, compound_id) for compound_name in compounds_of_interest for compound_id in get_all_related_compound_ids(compound_name)]
    csv_writer.writerow(header_row)

    # Iterate through gene IDs
    for gene_id in gene_ids_to_check:
        # Get pathway IDs for the current gene
        pathway_ids = get_pathways_for_gene(gene_id)

        # Iterate through pathway IDs
        for pathway_id in pathway_ids:
            # Create a row for the current gene and pathway
            row = [gene_id, pathway_id]

            # Check each compound for presence in the pathway
            for compound_name in compounds_of_interest:
                compound_ids = get_all_related_compound_ids(compound_name)
                for compound_id in compound_ids:
                    result = is_compound_id_in_pathway(compound_id, pathway_id)
                    # Append 1 if the compound is present, else 0
                    row.append(1 if result else 0)

            # Write the row to the CSV file
            csv_writer.writerow(row)
