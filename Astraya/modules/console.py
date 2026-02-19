from modules import variables as var
import pyxel
from modules import check_tiles as ct
from modules import inventory as inv
from modules import actions as actions
from modules import dialogs as dial


#fonction input déplacement
def input():
    vitesse = 5
    if not var.in_console:
        if pyxel.btnp(pyxel.KEY_Z, 10, vitesse) or pyxel.btnp(
                pyxel.KEY_UP, 10, vitesse):
            ct.try_move(var.x, var.y - 1)
            var.orientation = "back"

        if pyxel.btnp(pyxel.KEY_S, 10, vitesse) or pyxel.btnp(
                pyxel.KEY_DOWN, 10, vitesse):
            ct.try_move(var.x, var.y + 1)
            var.orientation = "face"

        if pyxel.btnp(pyxel.KEY_Q, 10, vitesse) or pyxel.btnp(
                pyxel.KEY_LEFT, 10, vitesse):
            ct.try_move(var.x - 1, var.y)
            var.orientation = "left"

        if pyxel.btnp(pyxel.KEY_D, 10, vitesse) or pyxel.btnp(
                pyxel.KEY_RIGHT, 10, vitesse):
            ct.try_move(var.x + 1, var.y)
            var.orientation = "right"

        if pyxel.btnp(pyxel.KEY_H, 10, vitesse):
            inv.add_item("Bois", 1)

        if pyxel.btnp(pyxel.KEY_J, 10, vitesse):
            inv.remove_item("Bois", 1)


#fonction d'affichage de la console
def print_console(nx, ny, widht, height):
    if var.timer_cursor > 0:
        var.timer_cursor -= 1

    var.consoleinfo = nx, ny, widht, height
    pyxel.rect(nx, ny, widht, height, 0)

    visible_max = (widht // 4) - 3
    visible_text = var.console_content[-visible_max:]

    # verif si la console est ouverte
    if var.in_console:
        pyxel.rect(nx + 1, ny + (height - 9), widht - 12, 8, 7)
        pyxel.rect(nx + widht - 11, ny + (height - 9), 8, 8, 13)
        pyxel.text(nx + widht - 8, ny + (height - 8), "X", 0)

        # afficher curseur
        if var.timer_cursor > 10:
            pyxel.rect(nx + 2 + var.pos_cursor, ny + (height - 8), 1, 6, 0)
        elif var.timer_cursor > 0:
            pyxel.rect(nx + 2 + var.pos_cursor, ny + (height - 8), 1, 6, 7)
        else:
            var.timer_cursor = 20

        # CTRL + C pour quitter
        if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_C):
            var.in_console = False
        else:
            for i in range(26):
                key = getattr(pyxel, f"KEY_{chr(ord('A') + i)}")
                if pyxel.btnp(key, 4, 2):
                    var.console_content += chr(ord("a") + i)

        if pyxel.btnp(pyxel.KEY_SPACE, 4, 2):
            var.console_content += " "

        if pyxel.btnp(pyxel.KEY_BACKSPACE, 4, 2):
            var.console_content = var.console_content[:-1]

        # entrée (shift ou bouton)
        if pyxel.btnp(pyxel.KEY_SHIFT) or pyxel.btnp(pyxel.KEY_KP_ENTER) or (
                pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and nx +
            (widht - 11) <= pyxel.mouse_x <= nx + (widht - 3) and ny +
            (height - 9) <= pyxel.mouse_y <= ny + (height - 1)):
            if var.console_content != "":
                execute_console(var.console_content)
                var.in_console = False
                var.console_content = ""

        pyxel.text(nx + 2, ny + (height - 8), visible_text, 0)
        var.pos_cursor = len(visible_text) * 4

    else:
        var.console_content = ""
        var.pos_cursor = 0
        pyxel.rect(nx, ny + (height - 10), widht, 10, 13)
        pyxel.text(nx + 2, ny + (height - 8), "Cliquez pour ecrire", 7)

        if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
                and nx <= pyxel.mouse_x <= nx + widht and ny +
            (height - 10) <= pyxel.mouse_y <= ny + height) or (pyxel.btn(
                pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_T)):
            var.in_console = True
            var.console_content = ""

    print_to_console()


