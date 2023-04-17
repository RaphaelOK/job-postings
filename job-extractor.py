import streamlit as st
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

st.title("Job Data Extractor")
options = ["Backend Engineer", "Frontend Engineer", "Software Engineer", "Mobile Developer"]
selected_option = st.selectbox("Select a job category", options)

if selected_option:
    option_parts = selected_option.split(" ")
    new_option = "+".join(option_parts)

# Use the selected option to navigate to a website
if selected_option:
    st.write("You selected `%s`" % selected_option)

    # Set up the headless browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)

    # Navigate to the first page of the website
    url = f"https://portfoliojobs.a16z.com/jobs?jobTypes={new_option}"
    browser.get(url)

    jobs = []
    companies = []
    skill_list = []
    location_list = []
    addition = []

    while True:
        # Scroll to the bottom of the page to load the lazy-loaded content
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        html = browser.page_source

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        job_list = soup.find('div', {'class': 'job-list'})
        job_list_filter = soup.find('div', {'class': 'job-list-filter-value'}).text
        print(job_list_filter)

        job_items = job_list.find_all('div', {'class': 'job-list-job'})

        # print(job_items)
        job_description_list = []
        skill_set_list = []
        work_venue = []
        comp_name = []
        remote_status = []
        grand_job = []
        for i in job_items:
            remote = i.find_all('div', {'class': 'job-list-badges'})
            company_name = i.find_all('a', {'class': 'job-list-job-company-link'})
            job_description = i.find_all('h2', {'class': 'job-list-job-title'})
            job_skills = i.find_all('div', {'class': 'job-list-job-skills'})
            venue = i.find_all('div', {'class': 'job-list-job-details'})
            for rem in remote:
                remotely = rem.find('span', {'class': 'job-list-badge-text'})

                for item in remotely:
                    remote_jobs = item.text

                    if remote_jobs.lower() != 'work remotely':
                        remote_jobs = 'Remotely Unavailable'
                        remote_status.append(remotely.text)

            for c in company_name:
                name = c.text
                comp_name.append(name)
            for v in venue:
                new_venue = v.find('span', {'class': 'job-list-company-meta-item'})
                number = v.find_all('span', {'class': 'job-list-company-meta-item'})[1]
                comp_link = v.find_all('a')
                for link in comp_link:
                    urls = link.get('href')
                for n in number:
                    num_text = n.text

                for thing in new_venue:
                    new_venue1 = thing.text

                    work_venue.append(new_venue1)
            for s in job_skills:
                skills = s.text
                skill_set_list.append(skills)
            for j in job_description:
                jobs_new = j.text
                job_description_list.append(jobs_new)
                grand_job.append(
                    {'Job Category': job_list_filter, 'Company_Name': name, 'Location': new_venue1, 'Skills': skills,
                     'Job_Description': jobs_new,
                     'Remote_Options': remote_jobs, 'Number_of_employees': num_text, 'Company_url': urls})

        # Display the extracted job data in a table
        st.write("Job Data")
        df = pd.DataFrame(grand_job)
        st.dataframe(df)

        try:
            next_button = browser.find_element_by_css_selector(".next-button")
        except:
            break

        if not next_button.is_enabled():
            break

        # Click on the next page button
        next_button.click()
