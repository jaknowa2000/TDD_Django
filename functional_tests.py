from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
    # metoda przed każdym testem (tu wybierzemy przegladarke)
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    # metoda po każdym teście  (zamkniecie przegladarki, metoda!)
    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # przejście na stronę główą aplikacji
        self.browser.get('http://localhost:8000')
        # sprawdzenie poprawności tytułu strony
        self.assertIn("Listy", self.browser.title)
        header_text = self.browser.find_element(by="tag name", value="h1").text
        self.assertIn("Listy", header_text)
        # wpisanie pierwszego hobby
        inputbox = self.browser.find_element(by="id", value='id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), "Wpisz rzeczy do zrobienia")
        inputbox.send_keys("Kupić nowe pióra")
        # wciśnięcie klawisza enter, wyświetla pierwsze hobby
        inputbox.send_keys(Keys.ENTER)
        table = self.browser.find_element(by="id", value='id_list_table')
        rows = table.find_elements(by='tag name', value='tr')
        self.assertTrue(any(row.text == '1: Kupić pawie pióra' for row in rows))
        # nadal mamy mozliwość wpisania zadania, wpisanie kolejnego zadania

        # wystepuja dwie pozycje na liscie

        # wygenerowany unikalny adres url

        # sprawdzenie tego urla

        # koniec
        self.fail("Zakonczenie testu")


if __name__ == '__main__':
    unittest.main()
