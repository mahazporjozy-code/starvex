import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class StarvexSourceContractTests(unittest.TestCase):
    def test_navigation_callbacks_are_handled_before_unknown_callbacks(self):
        source = (ROOT / "bot.py").read_text(encoding="utf-8")
        handler = source.split("async def buttons", 1)[1].split(
            "async def receive_order", 1
        )[0]
        navigation = handler.index('query.data in ("home", "main_menu")')
        product = handler.index('if query.data == "premium"')
        self.assertLess(navigation, product)
        self.assertIn("reply_markup=main_menu()", handler[navigation:product])

    def test_order_is_forwarded_to_configured_admin_before_success(self):
        source = (ROOT / "bot.py").read_text(encoding="utf-8")
        self.assertIn('ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")', source)
        self.assertIn(
            'await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)',
            source,
        )
        delivery = source.index(
            'await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)'
        )
        success = source.index('"✅ درخواستت با موفقیت برای مدیریت ارسال شد.')
        self.assertLess(delivery, success)
        self.assertIn("ثبت خودکار سفارش در حال حاضر فعال نیست", source)

    def test_product_links_pass_matching_start_parameter(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        for product in ("premium", "boost", "stars"):
            self.assertIn(
                f"https://t.me/StarvexEmpire24Bot?start={product}", source
            )


if __name__ == "__main__":
    unittest.main()
