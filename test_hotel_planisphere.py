from playwright.sync_api import Page
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pytest


class TestHotelPlanisphere(object):

    @pytest.fixture(scope="function", autouse=True)
    def page_fixture(self, page: Page):
        self.page = page
        yield
        self.page.close()
    
    def setup_method(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()

    def test_before_today(self):
        page = self.page
        self.page.goto("https://hotel.testplanisphere.dev/ja/reserve.html?plan-id=0", wait_until="networkidle")

        # 1.宿泊日を今日の日付に設定
        page.fill("#date", "2024/12/18")
        page.press("#date", "Tab")
        # 2.宿泊日数を3泊に設定
        page.fill("#term", "3")
        # 3.人数を2人に設定
        page.fill("#head-count", "2")
        # 4.お得なプランを選択
        page.check("#sightseeing")
        # 5.お名前に自分の名前を入力
        page.fill("#username", "古賀")
        # 6.確認のご連絡は希望しないを選択
        page.select_option("#contact", "no")
        #  7.予約内容を確認するボタンをクリック
        page.click("#submit-button")
        #  スクリーンショットの保存
        page.screenshot(path="sample.png")

        assert page.text_content("#total-bill") == "合計 44,000円（税込み）", "合計金額が表示されること。"
