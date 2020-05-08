import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 사용자는 서버 자산관리를 위해 관리 페이지로 이동한다.
        self.browser.get('http://localhost:8000')

        # 사용자는 페이지 타이틀과 헤더에서 '서버관리'를 확인한다.
        self.assertIn('서버관리', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('서버관리', header_text)

        # 사용자는 새로운 서버 자산을 등록하기 위해 서버명 입력박스를 찾는다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '서버명')

        # 사용자는 서버명 텍스트 박스에 서버명"SERVER01"을 입력하고
        # 엔터를 입력하면, 페이지의 서버 리스트가 업데이트 된다.
        # 1: SERVER01
        inputbox.send_keys('SERVER01')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: SERVER01' for row in rows))

        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