#Fonction pour afficher du texte dans la console
def print_to_console(text=None, color=7):
    nx, ny, width, height = var.consoleinfo

    max_chars_per_line = width // 4
    max_visible_lines = (height - 10) // 8

    #chatgpt pour le if
    if text is not None:
        for i in range(0, len(text), max_chars_per_line):
            line = text[i:i + max_chars_per_line]
            var.console_lines.append((line, color))

        while len(var.console_lines) > max_visible_lines:
            var.console_lines.pop(0)

    for i, (line, color) in enumerate(var.console_lines):
        pyxel.text(nx + 4, ny + 4 + i * 8, line, color)


#fonction pour verifier les commandes
def execute_console(command):

    if var.in_name_input:
        var.player_name = command

    if var.current_dialog == 0:
        if command == "clear":
            var.console_lines = []
            var.console_content = ""

        elif command == "quit":
            var.in_console = False

        elif command == "end":
            var.end = True
            
        elif command == "death":
            var.coeur = 0

        elif command == "quitgame":
            pyxel.quit()

        elif command == "ping":
            print_to_console("pong", 10)

    else:
        #Input de nom au début
        if var.current_dialog == 2:
            var.player_name = command
            var.current_quest = 1  # après le pêcheur
            print_to_console("")
            print_to_console(f"Bienvenue {var.player_name}", 7)
            print_to_console("Suis les pommiers et tu arriveras au village", 7)
            print_to_console("La bas tu trouveras le chef du village", 7)
            print_to_console("Il pourra t'expliquer l'histoire de l'ile", 7)
            return

        # Dialogue Roger
        if var.current_dialog == 1:
            if var.current_quest == 2:
                if var.dialog_png_1_state == 0:
                    var.console_content = ""
                    var.console_lines = []
                    var.in_console = True
                    if command == "oui":
                        var.dialog_png_1_state = 1
                        print_to_console("Merci d'avance !", 7)
                        print_to_console("Voici une hache tu en auras besoin",
                                         7)
                        if inv.item_in_inventory("Hache") == 0:
                            inv.add_item("Hache", 1)
                    elif command == "non":
                        print_to_console(
                            "Dommage, reviens me voir si tu veux m'aider", 7)

                    else:
                        print_to_console("Je n'ai pas compris votre reponse.",
                                         7)

        #Dialogue Helena
        if var.current_dialog == 3:
            if var.current_quest == 3:
                var.console_content = ""
                var.console_lines = []
                if command in [
                        "ski", "le ski", "les ski", "un ski", "des ski",
                        "les skis", "un paire de ski", "la paire de ski",
                        "mes skis", "mes ski", "skis"
                ]:
                    var.console_lines = []
                    print_to_console(
                        "Bravo tu as trouve la reponse voici une recompense", 7)
                    print_to_console(
                        "Grace a ces skis tu vas pouvoir traverser les montagnes et parler a la statue du Heros",
                        7)
                    inv.add_item("Ski", 1)
                    var.game_map[14][32] = 1
                    var.game_map[16][30] = 1
                    var.current_quest = 4
                else:
                    print_to_console("Ce n'est pas la bonne reponse.", 7)

        # Dialogue Chef du village
        if var.current_dialog == 5 and var.current_quest == 1:
            if var.dialog_step == 0:
                if command == "oui":
                    var.console_content = ""
                    var.console_lines = []
                    print_to_console("Je te la raconte :", 7)
                    print_to_console(
                        "Il y a bien longtemps, cette ile etait habitee par un peuple avance les Eldarins.",
                        7)
                    print_to_console(
                        "Ils vivaient en harmonie et avaient une technologie avancee.",
                        7)
                    print_to_console("Mais un jour, un naufrage est arrive.")
                    print_to_console(
                        "Les habitants l'ont acceuilli et lui ont appris les secrets de leurs technologies."
                    )
                    print_to_console("Veux-tu savoir la suite ?", 7)
                    var.in_console = True
                    var.dialog_step = 1
                elif command == "non":
                    var.console_content = ""
                    var.console_lines = []
                    print_to_console(
                        "Dommage. Tu peux aller voir Roger, sa maison a ete detruite.",
                        7)
                    var.current_quest = 2
                    var.dialog_step = 99
                else:
                    var.console_content = ""
                    var.console_lines = []
                    print_to_console("Je n'ai pas compris votre reponse.", 7)
            elif var.dialog_step == 1:
                if command == "oui":
                    var.console_content = ""
                    var.console_lines = []
                    print_to_console(
                        "Cependant le naurage etait en realite assoiffe de pouvoir",
                        7)
                    print_to_console(
                        "Il a commence a utiliser la technologie a l'encontre des habitants.",
                        7)
                    print_to_console(
                        "Sachant que cette technologie etait trop avances pour etre entre de mauvaises mains",
                        7)
                    print_to_console(
                        "Les Eldarins ont decide de se sacrifier pour arreter le naufrage",
                        7)
                    print_to_console("Veux-tu savoir la suite ?", 7)
                    var.in_console = True
                    var.dialog_step = 2
                elif command == "non":
                    var.console_content = ""
                    var.console_lines = []
                    print_to_console("Dommage. Tu peux aller voir Roger.", 7)
                    var.current_quest = 2
                    var.dialog_step = 99
            elif var.dialog_step == 2:
                if command == "oui":
                    var.console_content = ""
                    var.console_lines = []
                    print_to_console("La technologie de l'ile a donc disparu",
                                     7)
                    print_to_console(
                        "Si tu veux gagner ta place ici tu dois aller au dela des montagnes",
                        7)
                    print_to_console(
                        "Parler au Heros en ruine et survivre a ses questions",
                        7)
                    print_to_console("")
                    print_to_console(
                        "Tu peux aller voir Roger, sa maison a ete detruite.",
                        7)
                    var.current_quest = 2
                    var.dialog_step = 99
                elif command == "non":
                    var.console_content = ""
                    var.console_lines = []
                    print_to_console("Dommage. Tu peux aller voir Roger.", 7)
                    var.current_quest = 2

        #dialogue statue
        if var.current_dialog == 100:
            if var.current_quest == 4 and var.hero_question_posed:
                if var.dialog_hero_state == 0:
                    if command in [
                            "Eldarins", "Eldarin", "eldarin", "eldarins"
                    ]:
                        print_to_console("Bravo tu as trouve la reponse", 7)
                        var.dialog_hero_state = 1
                        var.hero_question_posed = False
                        dial.dialogs(100)
                    else:
                        print_to_console("Ce n'est pas la bonne reponse.", 7)
                        print_to_console("Tu perds 4 coeur", 7)
                        var.coeur = var.coeur - 4
                        var.dialog_hero_state = 1
                        var.hero_question_posed = False
                        dial.dialogs(100)

                elif var.dialog_hero_state == 1:
                    if command == "fisher":
                        print_to_console("Bravo tu as trouve la reponse", 7)
                        var.dialog_hero_state = 2
                        var.hero_question_posed = False
                        dial.dialogs(100)
                    else:
                        print_to_console("Ce n'est pas la bonne reponse.", 7)
                        print_to_console("Tu perds 4 coeur", 7)
                        var.coeur = var.coeur - 4
                        var.dialog_hero_state = 2
                        var.hero_question_posed = False
                        dial.dialogs(100)

                elif var.dialog_hero_state == 2:
                    if command in ["Helena", "helena"]:
                        print_to_console("Bravo tu as trouve la reponse", 7)
                        var.dialog_hero_state = 3
                        var.hero_question_posed = False
                        dial.dialogs(100)
                    else:
                        print_to_console("Ce n'est pas la bonne reponse.", 7)
                        print_to_console("Tu perds 4 coeur", 7)

                        var.coeur = var.coeur - 4
                        var.dialog_hero_state = 3
                        var.hero_question_posed = False
                        dial.dialogs(100)

                elif var.dialog_hero_state == 3:
                    if command in ["quatre", "4", "Quatre"]:
                        print_to_console("Bravo tu as trouve la reponse", 7)
                        var.dialog_hero_state = 4
                        var.hero_question_posed = False
                        dial.dialogs(100)
                    else:
                        print_to_console("Ce n'est pas la bonne reponse.", 7)
                        print_to_console("Tu perds 4 coeur", 7)
                        var.coeur = var.coeur - 4
                        var.dialog_hero_state = 4
                        var.hero_question_posed = False
                        dial.dialogs(100)

                if var.dialog_hero_state == 4:
                    var.end = True
