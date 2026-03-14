import pytest
from main import BooksCollector


@pytest.fixture
def horror_book():
    return 'КлаТбище домашних жЫвотных'


@pytest.fixture
def horror_book_2():
    return 'Падение дома Ашеров'


@pytest.fixture
def kids_book():
    return 'Мама для мамонтенка'


class TestBooksCollector:
    # 1. Тест на добавление двух валидных книг
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        assert len(collector.get_books_genre(
        )) == 2, "Должны добавиться обе валидные книги"  # Исправленный тест

    # 2. Тест, что книга с названием более 40 символов не добавляется в books_genre
    def test_add_new_book_long_name_not_added(self):
        col = BooksCollector()

        long_name = 'Удивительное путешествие Нильса Хольгерссона с дикими гусями по Швеции'
        col.add_new_book(long_name)

        assert long_name not in col.get_books_genre(
        ), "Книга с названием длиннее 40 символов не должна быть добавлена"

    # 3. Тест, что книга с пустым названием не добавляется в books_genre
    def test_add_new_book_empty_name_not_added(self):
        col_0 = BooksCollector()

        empty_name = ''
        col_0.add_new_book(empty_name)

        assert empty_name not in col_0.get_books_genre(
        ), "Книга с пустым названием (0 символов) не должна быть добавлена"

    # 4. Тест, что нельзя добавить уже существующую книгу (нельзя создать дубль)
    def test_add_new_book_duplicate_not_added(self):
        col_1 = BooksCollector()

        col_1.add_new_book('Война и мир')
        col_1.add_new_book('Война и мир')

        assert len(col_1.get_books_genre()
                   ) == 1,  "Не должно быть дублирования книг"

    # 5. Тест для установки жанра из списка genre для существующей книги
    @pytest.mark.parametrize("genre", ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'])
    def test_set_book_genre_add_genre(self, genre):
        col_2 = BooksCollector()

        book_name = 'Тестовая книга'
        col_2.add_new_book(book_name)
        col_2.set_book_genre(book_name, genre)

        assert col_2.get_book_genre(
            book_name) == genre, "Жанр должен установиться для существующей книги в books_genre"

    # 6. Тест на смену жанра у существующей книги
    def test_set_book_genre_change_existing_genre(self, horror_book):
        col_3 = BooksCollector()

        col_3.add_new_book(horror_book)
        col_3.set_book_genre(horror_book, 'Ужасы')

        assert col_3.get_book_genre(horror_book) == 'Ужасы'

        col_3.set_book_genre(horror_book, 'Фантастика')

        assert col_3.get_book_genre(horror_book) == 'Фантастика'

    # 7. Тест для установки несуществующего жанра для существующей книги
    def test_set_book_genre_invalid_genre_unchanged(self):
        col_4 = BooksCollector()

        book_name = 'Поиск Анны'
        col_4.add_new_book(book_name)
        col_4.set_book_genre(book_name, 'Триллер')

        assert col_4.get_book_genre(
            book_name) == '', "Триллер не должен установиться"

    # 8. Тест для установки существующего жанра для несуществующей книги
    def test_set_book_genre_nonexistent_book_unchanged(self):
        col_5 = BooksCollector()

        book_name = 'Несуществующая книга'
        col_5.set_book_genre(book_name, 'Детективы')

        assert col_5.get_book_genre(
            book_name) is None, "Жанр не должен устанавливаться для несуществующей книги в books_genre"

    # 9. Тест для получения жанра по названию существующей книги с жанром
    def test_get_book_genre_get_an_existing_book(self):
        col_6 = BooksCollector()

        book_name = 'Следствие ведут колобки'
        col_6.add_new_book(book_name)
        col_6.set_book_genre(book_name, 'Мультфильмы')

        assert col_6.get_book_genre(book_name) == 'Мультфильмы'

    # 10. Тест на получение жанра у существующей книги, у которой не установлен жанр
    def test_get_book_genre_no_genre_returns_none(self, horror_book):
        col_7 = BooksCollector()

        col_7.add_new_book(horror_book)

        assert col_7.get_book_genre(
            horror_book) == '', "Новая книга без жанра → None"

    # 11. Тест на поиск жанра у несуществующей книги
    def test_get_book_genre_nonexistent_book_returns_none(self):
        col_8 = BooksCollector()

        assert col_8.get_book_genre('Несуществующая') is None

    # 12. Тест для получения списка книг с определённым жанром из списка genre
    def test_get_books_with_specific_genre_get_valid_genre(self, horror_book, horror_book_2, kids_book):
        col_9 = BooksCollector()

        col_9.add_new_book(horror_book)
        col_9.set_book_genre(horror_book, 'Ужасы')
        col_9.add_new_book(horror_book_2)
        col_9.set_book_genre(horror_book_2, 'Ужасы')
        col_9.add_new_book(kids_book)
        col_9.set_book_genre(kids_book, 'Мультфильмы')
        horror_books = col_9.get_books_with_specific_genre('Ужасы')

        assert len(horror_books) == 2, "Должно быть 2 книги жанра Ужасы"
        assert set(horror_books) == {
            horror_book_2, horror_book}, "Только ужасы, без 'Мама для мамонтенка' (Мультфильмы не устанавливается)"

    # 13. Тест на поиск по несуществующему жанру
    def test_get_books_with_specific_genre_unknown_returns_empty(self, horror_book):
        col_10 = BooksCollector()
        col_10.add_new_book(horror_book)
        col_10.set_book_genre(horror_book, 'Ужасы')

        assert col_10.get_books_with_specific_genre('Фэнтези') == [
        ], "Неизвестный жанр 'Фэнтези' не входит в self.genre → должен вернуть пустой список []"

    # 14. Тест на вывод текущего словаря books_genre, у всех книг установлен жанр
    def test_get_books_genre_get_full_list(self, horror_book, horror_book_2, kids_book):
        col_11 = BooksCollector()

        col_11.add_new_book(horror_book)
        col_11.set_book_genre(horror_book, 'Ужасы')
        col_11.add_new_book(horror_book_2)
        col_11.set_book_genre(horror_book_2, 'Ужасы')
        col_11.add_new_book(kids_book)
        col_11.set_book_genre(kids_book, 'Мультфильмы')

        assert len(col_11.get_books_genre()) == 3
        assert col_11.get_books_genre() == {
            horror_book_2: 'Ужасы', kids_book: 'Мультфильмы', horror_book: 'Ужасы'}

    # 15. Тест на вывод текущего словаря books_genre, у книги не установлен жанр
    def test_get_books_genre_get_full_list_without_genre(self, horror_book):
        col_12 = BooksCollector()

        col_12.add_new_book(horror_book)

        assert len(col_12.get_books_genre()) == 1
        assert col_12.get_books_genre() == {horror_book: ''}

    # 16. Тест, что в детские книги не попадают книги для взрослых
    @pytest.mark.parametrize("adult_genre", ['Ужасы', 'Детективы'])
    def test_get_books_for_children_excludes_adult_genres(self, adult_genre):
        col_13 = BooksCollector()

        col_13.add_new_book('Взрослая книга')
        col_13.set_book_genre('Взрослая книга', adult_genre)
        col_13.add_new_book('Детская книга')
        col_13.set_book_genre('Детская книга', 'Мультфильмы')
        assert len(col_13.get_books_for_children()) == 1

    # 17. Тест, что когда список пустой, поиск по детским книгам не падает
    def test_get_books_for_children_empty_returns_empty(self):
        col_14 = BooksCollector()
        assert col_14.get_books_for_children() == []

    # 18. Тест, что существующая книга, добавляется в избранное, у книги установлен жанр
    def test_add_book_in_favorites_add_one_book(self, horror_book):
        col_15 = BooksCollector()

        col_15.add_new_book(horror_book)
        col_15.add_book_in_favorites(horror_book)

        assert len(col_15.get_list_of_favorites_books()) == 1

    # 19. Тест, что существующая книга, добавляется в избранное, у книги не установлен жанр
    @pytest.mark.parametrize("book_name", [
        'Ледяная принцесса',
        'Война и мир',
        'Тьма в бутылке'
    ])
    def test_add_book_in_favorites_add_book_without_genre(self, book_name):
        col_16 = BooksCollector()

        col_16.add_new_book(book_name)
        col_16.add_book_in_favorites(book_name)

        assert len(col_16.get_list_of_favorites_books()) == 1

    # 20. Тест, что несуществующая книга не добавляется в избранное
    def test_add_book_in_favorites_nonexistent_not_added(self, horror_book):
        col_17 = BooksCollector()

        col_17.add_book_in_favorites(horror_book)

        assert len(col_17.get_list_of_favorites_books()) == 0

    # 21. Тест, что одна и та же книга повторно не добавляется в избранное
    def test_add_book_in_favorites_duplicate_not_added(self, horror_book):
        col_18 = BooksCollector()
        col_18.add_new_book(horror_book)
        col_18.add_book_in_favorites(horror_book)
        col_18.add_book_in_favorites(horror_book)

        assert len(col_18.get_list_of_favorites_books()) == 1

    # 22. Тест, что книга удаляется из избранного
    def test_delete_book_from_favorites_success(self, horror_book, kids_book):
        col_19 = BooksCollector()

        col_19.add_new_book(horror_book)
        col_19.add_book_in_favorites(horror_book)
        col_19.add_new_book(kids_book)
        col_19.add_book_in_favorites(kids_book)
        col_19.delete_book_from_favorites(kids_book)

        assert col_19.get_list_of_favorites_books() == [horror_book]

    # 23. Тест, что несуществующая книга не удаляется из избранного
    def test_delete_book_from_favorites_nonexistent_ignored(self, horror_book):
        col_20 = BooksCollector()
        col_20.add_new_book(horror_book)
        col_20.add_book_in_favorites(horror_book)
        col_20.delete_book_from_favorites('Несуществующая')

        assert len(col_20.get_list_of_favorites_books()) == 1

    # 24.Тест на получение списка избранных книг, в списке есть книги
    def test_get_list_of_favorites_get_books_success(self, horror_book, kids_book):
        col_21 = BooksCollector()

        col_21.add_new_book(horror_book)
        col_21.add_book_in_favorites(horror_book)
        col_21.add_new_book(kids_book)
        col_21.add_book_in_favorites(kids_book)
        favorites = col_21.get_list_of_favorites_books()

        assert len(col_21.get_list_of_favorites_books()
                   ) == 2, "Должно быть 2 избранные книги"
        assert set(col_21.get_list_of_favorites_books()) == {
            horror_book, kids_book}

    # 25. Тест на получение списка избранных книг, в списке нет книг
    def test_get_list_of_favorites_books_no_books_returns_empty_list(self):
        col_22 = BooksCollector()

        assert len(col_22.get_list_of_favorites_books()
                   ) == 0, "Должно быть 0 избранных книг"
        assert col_22.get_list_of_favorites_books() == []
