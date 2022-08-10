# Beautiful Soup for webscraping
# Request for sending request on chosen URL
# writer for storing web-scraped data to .csv file
from bs4 import BeautifulSoup
import requests
from csv import writer
import time


# Function that generates the search URL based on the input Job Title of the user
def urlGenerator():
    url_for_search = 'https://ph.indeed.com/jobs?q='
    word_counter = 0
    search_word_count = len(job_to_search.split())
    for url_bits in job_to_search.split():
        url_for_search += url_bits
        word_counter += 1
        if word_counter == search_word_count:
            url_for_search += '&'
        else:
            url_for_search += '+'
    return url_for_search

# Function for writing and appending new data to .csv
def csv_maker():
    with open('JobsSalary.csv', 'a+', encoding='utf8', newline='') as f:
        the_writer = writer(f)
        header = ['Job Title', 'Company Name', 'Fixed Salary', 'Min Salary', 'Max Salary']
        the_writer.writerow(header)

# Function that executes the webscraping where the parameter is the generated URL
def searchStart(urlGet):
    time.sleep(0.5)
    html_text = requests.get(urlGet).text
    soup = BeautifulSoup(html_text, 'lxml')
    with open('JobsSalary.csv', 'a+', encoding='utf8', newline='') as f:
        the_writer = writer(f)
        job_list = soup.find('ul', class_='jobsearch-ResultsList css-0')
        jobs = job_list.find_all('td', class_='resultContent')
        for job in jobs:
            job_title = job.find('h2').text
            company_name = job.find('span', class_='companyName').text
            if key_job_title.upper() in job_title.upper():
                try:
                    salary = job.find('div', class_='attribute_snippet').text
                    if salary.split()[3] == "month":
                        dir_salary = salary.split()[1]
                        extracted_data = [job_title, company_name, dir_salary, "N/A", "N/A"]
                        the_writer.writerow(extracted_data)

                    else:
                        min_salary = salary.split()[1]
                        max_salary = salary.split()[4]
                        extracted_data = [job_title, company_name, "N/A", min_salary, max_salary]
                        the_writer.writerow(extracted_data)
                except:
                    dir_salary = "no salary"
                    extracted_data = [job_title, company_name, dir_salary, "N/A", "N/A"]
                    the_writer.writerow(extracted_data)
            else:
                extracted_data = [f'Not {key_job_title} related', "N/A", "N/A", "N/A", "N/A"]
                the_writer.writerow(extracted_data)

# specific function that adds a detail in the generated URL of urlGenerator based on the number of pages that the user defined
def urlWithPages(pages):
    urlGenerator()
    return urlGenerator() + 'start=' + str((pages - 1) * 10)

# where user will input the job title.
job_to_search = input("Input Job Title to search: ")

# Key job title was a more specific key word from initial version. Not really needed because the URL generator was improved significantly over the course of the coding.
key_job_title = input("Input a key Job Title: ")

# below will generate the number of max pages for the job title, this ensures that use will not input more than the max pages available in the search
urlGenerator()
html_text = requests.get(urlGenerator()).text
soup = BeautifulSoup(html_text, 'lxml')
try:
    max_page = soup.find('div', id='searchCountPages').text
    print(f'{max_page.split()[3]} max pages')
except:
    # except was added here as there are instances where indeed website will not show the max generated pages
    print("Try again or enter a number max 10 in the next entry.")

# input on how many pages of data would the user want to extract
max_page_by_user = int(input("Insert how many pages you want to extract (more pages, bigger data): "))

# Try and Except was used to have results when given job title was user return no results
try:
    if max_page_by_user <= 1:
        # if pages are set to 1 or nothing, only generates data for the first page only
        urlGenerator()
        csv_maker()
        searchStart(urlGenerator())
    else:
        # if pages are set to more than 1, for loop will loop based on the number of max pages. It will generate the URL first then execute the webscraping per page then loop through until last page is reached.
        csv_maker()
        for x in range(1, max_page_by_user+1):
            urlWithPages(x)
            searchStart(urlWithPages(x))
    print("Data Generation Success")
except:
    print("No results from given keywords")
