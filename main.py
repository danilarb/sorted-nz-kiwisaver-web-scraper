"""
This is a simple example of a web scraper that uses Selenium and BeautifulSoup to scrape data.
"""
import time
import json
import csv
import os

import selenium
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

AGE = int(os.environ['AGE'])
RETIREMENT_AGE = int(os.environ['RETIREMENT_AGE'])
YEARS_LEFT = RETIREMENT_AGE - AGE
SALARY = float(os.environ['SALARY'])
CURRENT_BALANCE = float(os.environ['CURRENT_BALANCE'])
GOVT_CONTRIBUTION = float(os.environ['GOVT_CONTRIBUTION'])
SALARY_SACRIFICES = [0.03, 0.04, 0.06, 0.08, 0.1]
EMPLOYER_CONTRIBUTIONS = [0.03, 0.04]


def main():
    """
    Script entry point
    """
    if not os.path.isfile('sorted.html'):
        html_content = parse_html()
    else:
        with (open('sorted.html', 'r', encoding='utf-8')) as file:
            html_content = file.read()

    print('Loaded HTML')

    soup = BeautifulSoup(html_content, 'html.parser')

    if not os.path.isfile('sorted.html'):
        with (open('sorted.html', 'w', encoding='utf-8')) as file:
            file.write(soup.prettify())

        print('Written HTML to file')
    print('Starting conversion')
    my_funds = get_my_funds(soup)
    print('Conversion successful')
    write_json_csv_files(my_funds)
    print('Done')


def parse_html():
    """
    Parse the html with selenium webdriver
    """
    url = ('https://smartinvestor.sorted.org.nz/kiwisaver-and-managed-funds/'
           '?fundTypes=all-fund-types&managedFundTypes=kiwisaver&sort=growth-assets-asc')

    driver = selenium.webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(20)  # wait 20 seconds max for elements to load

    close_modal_button = driver.find_element(By.CLASS_NAME, "leadinModal-close")
    close_modal_button.click()

    while True:
        try:
            load_more_button = driver.find_element(By.CLASS_NAME, "Pagination__button")
            load_more_button.click()
            time.sleep(5)
        except selenium.common.exceptions.NoSuchElementException:
            print('Finished scraping')
            break

    print('Starting to parse')
    html_content = driver.page_source
    driver.quit()
    print('Finished parsing')
    return html_content


def get_my_funds(soup):
    """
    Gets a formatted array of all applicable funds
    """
    all_funds = soup.find_all('div', class_='FundTile')
    my_funds = []

    for fund in all_funds:
        current_fund = get_current_fund(fund)

        if current_fund is not None and current_fund not in my_funds:
            my_funds.append(current_fund)

    return my_funds


def get_current_fund(fund):
    """
    Finds values of the current fund and formats them
    """
    fund_values = fund.find_all('div', class_='DoughnutChartWrapper__main-val')
    return_percentage = fund_values[1].text.strip().split('\n')[0].strip()

    # We skip funds that don't have five-year data
    if return_percentage == 'No five-year data available':
        return None

    if return_percentage[-1] == '%':
        return_percentage = return_percentage[:-1]

    fee_percentage = fund_values[0].text.strip().split('\n')[0].strip()

    if fee_percentage[-1] == '%':
        fee_percentage = return_percentage[:-1]

    return_percentage = float(return_percentage)
    fee_percentage = float(fee_percentage)

    provider_name = fund.find('p', class_='FundTile__category').text.strip()
    fund_name = fund.find('h3', class_='FundTile__title').text.strip()
    fund_link = fund.find('a', href=True)['href']

    try:
        fund_category = fund.find_all(
            'span',
            class_='Tag FundTile__tag'
        )[1].text.strip().split('\n')[-1].strip()
    except IndexError:
        # Some funds don't have an Aggressive, Conservative, etc. tag
        fund_category = 'N/A'

    current_fund = [
        provider_name,
        fund_name,
        fund_link,
        fund_category,
        fee_percentage,
        return_percentage
    ]

    for employee_contribution in EMPLOYER_CONTRIBUTIONS:
        for salary_sacrifice in SALARY_SACRIFICES:
            final_balance = calculate_compound_interest_with_deposits(
                return_percentage,
                fee_percentage,
                salary_sacrifice,
                employee_contribution
            )
            current_fund.append(final_balance)

    return current_fund


