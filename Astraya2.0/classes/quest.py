"""
En gros t'as les quetes et les objectives
"""


class Quest():
    def __init__(self, title, content, type, objectives, is_done):
        self.title = title
        self.content = content
        self.type = type
        self.is_done = is_done 

    def update(self):
        pass

    def change_done(self):
        self.type = True


class Objective:
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
    def __init__(self, description, npc_id):
        super().__init__(description)
        self.npc_id = npc_id
        self.talked = False

    def is_complete(self):
        return self.talked

    def on_talk(self, npc_id):
        if npc_id == self.npc_id:
            self.talked = True


class QuestManager:
    def __init__(self):
        self.available = []   # quetes disponibles mais pas encore prises
        self.active = []      # quetes en cours
        self.completed = []   # quetes terminées

    def add_quest(self, quest):
        self.available.append(quest)

    def accept_quest(self, quest):
        if quest in self.available:
            self.available.remove(quest)
            quest.activate()
            self.active.append(quest)

    def update(self):
        """Appelé à chaque frame."""
        newly_done = [q for q in self.active if q.update() or q.is_done]
        for quest in newly_done:
            self.active.remove(quest)
            self.completed.append(quest)
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

    def on_talk(self, npc_id):
        for quest in self.active:
            for obj in quest.objectives:
                if isinstance(obj, TalkObjective):
                    obj.on_talk(npc_id)

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

quetes_principales = [

]