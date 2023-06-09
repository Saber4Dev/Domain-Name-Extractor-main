import os
import time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Style

# Function to check if a directory path is valid
def validate_path(path):
    if os.path.isdir(path):
        print("Selected path:", path, "✓")
        return True
    else:
        print("Invalid path. Please enter a valid path.")
        return False

def select_project_file(path):
    projects = glob.glob(os.path.join(path, "*", "project.txt"))
    if not projects:
        print("No project files found in the specified path.")
        return None
    print("Available project files:")
    for i, project_file in enumerate(projects):
        print(f"{i+1}. {project_file}")
    choice = input("Enter the number of the project file: ")
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(projects):
            raise ValueError
        return projects[index]
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid number.")
        return None

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
    print(Fore.BLUE + "+------------------------------------+")
    print("|          Result              |")
    print("+------------------------------------+")
    print("|   Company name           | Domain name             | Information Supplementary  |")
    print("+------------------------------------+")

    for company_name, domain_name, info_supplementary in domain_info_list:
        print(f"|   {company_name:<23} | {domain_name:<22} | {info_supplementary:<26} |")

    print("+------------------------------------+")
    print(Style.RESET_ALL)

# Function to export domain information to a text file
def export_domains(project_folder):
    project_files = get_project_files(project_folder)

    if not project_files:
        print("No project files found in the specified folder.")
        return

    print("\n--- Exporting Domain Information ---\n")

    domain_info_list = []
    for project_file in project_files:
        company_name, domain_name, info_supp = extract_domain_info(project_file)
        domain_info_list.append((company_name, domain_name, info_supp))

    display_domain_info(domain_info_list)

    export_choice = input("Do you want to export the domain information to a file? (y/n): ")
    if export_choice.lower() == "y":
        export_file_name = "Domain-Export.txt"
        export_path = os.path.join(os.path.dirname(__file__), "Domain Exported", export_file_name)

        with open(export_path, "w") as f:
            f.write("+------------------------------------+\n")
            f.write("|          Result              |\n")
            f.write("+------------------------------------+\n")
            f.write("|   Company name           | Domain name             | Information Supplementary  |\n")
            f.write("+------------------------------------+\n")
            for company_name, domain_name, info_supp in domain_info_list:
                f.write(f"|   {company_name:<23} | {domain_name:<22} | {info_supp:<26} |\n")
            f.write("+------------------------------------+\n")

        print(f"\nDomain information exported to: {export_path}")
    else:
        print("\nDomain information export canceled.")

# Function to capture website screenshot
def capture_screenshot(url, file_path):
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--start-maximized")  # Maximize the browser window
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

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
    print("==============================================\n")
    path = input("Enter the path of the projects folder: ")
    while not validate_path(path):
        path = input("Enter the path of the projects folder: ")

    project_file = None
    
    while True:
        print("\nSelect an option:")
        print("1. Choose the project file")
        print("2. Export domain information to a file")
        print("3. Capture website screenshots")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            project_file = select_project_file(path)
            if project_file:
                print("Selected project file:", project_file)

        elif choice == "2":
            if project_file:
                export_domains(project_file)

        elif choice == "3":
            if project_file:
                capture_screenshot(project_file)

        elif choice == "4":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
