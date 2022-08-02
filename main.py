from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://ph.indeed.com/jobs?q=python%20data%20engineer&fromage=1&vjk=c034bf4d2b573e1c').text
soup = BeautifulSoup(html_text, 'lxml')
job_list = soup.find('ul', class_='jobsearch-ResultsList css-0')
jobs = job_list.find_all('td', class_='resultContent')

for job in jobs:
    job_title = job.find('h2').text

    company_name = job.find('span', class_='companyName').text
    print('')
    print(f"Job Title: {job_title.strip()}")
    print(f"Company Name: {company_name.strip()}")
    try:
        salary = job.find('div', class_='attribute_snippet').text
        if salary.split()[3] == "month":
            dir_salary = salary.split()[1]
            print(f"Salary: {dir_salary.strip()}")

        else:
            min_salary = salary.split()[1]
            max_salary = salary.split()[4]
            print(f"Salary: {min_salary.strip()} to {max_salary.strip()}")

    except:
        dir_salary = "no salary"
        print(f"Salary: {dir_salary.strip()}")

