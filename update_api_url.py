import subprocess

# Path to your app.js
APP_JS_PATH = 'frontend/static/app.js'

# The placeholder string in app.js to replace
PLACEHOLDER = '__API_GATEWAY_URL__'

def get_terraform_output(output_name):
    result = subprocess.run(
        ["terraform", "-chdir=terraform", "output", "-raw", output_name],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def replace_placeholder_in_file(file_path, placeholder, replacement):
    with open(file_path, 'r') as file:
        content = file.read()

    content = content.replace(placeholder, replacement)

    with open(file_path, 'w') as file:
        file.write(content)

def main():
    api_url = get_terraform_output('api_gateway_url')
    print(f"Replacing placeholder with API URL: {api_url}")
    replace_placeholder_in_file(APP_JS_PATH, PLACEHOLDER, api_url)
    print("Done updating app.js")

if __name__ == '__main__':
    main()
