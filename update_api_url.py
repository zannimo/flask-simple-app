import subprocess
import shutil
import os

# Paths
TEMPLATE_JS_PATH = 'frontend/static/app.js.template'  # The template with placeholder
TARGET_JS_PATH = 'frontend/static/app.js'            # The generated file that will be uploaded

PLACEHOLDER = '__API_GATEWAY_URL__'

def get_terraform_output(output_name):
    result = subprocess.run(
        ["terraform", "-chdir=terraform", "output", "-raw", output_name],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def generate_app_js(template_path, target_path, api_url):
    # Copy template first
    shutil.copyfile(template_path, target_path)

    # Replace placeholder with actual API URL
    with open(target_path, 'r') as f:
        content = f.read()

    content = content.replace(PLACEHOLDER, api_url)

    with open(target_path, 'w') as f:
        f.write(content)

def main():
    api_url = get_terraform_output('api_gateway_url')
    print(f"Generating app.js with API URL: {api_url}")
    generate_app_js(TEMPLATE_JS_PATH, TARGET_JS_PATH, api_url)
    print("app.js generated successfully.")

if __name__ == '__main__':
    main()
