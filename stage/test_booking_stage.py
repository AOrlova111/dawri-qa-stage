лfrom playwright.sync_api import sync_playwright

def test_venue_facility_booking_stage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("\n--- Сценарій: Повний цикл бронювання на Stage ---")

        # 1. Перехід на головну сторінку Stage
        page.goto("https://stage-dawri.pprnd.co/", timeout=60000)
        page.wait_for_load_state("networkidle")

        # 2. Чітке перемикання мови на EN (без зачіпання меню)
        print("1. Перемикаємо мову на EN...")
        en_button = page.get_by_text("EN", exact=True)
        if en_button.is_visible():
            en_button.click()
            page.wait_for_timeout(1000)

        # 3. Натискаємо SEARCH на головній сторінці
        print("2. Натискаємо SEARCH...")
        search_button = page.get_by_role("button", name="SEARCH")
        search_button.click()

        # 4. Перехід на сторінку з Venue, обираємо "venue stage"
        print("3. Обираємо 'venue stage'...")
        page.wait_for_selector("text=venue stage", timeout=15000)
        venue_stage = page.get_by_text("venue stage", exact=True)
        venue_stage.scroll_into_view_if_needed()
        venue_stage.click()

        # 5. Перехід на сторінку фасіліті, обираємо "facility stage"
        print("4. Обираємо 'facility stage'...")
        page.wait_for_selector("text=facility stage", timeout=15000)
        facility_stage = page.get_by_text("facility stage", exact=True)
        facility_stage.click()

        # 6. Натискаємо BOOK SERVICE
        print("5. Натискаємо 'BOOK SERVICE'...")
        book_service_btn = page.get_by_role("button", name="BOOK SERVICE")
        book_service_btn.click()

        # 7. Обираємо Single session
        print("6. Перевіряємо вибір 'Single session'...")
        single_session_radio = page.get_by_label("Single session")
        if not single_session_radio.is_checked():
            single_session_radio.check()

        # 8. Відкриваємо вибір часу (Choose time) і вибираємо слоти
        print("7. Обираємо час та слоти...")
        choose_time_btn = page.get_by_text("Choose time")
        choose_time_btn.click()

        page.wait_for_selector("text=Min slots amount", timeout=10000)
        available_slots = page.locator("button:has-text('AM'), button:has-text('PM')")
        
        if available_slots.count() >= 2:
            available_slots.nth(0).click()
            available_slots.nth(1).click()
        else:
            available_slots.nth(0).click()

        # 9. Натискаємо CONTINUE
        print("8. Натискаємо 'CONTINUE'...")
        continue_btn = page.get_by_role("button", name="CONTINUE")
        continue_btn.click()

        # 10. Натискаємо CONFIRM
        print("9. Натискаємо перший 'CONFIRM'...")
        confirm_btn_1 = page.locator("button:has-text('CONFIRM')").first
        confirm_btn_1.click()

        # 11. На наступній сторінці натискаємо PAYMENT
        print("10. Натискаємо 'PAYMENT'...")
        page.wait_for_selector("button:has-text('PAYMENT')", timeout=15000)
        payment_btn = page.get_by_role("button", name="PAYMENT")
        payment_btn.click()

        # 12. Обираємо Payment Method (Wallet/Cash)
        print("11. Обираємо метод оплати...")
        page.wait_for_selector("text=Payment options", timeout=15000)
        wallet_checkbox = page.locator("input[type='checkbox']").first
        if not wallet_checkbox.is_checked():
            wallet_checkbox.check()

        # 13. Натискаємо CONFIRM
        print("12. Натискаємо 'CONFIRM'...")
        confirm_payment_opt_btn = page.get_by_role("button", name="CONFIRM")
        confirm_payment_opt_btn.click()

        # 14. Підтверджуємо CONFIRM PAYMENT
        print("13. Підтверджуємо 'CONFIRM PAYMENT'...")
        confirm_final_btn = page.get_by_role("button", name="CONFIRM PAYMENT")
        confirm_final_btn.click()

        # 15. Перевірка успішності бронювання
        print("14. Перевіряємо успішність бронювання...")
        page.wait_for_selector("text=Booking details", timeout=20000)
        
        assert "booking-details" in page.url or page.locator("text=Upcoming").is_visible()
        print("✅ Тест успішно пройдено! Бронювання створено.")

        browser.close()

if __name__ == "__main__":
    test_venue_facility_booking_stage()
