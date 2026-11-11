from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800}
    )
    page = context.new_page()
    
    print("Navigating to Cricbuzz...")
    page.goto("https://www.cricbuzz.com/", timeout=60000)
    
    # Use a flexible locator that targets match lists or carousel links anywhere on the page
    # Instead of wait_for_selector crashing, we can locate links or blocks containing score indicators
    print("Waiting for match score elements...")
    
    try:
        # Wait for any element containing match scores or list blocks to render
        page.wait_for_selector("li.cb-mtch-lst, div.cb-col-25, a[href*='/live-cricket-scores/']", timeout=20000)
        
        # Grab the first live score container element available
        match_element = page.locator("li.cb-mtch-lst, div.cb-col-25, a[href*='/live-cricket-scores/']").first
        score = match_element.inner_text()
        
        print("\n--- Match Score Found ---")
        print(score)
        print("-------------------------")
        
        # Take a screenshot of the score element
        match_element.screenshot(path="score.png")
        print("saved score.png")
        
    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="debug_full_page.png", full_page=True)
        print("Saved debug_full_page.png for troubleshooting.")
        
    browser.close()