def calculate_compound_interest_with_deposits(rate, fees, sacrifice, employer):
    """
    Calculates your final balance with the fund
    """
    final_rate = rate / 100 - fees / 100
    yearly_contribution = calculate_yearly_contribution(sacrifice, employer)

    if final_rate == 0:
        return round(CURRENT_BALANCE + yearly_contribution * YEARS_LEFT, 2)

    principal_interest = calculate_principal_interest(final_rate)
    contributions_interest = calculate_contributions_interest(yearly_contribution, final_rate)
    # Calculate the total future value
    future_value = principal_interest + contributions_interest

    return round(future_value, 2)


def calculate_yearly_contribution(sacrifice, employer):
    """
    Calculate the yearly deposit based on your income
    """
    yearly_contribution = (SALARY * sacrifice) + (SALARY * employer)
    govt_contribution = min(yearly_contribution, GOVT_CONTRIBUTION)
    return yearly_contribution + govt_contribution


def calculate_principal_interest(final_rate: float):
    """
    Calculate the compound interest on the initial principal
    """
    return CURRENT_BALANCE * ((1 + final_rate) ** YEARS_LEFT)


def calculate_contributions_interest(yearly_contribution: float, final_rate: float):
    """
    Calculate the compound interest on the additional yearly deposits
    """
    return yearly_contribution * (((1 + final_rate) ** YEARS_LEFT) - 1) * (1 / final_rate)


def write_json_csv_files(my_funds):
    """
    Writes the processed funds to a json and csv file
    """
    with open('sorted.json', 'w', encoding='utf-8') as file:
        json.dump(reformat_for_json(my_funds), file, ensure_ascii=False, indent=4)
        print('Written to JSON')

    with open('sorted.csv', 'w', encoding='utf-8') as file:
        write = csv.writer(file)
        write.writerow(get_headers())
        write.writerows(my_funds)
        print('Written to CSV')


def reformat_for_json(my_funds):
    """
    Formats the funds list for a json file
    """
    headers = get_headers()
    json_funds = []
    for fund in my_funds:
        json_funds.append({
            headers[0]: fund[0],
            headers[1]: fund[1],
            headers[2]: fund[2],
            headers[3]: fund[3],
            headers[4]: fund[4],
            headers[5]: fund[5],
            headers[6]: fund[6],
            headers[7]: fund[7],
            headers[8]: fund[8],
            headers[9]: fund[9],
            headers[10]: fund[10],
            headers[11]: fund[11],
            headers[12]: fund[12],
            headers[13]: fund[13],
            headers[14]: fund[14],
            headers[15]: fund[15]
        })

    return json_funds


def get_headers():
    """
    Returns the CSV column headers
    """
    return [
        'Provider',
        'Fund Name',
        'Fund Link',
        'Fund Category',
        'Fee %',
        'Return % (last 5 years)',
        'Estimated Final Balance (Salary Sacrifice at 3%, ' +
        'Employer Contribution at 3% and maximum Government Contribution)',
        'Estimated Final Balance (Salary Sacrifice at 4%, ' +
        'Employer Contribution at 3% and maximum Government Contribution)',
        'Estimated Final Balance (Salary Sacrifice at 6%, ' +
        'Employer Contribution at 3% and maximum Government Contribution)',
        'Estimated Final Balance (Salary Sacrifice at 8%, ' +
        'Employer Contribution at 3% and maximum Government Contribution)',
        'Estimated Final Balance (Salary Sacrifice at 10%, ' +
        'Employer Contribution at 3% and maximum Government Contribution)',
        'Estimated Final Balance (Salary Sacrifice at 3%, ' +
        'Employer Contribution at 4% and maximum Government Contribution)',
        'Estimated Final Balance (Salary Sacrifice at 4%, ' +
        'Employer Contribution at 4% and maximum Government Contribution)',
        'Estimated Final Balance (Salary Sacrifice at 6%, ' +
        'Employer Contribution at 4% and maximum Government Contribution)',
        'Estimated Final Balance (Salary Sacrifice at 8%, ' +
        'Employer Contribution at 4% and maximum Government Contribution)',
        'Estimated Final Balance (Salary Sacrifice at 10%, ' +
        'Employer Contribution at 4% and maximum Government Contribution)'
    ]


if __name__ == '__main__':
    main()