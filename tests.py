import pytest
from main import BooksCollector

horror_book = 'КлаТбище домашних жЫвотных'
horror_book_2 = 'Падение дома Ашеров'
kids_book = 'Мама для мамонтенка'


class TestBooksCollector:
    # 1. Тест на добавление двух валидных книг
    def test_add_new_book_add_two_books(self, col):

        col.add_new_book('Гордость и предубеждение и зомби')
        col.add_new_book('Что делать, если ваш кот хочет вас убить')

        assert len(col.get_books_genre(
        )) == 2, "Должны добавиться обе валидные книги"  # Исправленный тест

    # 2. new Тест, что валидные названия добавляются
    @pytest.mark.parametrize("valid_book_name, msg", [
        ('А', "Один символ"),
        ('Кот в сапогах', "13 символов"),
        ('Г. Поттер и философский камень Д Роулинг', "40 символов")
    ])
    def test_add_book_add_valid_name_book(self, valid_book_name, msg, col):

        col.add_new_book(valid_book_name)

        assert valid_book_name in col.books_genre, msg

    # 3. new Тест, что невалидные названия книг не добавляются
    @pytest.mark.parametrize("invalid_book_name, msg", [
        ('', "Пустое название(0 символов)"),
        ('Г. Поттер и философский камень Д. Роулинг', "41 символов"),
        ('Удивительное путешествие Нильса Хольгерссона с дикими гусями по Швеции', "70 символов")
    ])
    def test_add_book_add_invalid_name_book(self, invalid_book_name, msg, col):

        col.add_new_book(invalid_book_name)

        assert invalid_book_name not in col.books_genre, msg

    # 4. Тест, что нельзя добавить уже существующую книгу (нельзя создать дубль)
    def test_add_new_book_duplicate_not_added(self, col):

        col.add_new_book('Война и мир')
        col.add_new_book('Война и мир')

        assert len(col.get_books_genre()
                   ) == 1,  "Не должно быть дублирования книг"

    # 5. Тест для установки жанра из списка genre для существующей книги
    @pytest.mark.parametrize("genre", ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'])
    def test_set_book_genre_add_genre(self, genre, col):
        col = BooksCollector()

        book_name = 'Тестовая книга'
        col.add_new_book(book_name)
        col.set_book_genre(book_name, genre)

        assert col.get_book_genre(
            book_name) == genre, "Жанр должен установиться для существующей книги в books_genre"

    # 6. Тест на смену жанра у существующей книги
    def test_set_book_genre_change_existing_genre(self, col):

        col.add_new_book(horror_book)
        col.set_book_genre(horror_book, 'Ужасы')
        col.set_book_genre(horror_book, 'Фантастика')

        assert col.get_book_genre(horror_book) == 'Фантастика'

    # 7. Тест для установки несуществующего жанра для существующей книги
    def test_set_book_genre_invalid_genre_unchanged(self, col):

        book_name = 'Поиск Анны'
        col.add_new_book(book_name)
        col.set_book_genre(book_name, 'Триллер')

        assert col.get_book_genre(
            book_name) == '', "Триллер не должен установиться"

    # 8. Тест для установки существующего жанра для несуществующей книги
    def test_set_book_genre_nonexistent_book_unchanged(self, col):

        book_name = 'Несуществующая книга'
        col.set_book_genre(book_name, 'Детективы')

        assert col.get_book_genre(
            book_name) is None, "Жанр не должен устанавливаться для несуществующей книги в books_genre"

    # 9. Тест для получения жанра по названию существующей книги с жанром
    def test_get_book_genre_get_an_existing_book(self, col):

        book_name = 'Следствие ведут колобки'
        col.add_new_book(book_name)
        col.set_book_genre(book_name, 'Мультфильмы')

        assert col.get_book_genre(book_name) == 'Мультфильмы'

    # 10. Тест на получение жанра у существующей книги, у которой не установлен жанр
    def test_get_book_genre_no_genre_returns_none(self, col):

        col.add_new_book(horror_book)

        assert col.get_book_genre(
            horror_book) == '', "Новая книга без жанра → None"

    # 11. Тест на поиск жанра у несуществующей книги
    def test_get_book_genre_nonexistent_book_returns_none(self, col):

        assert col.get_book_genre('Несуществующая') is None

    # 12. Тест для получения списка книг с определённым жанром из списка genre
    def test_get_books_with_specific_genre_get_valid_genre(self, col):

        col.add_new_book(horror_book)
        col.set_book_genre(horror_book, 'Ужасы')
        col.add_new_book(horror_book_2)
        col.set_book_genre(horror_book_2, 'Ужасы')
        col.add_new_book(kids_book)
        col.set_book_genre(kids_book, 'Мультфильмы')
        horror_books = col.get_books_with_specific_genre('Ужасы')

        assert len(horror_books) == 2, "Должно быть 2 книги жанра Ужасы"
        assert set(horror_books) == {
            horror_book_2, horror_book}, "Только ужасы, без 'Мама для мамонтенка' (Мультфильмы не устанавливается)"

    # 13. Тест на поиск по несуществующему жанру
    def test_get_books_with_specific_genre_unknown_returns_empty(self, col):

        col.add_new_book(horror_book)
        col.set_book_genre(horror_book, 'Ужасы')

        assert col.get_books_with_specific_genre('Фэнтези') == [
        ], "Неизвестный жанр 'Фэнтези' не входит в self.genre → должен вернуть пустой список []"

    # 14. Тест на вывод текущего словаря books_genre, у всех книг установлен жанр
    def test_get_books_genre_get_full_list(self, col):

        col.add_new_book(horror_book)
        col.set_book_genre(horror_book, 'Ужасы')
        col.add_new_book(horror_book_2)
        col.set_book_genre(horror_book_2, 'Ужасы')
        col.add_new_book(kids_book)
        col.set_book_genre(kids_book, 'Мультфильмы')

        assert len(col.get_books_genre()) == 3
        assert col.get_books_genre() == {
            horror_book_2: 'Ужасы', kids_book: 'Мультфильмы', horror_book: 'Ужасы'}

    # 15. Тест на вывод текущего словаря books_genre, у книги не установлен жанр
    def test_get_books_genre_get_full_list_without_genre(self, col):

        col.add_new_book(horror_book)

        assert len(col.get_books_genre()) == 1
        assert col.get_books_genre() == {horror_book: ''}

    # 16. Тест, что в детские книги не попадают книги для взрослых
    @pytest.mark.parametrize("adult_genre", ['Ужасы', 'Детективы'])
    def test_get_books_for_children_excludes_adult_genres(self, adult_genre, col):

        col.add_new_book('Взрослая книга')
        col.set_book_genre('Взрослая книга', adult_genre)
        col.add_new_book('Детская книга')
        col.set_book_genre('Детская книга', 'Мультфильмы')
        assert len(col.get_books_genre()) == 2
        assert col.get_books_for_children() == ['Детская книга']

    # 17. Тест, что когда список пустой, поиск по детским книгам не падает
    def test_get_books_for_children_empty_returns_empty(self, col):

        assert col.get_books_for_children() == []

    # 18. Тест, что существующая книга, добавляется в избранное, у книги установлен жанр
    def test_add_book_in_favorites_add_one_book(self, col):

        col.add_new_book(horror_book)
        col.add_book_in_favorites(horror_book)

        assert len(col.get_list_of_favorites_books()) == 1

    # 19. Тест, что существующая книга, добавляется в избранное, у книги не установлен жанр
    def test_add_book_in_favorites_add_book_without_genre(self, col):

        book_name = 'Ледяная принцесса'
        col.add_new_book(book_name)
        col.add_book_in_favorites(book_name)

        assert len(col.get_list_of_favorites_books()) == 1

    # 20. Тест, что несуществующая книга не добавляется в избранное
    def test_add_book_in_favorites_nonexistent_not_added(self, col):

        col.add_book_in_favorites(horror_book)

        assert len(col.get_list_of_favorites_books()) == 0

    # 21. Тест, что одна и та же книга повторно не добавляется в избранное
    def test_add_book_in_favorites_duplicate_not_added(self, col):

        col.add_new_book(horror_book)
        col.add_book_in_favorites(horror_book)
        col.add_book_in_favorites(horror_book)

        assert len(col.get_list_of_favorites_books()) == 1

    # 22. Тест, что книга удаляется из избранного
    def test_delete_book_from_favorites_success(self, col):

        col.add_new_book(horror_book)
        col.add_book_in_favorites(horror_book)
        col.add_new_book(kids_book)
        col.add_book_in_favorites(kids_book)
        col.delete_book_from_favorites(kids_book)

        assert col.get_list_of_favorites_books() == [horror_book]

    # 23. Тест, что несуществующая книга не удаляется из избранного
    def test_delete_book_from_favorites_nonexistent_ignored(self, col):

        col.add_new_book(horror_book)
        col.add_book_in_favorites(horror_book)
        col.delete_book_from_favorites('Несуществующая')

        assert len(col.get_list_of_favorites_books()) == 1

    # 24.Тест на получение списка избранных книг, в списке есть книги
    def test_get_list_of_favorites_get_books_success(self, col):

        col.add_new_book(horror_book)
        col.add_book_in_favorites(horror_book)
        col.add_new_book(kids_book)
        col.add_book_in_favorites(kids_book)
        favorites = col.get_list_of_favorites_books()

        assert len(col.get_list_of_favorites_books()
                   ) == 2, "Должно быть 2 избранные книги"
        assert set(col.get_list_of_favorites_books()) == {
            horror_book, kids_book}

    # 25. Тест на получение списка избранных книг, в списке нет книг
    def test_get_list_of_favorites_books_no_books_returns_empty_list(self, col):

        assert len(col.get_list_of_favorites_books()
                   ) == 0, "Должно быть 0 избранных книг"
        assert col.get_list_of_favorites_books() == []
