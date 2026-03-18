import pygame
import settings

"""
En gros t'as les quetes et les objectives
"""
# Creer une quete

class Quest_Toast():
    def __init__(self, content, color="white", font_size=24,):
        self.content = content
        self.color = color
        self.print_interval = 25
        self.last_print_interval = pygame.time.get_ticks()
        self.letter_index = 0
        self.content_sliced = ""
        self.PADDING = 2
        self.font_size = font_size
        self.font = pygame.font.SysFont(None, self.font_size)
        
        
    def draw(self, x, y, screen):
        width = self.font.size(self.content_sliced)[0] + self.PADDING * 2
        height = self.font.size(self.content_sliced)[1] + self.PADDING * 2
        now = pygame.time.get_ticks()
        if self.letter_index <= len(self.content):
            if now - self.last_print_interval >= self.print_interval:
                self.last_print_interval = now
                self.content_sliced = self.content[:self.letter_index]
                self.letter_index += 1
        else: self.content_sliced = self.content
        toast = pygame.Surface((width, height))
        toast.fill("white")
        pygame.draw.rect(toast, self.color, (0, 0, width, height))
        content = self.font.render(self.content_sliced, True, "black")
        toast.blit(content, (self.PADDING, self.PADDING))
        screen.blit(toast, (x-width, y))
        


class Quest():
    def __init__(self, title, content, type, objectives):
        self.title = title
        self.content = content
        self.type = type
        self.toast = Quest_Toast(content, font_size=30)
        self.objectives = objectives
        self.done = False
            

    def update(self, screen):
        self.get_objectives()
        self.toast.draw(settings.WINDOW_WIDTH-100, 100, screen)
        if len(self.objectives) == 0:
            self.done = True

    def change_done(self):
        self.done = True
        
    def get_objectives(self):
        for objective in self.objectives:
            if objective.is_complete():
                self.objectives.remove(objective)


class Objective():
    def __init__(self, description):
        self.description = description

    def is_complete(self):
        raise NotImplementedError


class KillObjective(Objective):
    """Tuer X ennemis d'un certain type."""
    def __init__(self, description, enemy_type, required):
        super().__init__(description)
        self.enemy_type = enemy_type
        self.count = 0
        self.required = required

    def is_complete(self):
        return self.count >= self.required

    def on_kill(self, enemy_type):
        if enemy_type == self.enemy_type:
            self.count += 1


class CollectObjective(Objective):
    """Collecter X items."""
    def __init__(self, description, item_id, required):
        super().__init__(description)
        self.item_id = item_id
        self.required = required
        self.count = 0

    def is_complete(self):
        return self.count >= self.required

    def on_collect(self, item_id):
        if item_id == self.item_id:
            self.count += 1


class ReachObjective(Objective):
    """Atteindre un endroit."""
    def __init__(self, description, target_x, target_y, radius=50):
        super().__init__(description)
        self.target_x = target_x
        self.target_y = target_y
        self.radius = radius
        self.reached = False

    def is_complete(self):
        return self.reached

    def update_position(self, player_x, player_y):
        dist = ((player_x - self.target_x)**2 + (player_y - self.target_y)**2) ** 0.5
        if dist <= self.radius:
            self.reached = True


class TalkObjective(Objective):
    """Parler à un PNJ."""
    def __init__(self, description, npc):
        super().__init__(description)
        self.npc = npc
        self.talked = False

    def is_complete(self):
        return self.talked

    def on_talk(self, npc):
        if npc.has_talk_to_player:
            self.talked = True


class QuestManager:
    def __init__(self):
        self.available = []   # quetes disponibles mais pas encore prises
        self.active = []      # quetes en cours
        self.completed = []   # quetes terminées
        self.font = pygame.font.SysFont(None, 50)
        self.finished_text = "Quête Terminée !"
        self.text_surface = self.font.render(self.finished_text, False, "orange")
        self.font_stay_on_screen = 1000
        self.font_last_on_screen = pygame.time.get_ticks()

    def add_quest(self, quest):
        self.available.append(quest)

    def accept_quest(self, quest):
        if quest in self.available:
            self.available.remove(quest)
            self.active.append(quest)

    def complete_princ_quest(self, quest):
        if quest in self.active and quest.type == "principale":
            self.active.remove(quest)
            self.completed.append(quest)
            self.active.append(quest)
            self.font_last_on_screen = pygame.time.get_ticks()
            print(f" Quete termine : {quest.title}")

    def update(self, screen):
        now = pygame.time.get_ticks()
        if now - self.font_last_on_screen < self.font_stay_on_screen:
            screen.blit(self.text_surface, (settings.WINDOW_WIDTH//2-self.font.size(self.finished_text)[0]//2, (settings.WINDOW_HEIGTH//4)*3-self.font.size(self.finished_text)[1]//2))
            
        for quest in self.active:
            quest.update(screen)
            
        """Appelé à chaque frame."""
        newly_done = [q for q in self.active if q.done]
        for quest in newly_done:
            self.active.remove(quest)
            self.completed.append(quest)
            self.font_last_on_screen = now
            print(f" Quete termine : {quest.title}")

    # --- Événements globaux, à appeler depuis ton jeu ---

    def on_kill(self, enemy_type):
        for quest in self.active:
            for obj in quest.objectives:
                if isinstance(obj, KillObjective):
                    obj.on_kill(enemy_type)

    def on_collect(self, item_id):
        for quest in self.active:
            for obj in quest.objectives:
                if isinstance(obj, CollectObjective):
                    obj.on_collect(item_id)

    def on_talk(self, npc):
        for quest in self.active:
            for obj in quest.objectives:
                if isinstance(obj, TalkObjective):
                    obj.on_talk(npc)

    def on_player_move(self, player_x, player_y):
        for quest in self.active:
            for obj in quest.objectives:
                if isinstance(obj, ReachObjective):
                    obj.update_position(player_x, player_y)



#    quete_corruption = Quest(
#        title="Purifier la corruption",
#        content="La zone de corruption près de (1400, 1400) menace le village.",
#        type="principale",
#        objectives=[
#            ReachObjective("Atteindre le donjon", target_x=1400, target_y=1400, radius=50),
#        ],
#        rewards=[GoldReward(player, 500)]
#        )
#
#    quest_manager.add_quest(quete_corruption)
#    quest_manager.accept_quest(quete_corruption)

#hassoule ma poule blow blow blow



