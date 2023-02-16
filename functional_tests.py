from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    # metoda przed każdym testem (tu wybierzemy przegladarke)
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    #metoda po każdym teście  (zamkniecie przegladarki, metoda!)
    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # przejście na stronę główą aplikacji
        self.browser.get('http://localhost:8000')
        self.assertIn("Listy", self.browser.title)
        self.fail("Zakonczenie testu")

        # sprawdzenie poprawności tytułu strony

        # wpisanie pierwszego hobby

        # wciśnięcie klawisza enter, wyświetla pierwsze hobby

        # nadal mamy mozliwość wpisania zadania, wpisanie kolejnego zadania

        # wystepuja dwie pozycje na liscie

        # wygenerowany unikalny adres url

        # sprawdzenie tego urla

        # koniec


if __name__ == '__main__':
    unittest.main()
