
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from app.models import GeneralUser, Film, Review
from app.test.endtoendtest import EndToEndTest
from playwright.sync_api import Page
from django.db import connections
from app.api.seed.seed import seed_db
import json

class TestInjection(EndToEndTest):

    def find_film(arr, name):
        for film in arr:
            if film["name"] == name:
                return film

    def setUp(self):
        super().setUp()
        self.seed_test_db_no_review()

    
    # Taken from: https://github.com/payloadbox/sql-injection-payload-list?tab=readme-ov-file
    def get_username_password_to_inject(self):
        return [
"""'-'""",
"""' '""",
"""'&'""",
"""'^'""",
"""'*'""",
"""' or ''-'""",
"""' or '' '""",
"""' or ''&'""",
"""' or ''^'""",
"""' or ''*'""",
'''"-"''',
'''" "''',
'''"&"''',
'''"^"''',
'''"*"''',
'''" or ""-"''',
'''" or "" "''',
'''" or ""&"''',
'''" or ""^"''',
'''" or ""*"''',
"""or true--""",
"""" or true--""",
"""' or true--""",
"""") or true--""",
"""') or true--""",
"""' or 'x'='x""",
"""') or ('x')=('x""",
"""')) or (('x'))=(('x""",
"""" or "x"="x""",
"""") or ("x")=("x""",
"""")) or (("x"))=(("x""",
"""or 1=1""",
"""or 1=1--""",
"""or 1=1#""",
"""or 1=1/*""",
"""admin' --""",
"""admin' #""",
"""admin'/*""",
"""admin' or '1'='1""",
"""admin' or '1'='1'--""",
"""admin' or '1'='1'#""",
"""admin' or '1'='1'/*""",
"""admin'or 1=1 or ''='""",
"""admin' or 1=1""",
"""admin' or 1=1--""",
"""admin' or 1=1#""",
"""admin' or 1=1/*""",
"""admin') or ('1'='1""",
"""admin') or ('1'='1'--""",
"""admin') or ('1'='1'#""",
"""admin') or ('1'='1'/*""",
"""admin') or '1'='1""",
"""admin') or '1'='1'--""",
"""admin') or '1'='1'#""",
"""admin') or '1'='1'/*""",
"""1234 ' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055""",
"""admin" --""",
"""admin" #""",
"""admin"/*""",
"""admin" or "1"="1""",
"""admin" or "1"="1"--""",
"""admin" or "1"="1"#""",
"""admin" or "1"="1"/*""",
'''admin"or 1=1 or ""="''',
"""admin" or 1=1""",
"""admin" or 1=1--""",
"""admin" or 1=1#""",
"""admin" or 1=1/*""",
"""admin") or ("1"="1""",
"""admin") or ("1"="1"--""",
"""admin") or ("1"="1"#""",
"""admin") or ("1"="1"/*""",
"""admin") or "1"="1""",
"""admin") or "1"="1"--""",
"""admin") or "1"="1"#""",
"""admin") or "1"="1"/*""",
"""1234 " AND 1=0 UNION ALL SELECT "admin", "81dc9bdb52d04dc20036dbd8313ed055""",
        ]

    def test_inject_login(self):
        page = self.browser.new_page()
        for p in self.get_username_password_to_inject():
            page.goto(f"{self.live_server_url}/signin")
            page.fill('[name=username]', p)
            page.fill('[name=password]', p)
            page.click('[value=Login]')
            self.assertEqual(page.url, f"{self.live_server_url}/signin", f"SQL injection should not be possible in login")
        page.close()


    def test_inject_review(self):
        page = self.browser.new_page()

        the_batman = Film.objects.get(title="The Batman")

        self.simulate_register(page, f"attacker", f"attacker@email.com", "Hacker", f"Handal")
        self.simulate_login(page, f"attacker")
        page.goto(f"{self.live_server_url}/details/{the_batman.id}")
        page.fill('[name=review]', '<script>document.body.innerHTML="";</script>')
        page.click(f'button:has(div:text("Post Review"))')
        self.simulate_logout(page)

        self.simulate_register(page)
        self.simulate_login(page)
        page.goto(f"{self.live_server_url}/details/{the_batman.id}")
        page.wait_for_timeout(500)
        title_text = page.locator("h1", has_text="The Batman")

        page.wait_for_timeout(3000)
        self.assertTrue(title_text.is_visible(), "<script> tag should not be able to be injected in review")

        page.close()