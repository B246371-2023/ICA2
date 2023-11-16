import requests
import time
import re

def blast_sequence(sequence, api_key, db='nr', program='blastp', email='your_email@example.com'):
    """
    Submit a sequence to NCBI BLAST for searching against specified database.
    """
    params = {
        'CMD': 'Put',
        'DATABASE': db,
        'PROGRAM': program,
        'QUERY': sequence,
        'FORMAT_TYPE': 'Text',
        'EMAIL': email,
        'API_KEY': api_key
    }

    response = requests.post('https://blast.ncbi.nlm.nih.gov/Blast.cgi', data=params)
    if response.status_code != 200:
        raise Exception(f"Error submitting BLAST job: {response.text}")

    print("BLAST Response:", response.text)  # 打印响应内容

    # Use regular expression to extract RID
    rid_search = re.search(r'RID = (.*?)\n', response.text)
    if rid_search:
        rid = rid_search.group(1)
        return rid
    else:
        raise Exception("RID not found in BLAST response.")

def get_blast_results(rid, api_key, sleep_time=30, max_attempts=40):
    """
    Retrieve BLAST search results from NCBI using RID.
    """
    params = {
        'CMD': 'Get',
        'RID': rid,
        'FORMAT_TYPE': 'Text',
        'API_KEY': api_key
    }

    for attempt in range(max_attempts):
        response = requests.post('https://blast.ncbi.nlm.nih.gov/Blast.cgi', data=params)
        if 'Status=WAITING' in response.text:
            print(f"Attempt {attempt + 1}: Result is not ready, waiting for {sleep_time} seconds.")
            time.sleep(sleep_time)
        elif 'Status=READY' in response.text:
            with open(f"{rid}_results.txt", 'w') as file:
                file.write(response.text)
            print(f"Results written to {rid}_results.txt")
            break
        else:
            raise Exception(f"Error retrieving BLAST results: {response.text}")

# Example usage
my_sequence = "MASSMDLLHDAGIRATQWLQEHFQGSQDWFLFISFAADLRNTFFVLFPIWFHFSESVGIRLIWVAVIGDW LNLVFKWILFGERPYWWVHETDYYSNTSAPEIQQFPLTCETGPGSPSGHAMGAAGVYYVMVTALLSTAMG KKQLRTFKYWVLWMVLWMGFWAVQVCVCLSRVFIAAHFPHQVIAGVISGMAVAKTFQHVRCIYNASLRQY LGITFFLFSFALGFYLLLRVLGVDLLWTLEKAQRWCSHPEWVHIDTTPFASLLRNLGILFGLGLALNSHM YQESCQGKQGPQLPFRLGCIAASLLILHLFDAFKPPSHMQLLFYILSFCKSAAVPLATVGLIPYCISQLL ATQDKKAA"
my_api_key = "9570bdf95400b6e4c57a2ef852119f49e008"
email = "1439151477@qq.com"

rid = blast_sequence(my_sequence, my_api_key, email=email)
get_blast_results(rid, my_api_key)
