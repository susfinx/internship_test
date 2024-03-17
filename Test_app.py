import unittest
from game_score_app import generate_stamp, generate_game, get_score


class TestGenerateStamp(unittest.TestCase):
    # Тест для проверки генерации штрафного времени
    def test_generate_stamp_offset(self):
        previous_value = {"offset": 0, "score": {"home": 0, "away": 0}}
        new_stamp = generate_stamp(previous_value)
        self.assertTrue(new_stamp["offset"] >= 1)

    # Тест для проверки генерации изменения счета
    def test_generate_stamp_score(self):
        previous_value = {"offset": 0, "score": {"home": 0, "away": 0}}
        for _ in range(100):  # Прогоняем несколько раз, чтобы убедиться, что изменения счета случайны
            new_stamp = generate_stamp(previous_value)
            self.assertTrue(new_stamp["score"]["home"] in [0, 1])
            self.assertTrue(new_stamp["score"]["away"] in [0, 1])


class TestGenerateGame(unittest.TestCase):
    # Тест для проверки длины списка состояний игры
    def test_generate_game_length(self):
        game_stamps = generate_game()
        self.assertEqual(len(game_stamps), 50001)  # Инициальная отметка + 50000 шагов

    # Тест для проверки формата списка состояний игры
    def test_generate_game_format(self):
        game_stamps = generate_game()
        self.assertIsInstance(game_stamps, list)
        for stamp in game_stamps:
            self.assertIsInstance(stamp, dict)
            self.assertIn("offset", stamp)
            self.assertIn("score", stamp)
            self.assertIsInstance(stamp["offset"], int)
            self.assertIsInstance(stamp["score"], dict)
            self.assertIn("home", stamp["score"])
            self.assertIn("away", stamp["score"])
            self.assertIsInstance(stamp["score"]["home"], int)
            self.assertIsInstance(stamp["score"]["away"], int)


class TestGetScore(unittest.TestCase):
    # Тест для случая, когда offset меньше первой метки времени
    def test_offset_before_first_stamp(self):
        game_stamps = generate_game()
        offset = -1
        home_score, away_score = get_score(game_stamps, offset)
        self.assertEqual(home_score, 0)
        self.assertEqual(away_score, 0)

    # Тест для случая, когда offset равен времени первой метки
    def test_offset_equal_to_first_stamp(self):
        game_stamps = generate_game()
        offset = game_stamps[0]["offset"]
        home_score, away_score = get_score(game_stamps, offset)
        self.assertEqual(home_score, 0)
        self.assertEqual(away_score, 0)

    # Тест для случая, когда offset равен времени последней метки
    def test_offset_equal_to_last_stamp(self):
        game_stamps = generate_game()
        offset = game_stamps[-1]["offset"]
        home_score, away_score = get_score(game_stamps, offset)
        self.assertGreaterEqual(home_score, 0)
        self.assertGreaterEqual(away_score, 0)

    # Тест для случая, когда offset больше времени последней метки
    def test_offset_after_last_stamp(self):
        game_stamps = generate_game()
        offset = game_stamps[-1]["offset"] + 1
        home_score, away_score = get_score(game_stamps, offset)
        self.assertGreaterEqual(home_score, 0)
        self.assertGreaterEqual(away_score, 0)

    # Тест для случая, когда offset между двумя метками времени
    def test_offset_between_stamps(self):
        game_stamps = generate_game()
        offset = (game_stamps[0]["offset"] + game_stamps[-1]["offset"]) // 2
        home_score, away_score = get_score(game_stamps, offset)
        self.assertGreaterEqual(home_score, 0)
        self.assertGreaterEqual(away_score, 0)


if __name__ == '__main__':
    unittest.main()
