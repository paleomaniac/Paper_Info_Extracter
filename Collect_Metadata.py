import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_affiliations_and_numbers(url):
    """
    Extract affiliations and their corresponding numbers from a PubMed article.

    Args:
        url (str): The URL of the PubMed article.

    Returns:
        dict: A dictionary with the number as the key and the affiliation as the value.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    affiliations_dict = {}

    # Find the affiliations section
    affiliations_section = soup.find_all('div', class_='affiliations')
    if affiliations_section:
        for item in affiliations_section:
            affiliation_list = item.find_all('li')
            for aff in affiliation_list:
                # Extract the affiliation number and text
                number = aff.find('sup').get_text(strip=True)
                affiliation = aff.get_text(strip=True).replace(number, '').strip()
                affiliations_dict[int(number)] = affiliation

    return affiliations_dict

def extract_authors_and_numbers(url):
    """
    Extract authors and their corresponding affiliation numbers from a PubMed article.

    Args:
        url (str): The URL of the PubMed article.

    Returns:
        dict: A dictionary with the author's name as the key and a list of numbers as the value.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    authors_dict = {}

    # Find the author elements
    authors_elements = soup.find_all('a', class_='full-name')
    # Find the affiliation elements
    affiliation_elements = soup.find_all('sup')

    for author_elem in authors_elements:
        author_name = author_elem.get_text(strip=True)
        numbers = []
        for aff_elem in author_elem.find_next_siblings('sup'):
            numbers_text = aff_elem.get_text(strip=True)
            numbers.extend(int(num) for num in numbers_text if num.isdigit())
        authors_dict[author_name] = numbers

    return authors_dict

def extract_article_info(url):
    """
    Extract the publication year, PMID, and title from a PubMed article.

    Args:
        url (str): The URL of the PubMed article.

    Returns:
        tuple: A tuple containing the year, PMID, and title.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the title
    title = soup.find('h1', class_='heading-title').get_text(strip=True)
    
    # Extract the PMID
    pmid = soup.find('strong', class_='current-id').get_text(strip=True)
    
    # Extract the publication date
    pub_date = soup.find('span', class_='cit').get_text(strip=True)
    pub_date_parts = pub_date.split()
    
    # Extract the year (assuming it's the last part of the date string)
    for part in pub_date_parts:
        if part.isdigit() and len(part) == 4:  # checking for a 4-digit year
            year = part
            break
    
    return year, pmid, title

def combine_article_info(urls):
    """
    Combine information from multiple PubMed articles into a single DataFrame.

    Args:
        urls (list): A list of URLs of the PubMed articles.

    Returns:
        DataFrame: A DataFrame containing combined information from the articles.
    """
    all_table_data = []

    for url in urls:
        # Extract the individual information
        affiliations_dict = extract_affiliations_and_numbers(url)
        authors_dict = extract_authors_and_numbers(url)
        year, pmid, title = extract_article_info(url)

        # Prepare data for the table
        for author, numbers in authors_dict.items():
            for number in numbers:
                affiliation = affiliations_dict.get(number, "")
                all_table_data.append({
                    "Year": year,
                    "PMID": pmid,
                    "Title": title,
                    "Author": author,
                    "Affiliation Number": number,
                    "Affiliation": affiliation
                })

    # Create a DataFrame
    df = pd.DataFrame(all_table_data)
    return df

# Example usage:
urls = ['https://pubmed.ncbi.nlm.nih.gov/32269234/', 'https://pubmed.ncbi.nlm.nih.gov/34370580/']
df = combine_article_info(urls)
df.to_csv("Ellie_Paper_Information.csv", index=False)
