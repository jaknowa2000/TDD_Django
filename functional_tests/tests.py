from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from time import sleep, time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    # metoda przed każdym testem (tu wybierzemy przegladarke)
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    # metoda po każdym teście  (zamkniecie przegladarki, metoda!)
    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time()
        while True:
            try:
                table = self.browser.find_element(by='id', value='id_list_table')
                rows = table.find_elements(by='tag name', value='tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as excpt:
                if time() - start_time > MAX_WAIT:
                    raise excpt
                sleep(0.5)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(by='id', value='id_list_table')
        rows = table.find_elements(by='tag name', value='tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # przejście na stronę główą aplikacji przez user1
        self.browser.get(self.live_server_url)

        # sprawdzenie poprawności tytułu strony
        self.assertIn("Listy", self.browser.title)
        header_text = self.browser.find_element(by="tag name", value="h1").text
        self.assertIn("Twoja lista", header_text)

        # wpisanie pierwszego hobby
        inputbox = self.browser.find_element(by="id", value='id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), "Wpisz rzeczy do zrobienia")
        inputbox.send_keys("Kupić pawie pióra")

        # wciśnięcie klawisza enter, wyświetla pierwsze hobby
        inputbox.send_keys(Keys.ENTER)
        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, '/lists/.+') # sprawdzenie czy pasuje do wyrażenia regilarnego
        self.wait_for_row_in_list_table('1: Kupić pawie pióra')

        # nadal mamy mozliwość wpisania zadania, wpisanie kolejnego zadania
        inputbox = self.browser.find_element(by='id', value='id_new_item')
        inputbox.send_keys("Użyć piór do przynęty")
        inputbox.send_keys(Keys.ENTER)

        # wystepuja dwie pozycje na liscie
        self.wait_for_row_in_list_table('1: Kupić pawie pióra')
        self.wait_for_row_in_list_table('2: Użyć piór do przynęty')

        # user2 rozpoczyna pracę
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # nie znajduje śladów user1
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(by='tag name', value='body').text
        self.assertNotIn('Kupić pawie pióra', page_text)
        self.assertNotIn('Użyć piór do przynęty', page_text)

        # utworzenie nowej listy
        inputbox = self.browser.find_element(by='id', value='id_new_item')
        inputbox.send_keys("Kupić mleko")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('Kupić mleko')

        # unikatowy adres url do listy
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user1_list_url, user2_list_url)

        # nadal nie ma śladu user1
        page_text = self.browser.find_element(by='tag name', value='body').text
        self.assertNotIn('Kupić pawie pióra', page_text)
        self.assertNotIn('Użyć piór do przynęty', page_text)
        self.assertIn('Kupić mleko', page_text)

        # koniec
        self.fail("Zakonczenie testu")

# bez __name__ == __main__ bo używamy silnika testów django
