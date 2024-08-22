import requests
import json
from playwright.sync_api import sync_playwright

url = "http://localhost:11434/api/generate"

headers = {
    "Content-Type":"application/json"
}

def fetch_test_script(prompt):

    data = {
        "model": "codellama:latest",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("response")
    else:
        raise Exception(f"Error fetching test script: {response.status_code} - {response.text}")


# to be generated by ai
test_script = '''() => {            
                send('mango');
                click();
            }'''

browser = None
page = None

def read_prompt_from_file(filename):
    with open(filename, 'r') as file:
        prompt = file.read().strip()
    return prompt

def open_browser(p):
    global browser, page    
    print("Launch browser...")
    browser = p.chromium.launch(headless=True) 
    context = browser.new_context()           
    page = context.new_page()

def close_browser():   
    global browser, page
    try:
        if browser:
            print("Closing browser...")
            page.close()
            browser.close()
    except Exception as e:
        print("****") 

def search_and_assert_mango():
    global page       
    try:
        with sync_playwright() as p:
            open_browser(p)                                  
            
            page.goto('https://www.google.com/')    
            page.wait_for_load_state("networkidle")            
            
            print("Inject JS...")
            with open('basic-actions.js', 'r') as js_file:
                js_code = js_file.read()                
                page.add_script_tag(content=js_code)        
                page.wait_for_load_state("networkidle")            
            
            # Read prompt from a text file
            prompt_file = 'prompt.txt'
            prompt = read_prompt_from_file(prompt_file)
            # print(f"Read prompt from file '{prompt_file}': {prompt}")

            # Fetching test_script dynamically based on a prompt            
            test_script = fetch_test_script(prompt)
            print("Output:")
            print(test_script)

            print("Run Scripts...")            
            page.evaluate(test_script)
            
            page.wait_for_load_state("networkidle")
            page.wait_for_function('''() => {
                return document.readyState === 'complete' && !window.isLoading;
            }''')

            assert_0()       
            print("Done...")

    except Exception as e:
        print(f"Error occurred: {e}")
        input("Press Enter to close the browser...")

    finally:       
        close_browser()
        

def assert_0 ():   
    global page 
    print("assert_0:", end=" ")
    assert "mango" in page.content().lower(), "Failed assertion: 'mango' not found in page."
    print("Passed")

if __name__ == "__main__":
    search_and_assert_mango()
