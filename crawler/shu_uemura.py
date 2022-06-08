from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.shuuemura.com.cn/product/SHUNF00000061", wait_until="networkidle")
    product_name = page.eval_on_selector(".detail-info-text > .product-name", "node => node.innerText")
    product_subtitle = page.eval_on_selector(".detail-info-text > .product-subtitle", "node => node.innerText")
    print(product_name)
    print(product_subtitle)
    color_box = page.locator(".color-wrap").nth(1)
    color_box.click(delay=100)
    handles = page.query_selector_all(".color-box-ul > li > div")
    for handle in handles:
        handle.click(delay=100)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        color = handle.eval_on_selector(".color-main", "node => node.style.backgroundColor")
        variant = handle.eval_on_selector(".color-text", "node => node.innerText")
        image = page.eval_on_selector(".product-big-image-box", "node => node.style.backgroundImage")
        print(color, variant, image)
        color_box.click(delay=100)
        page.wait_for_timeout(1000)
    browser.close()
