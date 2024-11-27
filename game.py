import flet as ft
from interface import MainMenu, GameWindow
from game2 import Level2

class Game:
    def __init__(self, page: ft.Page):
        self.page = page
        self.main_menu = MainMenu(self.page, self.start_game)
        self.game_window = None
        self.level2 = None
        self.main_menu.show_menu_screen()
        self.buttons_added = False  # Флаг для проверки добавления кнопок

    def start_game(self, level):
        if level == 1:
            self.page.clean()
            self.game_window = GameWindow(
                self.page, self.handle_command, self.restart_game, self.return_to_menu
            )
            self.init_game()
        elif level == 2:
            self.start_level2()

    def init_game(self):
        self.has_key = False
        self.current_room = 'start'
        self.game_window.clear_text()
        self.display_status()
        self.game_window.append_text("Добро пожаловать в темную комнату. Куда вы пойдете? (налево/направо)")

    def display_status(self):
        status = "Инвентарь: "
        status += "Ключ" if self.has_key else "Пусто"
        self.game_window.set_status(status)
        self.page.update()

    def handle_command(self, e=None):
        command = self.game_window.get_command()
        self.game_window.clear_command()
        self.page.update()

        self.game_window.clear_text()
        self.display_status()

        if self.current_room == 'start':
            self.handle_start_room(command)
        elif self.current_room == 'room4':
            self.handle_room4(command)
        elif self.current_room == 'room5':
            self.handle_room5(command)
        else:
            self.game_window.append_text("Неверный выбор. Попробуйте еще раз.")

    def handle_start_room(self, command):
        if command == "налево":
            self.room_2()
        elif command == "направо":
            self.room_3()
        else:
            self.game_window.append_text("Вы в темной комнате. Куда вы пойдете? (налево/направо)")

    def room_2(self):
        self.has_key = True
        self.display_status()
        self.game_window.append_text("Вы нашли сундук с ключом и вернулись в первую комнату.")
        self.current_room = 'start'
        self.game_window.append_text("Куда вы пойдете? (налево/направо)")

    def room_3(self):
        if self.has_key:
            self.game_window.append_text("Вы использовали ключ, чтобы открыть дверь и вошли в новую комнату.")
            self.current_room = 'room4'
            self.game_window.append_text("Вы в комнате с тремя дверями. Куда пойдете? (налево/направо/по центру)")
        else:
            self.game_window.append_text("Дверь заперта. Нужен ключ!")
            self.current_room = 'start'
            self.game_window.append_text("Куда вы пойдете? (налево/направо)")

    def handle_room4(self, command):
        if command == "налево":
            self.game_over("💀 В этой комнате дракон! Вы проиграли.")
        elif command == "направо":
            self.current_room = 'room5'
            self.game_window.append_text("Вы в комнате с двумя дверями. Куда пойдете? (налево/направо)")
        elif command == "по центру":
            self.game_window.append_text("🎉 Ты нашел пасхалку! 🎉")
            self.current_room = 'room4'
            self.game_window.append_text("Вы в комнате с тремя дверями. Куда пойдете? (налево/направо/по центру)")

    def handle_room5(self, command):
        if command == "налево":
            self.game_over("💀 В этой комнате вас съел зомби! Вы проиграли.")
        elif command == "направо":
            self.win_game()
        else:
            self.game_window.append_text("Вы в комнате с двумя дверями. Куда пойдете? (налево/направо)")

    def win_game(self):
        self.game_window.append_text("🎉 Поздравляем! Вы выбрались из замка и выиграли игру! 🎉")
        self.current_room = 'start'
        self.game_window.disable_input()

        if not self.buttons_added:
            self.page.clean()  # Очистим страницу перед добавлением новых кнопок
            self.page.add(self.game_window.story)  # Добавим снова элемент story для отображения текста
            self.page.add(ft.ElevatedButton(text="Перейти на Уровень 2", on_click=self.start_level2))
            self.page.add(ft.ElevatedButton(text="Начать сначала", on_click=self.restart_game))
            self.page.add(ft.ElevatedButton(text="В меню", on_click=self.return_to_menu))
            self.buttons_added = True

        self.page.update()

    def game_over(self, message):
        self.game_window.append_text(f"{message}")
        self.game_window.disable_input()

    def restart_game(self, e=None):
        self.buttons_added = False  # Сброс флага при перезапуске игры
        self.game_window.enable_input()
        self.init_game()

    def return_to_menu(self, e=None):
        self.buttons_added = False  # Сброс флага при возврате в меню
        self.page.clean()
        self.main_menu.show_menu_screen()

    def start_level2(self, e=None):
        self.page.clean()
        self.level2 = Level2(self.page, self.start_game)
        self.level2.next_step()  # Начнем с первого шага

if __name__ == "__main__":
    ft.app(target=Game)
