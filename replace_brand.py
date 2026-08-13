import os

directory = '/Users/anatolichastik/Documents/WEB-MURTAZA/WEB-MURTAZA/src'
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(('.html', '.njk', '.md')):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Rebrand Replacements
            new_content = content.replace('ChasTech', 'Murtaza Homes')
            new_content = new_content.replace('chastech.ca', 'murtazahomes.com')
            new_content = new_content.replace('hello@chastech.ca', 'info@murtazahomes.com')
            new_content = new_content.replace('Chastech', 'Murtaza Homes')

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")

print("Replacement Complete.")
