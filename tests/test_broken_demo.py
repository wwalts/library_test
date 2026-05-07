 
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from catalog import Catalog

class TestBrokenOnPurpose:
     def test_broken_book_title(self):
         catalog = Catalog()
         book = catalog.add_book("Кобзар", "Шевченко", "Поезія", 1840)
         assert book.title == "Невірна назва"
 