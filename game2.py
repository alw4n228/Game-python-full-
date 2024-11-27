import flet as ft
from interface import MainMenu

class Level2:
    def __init__(self, page: ft.Page, start_game_callback):
        self.page = page
        self.start_game_callback = start_game_callback
        self.current_step = 0
        self.correct_answers = [2, 1, 0]  # Индексы правильных ответов: 2 - Копье, 1 - Кошка, 0 - Шляпа с пером
        self.user_errors = 0  # Число ошибок игрока
        self.max_errors = 3  # Максимально допустимое число ошибок

        self.story_texts = [
            "Далее",
            '''Давным-давно, когда я был молод и силён, я путешествовал по далёким землям. В одном из своих путешествий я встретил старинного оружейного мастера, который подарил мне великолепное копьё. Это копьё спасало меня в многочисленных схватках с дикими зверями и разбойниками.
            Однажды, когда я шёл через густой лес, я нашёл себе верного спутника. Это была красивая и умная кошка. Она всегда предупреждала меня об опасности и помогала находить дорогу в самых труднопроходимых местах.''',
            "Во время одного из наших приключений, я нашёл старую, но удивительно хорошо сохранившуюся шляпу с пером. Она принадлежала великому воину, и мне казалось, что она приносит удачу в самых сложных ситуациях. Эта шляпа стала моим верным спутником в дальнейших путешествиях."
        ]

        self.questions = [
            {"text": "Какое у старика было оружие?", "options": ["Меч", "Лук", "Копье"]},
            {"text": "Какое у старика было животное?", "options": ["Собака", "Кошка", "Птица"]},
            {"text": "Какая у старика была шляпа?", "options": ["Шляпа с пером", "Цилиндр", "Панамка"]}
        ]

        self.story_label = ft.Text()
        self.page.add(self.story_label)
        self.next_button = ft.ElevatedButton(text="Далее", on_click=self.next_step)
        self.page.add(self.next_button)
        self.next_step()  # Начнем с первого шага

    def next_step(self, e=None):
        self.page.clean()  # Очистим страницу перед каждым шагом
        self.page.add(self.story_label)  # Добавляем снова текстовое поле
        if self.current_step < 3:
            self.show_story()
            self.page.add(self.next_button)  # Отображаем кнопку "Далее" только для шагов с рассказом
        elif self.current_step < 6:
            self.show_question()
        self.page.update()

    def show_story(self):
        if self.current_step < len(self.story_texts):
            self.story_label.value = self.story_texts[self.current_step]
            self.current_step += 1
        self.page.update()

    def show_question(self):
        question_index = self.current_step - 3
        question = self.questions[question_index]
        self.story_label.value = question["text"]

        self.answer_buttons = []  # Сохраним кнопки для дальнейшей деактивации
        for i, option in enumerate(question["options"]):
            button = ft.ElevatedButton(text=option, on_click=lambda e, i=i: self.check_answer(i))
            self.answer_buttons.append(button)
            self.page.add(button)

        self.page.update()

    def check_answer(self, selected_index):
        question_index = self.current_step - 3
        correct_answer = self.correct_answers[question_index]

        if selected_index == correct_answer:
            self.current_step += 1
            if self.current_step < 6:
                self.next_step()
            else:
                self.show_final_screen()
        else:
            self.user_errors += 1
            if self.user_errors >= self.max_errors:
                self.story_label.value = "Старик говорит: 'Вы плохо меня слушали. Игру придется начинать сначала.'"
                self.disable_answer_buttons()
                self.show_end_options()
            else:
                self.story_label.value = "Неправильно! Попробуйте еще раз."

        self.page.update()

    def disable_answer_buttons(self):
        for button in self.answer_buttons:
            button.disabled = True
        self.page.update()

    def show_final_screen(self):
        self.page.clean()
        self.story_label.value = "На все ответы вы ответили верно!"
        self.page.add(self.story_label)
        self.page.add(ft.ElevatedButton(text="Сначала", on_click=self.restart_level))
        self.page.add(ft.ElevatedButton(text="В главное меню", on_click=self.return_to_menu))
        self.page.update()

    def show_end_options(self):
        self.page.add(ft.ElevatedButton(text="Начать сначала", on_click=self.restart_level))
        self.page.add(ft.ElevatedButton(text="В меню", on_click=self.return_to_menu))
        self.page.update()

    def restart_level(self, e=None):
        self.user_errors = 0
        self.current_step = 0
        self.page.clean()
        self.next_step()  # Начнем с первого шага

    def return_to_menu(self, e=None):
        self.page.clean()
        main_menu = MainMenu(self.page, self.start_game_callback)
        main_menu.show_menu_screen()

if __name__ == "__main__":
    ft.app(target=Level2)
