from playwright.sync_api import sync_playwright
import time
import os

def take_screenshots():
    # Make sure plots directory exists
    os.makedirs('../plots', exist_ok=True)
    
    with sync_playwright() as p:
        # Launch headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1200, "height": 900})
        
        # Navigate to Streamlit
        print("Navigating to Streamlit app...")
        page.goto("http://localhost:8501")
        
        # Wait for Streamlit to load completely
        page.wait_for_selector(".stApp")
        time.sleep(5)  # Wait for charts to render
        
        # Screenshot Tab 1
        print("Taking screenshot of Tab 1 (Overview)...")
        page.screenshot(path="../plots/streamlit_tab1_overview.png")
        
        # Click Tab 2
        print("Clicking Tab 2 (Driver Analysis)...")
        page.click("button:has-text('Driver Analysis')")
        time.sleep(2)
        page.screenshot(path="../plots/streamlit_tab2_drivers.png")
        
        # Click Tab 3
        print("Clicking Tab 3 (Retention Action List)...")
        page.click("button:has-text('Retention Action List')")
        time.sleep(2)
        page.screenshot(path="../plots/streamlit_tab3_roi.png")
        
        browser.close()
        print("Screenshots saved successfully!")

if __name__ == "__main__":
    take_screenshots()
