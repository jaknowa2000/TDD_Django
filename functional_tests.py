from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from time import sleep


class NewVisitorTest(unittest.TestCase):
    # metoda przed każdym testem (tu wybierzemy przegladarke)
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    # metoda po każdym teście  (zamkniecie przegladarki, metoda!)
    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(by='id', value='id_list_table')
        rows = table.find_elements(by='tag name', value='tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # przejście na stronę główą aplikacji
        self.browser.get('http://localhost:8000')

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
        sleep(3)
        self.check_for_row_in_list_table('1: Kupić pawie pióra')

        # nadal mamy mozliwość wpisania zadania, wpisanie kolejnego zadania
        inputbox = self.browser.find_element(by='id', value='id_new_item')
        inputbox.send_keys("Użyć piór do przynęty")
        inputbox.send_keys(Keys.ENTER)
        sleep(3)

        # wystepuja dwie pozycje na liscie
        self.check_for_row_in_list_table('1: Kupić pawie pióra')
        self.check_for_row_in_list_table('2: Użyć piór do przynęty')
        # wygenerowany unikalny adres url

        # sprawdzenie tego urla

        # koniec
        self.fail("Zakonczenie testu")


if __name__ == '__main__':
    unittest.main()
