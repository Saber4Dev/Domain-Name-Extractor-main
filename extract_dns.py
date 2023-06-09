import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Function to extract domain information from a project text file
def extract_domain_info(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    company_name = get_field_value(content, "Nom de l'entreprise sur le site web :")
    domain_name = get_field_value(content, "Nom de domaine souhaité :")
    info_supplementary = get_field_value(content, "Informations supplémentaires :")

    return company_name, domain_name, info_supplementary

# Function to retrieve the value of a specific field from the content
def get_field_value(content, field_name):
    start_index = content.find(field_name)
    if start_index != -1:
        start_index += len(field_name)
        end_index = content.find("\n", start_index)
        value = content[start_index:end_index].strip()
        return value
    return ""

# Function to display domain information in a table format
def display_domain_info(domain_info_list):
    print("+------------------------------------+")
    print("|          Result              |")
    print("+------------------------------------+")
    print("|   Company name           | Domain name             | Information Supplementary  |")
    print("+------------------------------------+")

    for company_name, domain_name, info_supplementary in domain_info_list:
        print(f"|   {company_name:<23} | {domain_name:<22} | {info_supplementary:<26} |")

    print("+------------------------------------+")

# Function to export domain information to a text file
def export_domain_info(domain_info_list, export_file_path):
    with open(export_file_path, "w") as f:
        f.write("Company Name\tDomain Name\tInformation Supplementary\n")
        for company_name, domain_name, info_supplementary in domain_info_list:
            f.write(f"{company_name}\t{domain_name}\t{info_supplementary}\n")

# Function to capture website screenshot
def capture_screenshot(url, file_path):
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--start-maximized")  # Maximize the browser window
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(chrome_options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        driver.save_screenshot(file_path)
        print(f"Screenshot captured: {file_path}")
    except:
        print(f"Failed to capture screenshot for URL: {url}")

    driver.quit()

# Main program
def main():
    print("Welcome to the Domain Extractor and Website Screenshot Capture!")
    print("==============================================================\n")

    projects_path = input("Enter the path of the projects folder: ")

    project_files = []
    domain_info_list = []

    # Retrieve project text files from the projects folder
    for root, dirs, files in os.walk(projects_path):
        for file in files:
            if file.endswith(".txt"):
                project_files.append(os.path.join(root, file))

    # Extract domain information from project text files
    for file_path in project_files:
        domain_info = extract_domain_info(file_path)
        if domain_info[1]:  # Check if domain name is not empty
            domain_info_list.append(domain_info)

    # Display domain information in the terminal
    display_domain_info(domain_info_list)

    while True:
        print("\nSelect an option:")
        print("1. Capture website screenshots")
        print("2. Export domain information to a file")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Capture website screenshots
            screenshot_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Website Screenshots")
            os.makedirs(screenshot_folder, exist_ok=True)

            for company_name, domain_name, _ in domain_info_list:
                url = f"https://{domain_name}"
                file_name = f"{company_name} - {domain_name}.png"
                file_path = os.path.join(screenshot_folder, file_name)

                capture_screenshot(url, file_path)

        elif choice == "2":
            # Export domain information to a text file
            export_choice = input("\nDo you want to export the domain information to a file? (yes/no): ")
            if export_choice.lower() == "yes":
                export_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Domain Exported", "Domain-name.txt")
                export_domain_info(domain_info_list, export_file_path)
                print(f"\nDomain information exported to: {export_file_path}")
            else:
                print("Domain information not exported.")

        elif choice == "3":
            break

    print("\nExiting the program...")

if __name__ == "__main__":
    main()
