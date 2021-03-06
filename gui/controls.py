from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from gui.popups import ConfigAIPopup, ConfigTeacherPopup


class Controls(BoxLayout):
    def __init__(self, **kwargs):
        super(Controls, self).__init__(**kwargs)
        self.status = None
        self.status_node = None
        self.ai_settings_popup = None
        self.teacher_settings_popup = None

    def set_status(self, msg, at_node=None):
        self.status = msg
        self.status_node = at_node or self.katrain and self.katrain.game and self.katrain.game.current_node
        self.status_label.text = msg
        self.update_evaluation()

    def select_mode(self, mode):
        if mode == "analyze":
            self.analyze_tab_button.trigger_action(duration=0)
        else:
            self.play_tab_button.trigger_action(duration=0)

    def switch_mode(self):
        if self.play_tab_button.state == "down":
            self.select_mode("analyze")
        else:
            self.select_mode("play")

    def player_mode(self, player):
        return self.player_mode_groups[player].value

    def ai_mode(self, player):
        return self.ai_mode_groups[player].text

    def teaching_mode_enabled(self):
        return "undo" in self.player_mode("B") or "undo" in self.player_mode("W")

    def on_size(self, *args):
        self.update_evaluation()

    # handles showing completed analysis and score graph
    def update_evaluation(self):
        katrain = self.katrain
        current_node = katrain and katrain.game and katrain.game.current_node

        if current_node is not self.status_node and not (self.status is not None and self.status_node is None and current_node.is_root):  # startup errors on root
            self.status_label.text = ""
            self.status_node = None

        info = ""

        if current_node:
            move = current_node.move
            both_players_are_robots = "ai" in self.player_mode(current_node.player) and "ai" in self.player_mode(current_node.next_player)
            next_player_is_human_or_both_robots = current_node.player and ("ai" not in self.player_mode(current_node.player) or both_players_are_robots)
            current_player_is_ai_playing_human = current_node.player and "ai" in self.player_mode(current_node.player) and "ai" not in self.player_mode(current_node.next_player)
            if next_player_is_human_or_both_robots and not current_node.is_root and move:
                info += current_node.comment(teach="undo" in self.player_mode(current_node.player), hints=self.hints.active)
            elif current_player_is_ai_playing_human and current_node.parent:
                info += current_node.parent.comment(teach="undo" in self.player_mode(current_node.next_player), hints=self.hints.active)

            if current_node.analysis_ready:
                self.score.text = current_node.format_score()
                self.win_rate.text = current_node.format_win_rate()
                if move and next_player_is_human_or_both_robots:  # don't immediately hide this when an ai moves comes in
                    points_lost = current_node.points_lost
                    self.score_change.label = f"Points lost" if points_lost and points_lost > 0 else f"Points gained"
                    self.score_change.text = f"{move.player}: {abs(points_lost):.1f}" if points_lost else "..."
                elif not current_player_is_ai_playing_human:
                    self.score_change.label = f"Points lost"
                    self.score_change.text = ""
            elif current_player_is_ai_playing_human and current_node.parent and current_node.parent.move:
                points_lost = current_node.parent.points_lost
                self.score_change.label = f"Points lost" if points_lost and points_lost > 0 else f"Points gained"
                self.score_change.text = f"{current_node.parent.move.player}: {abs(points_lost):.1f}" if points_lost else "..."
            elif both_players_are_robots and current_node.parent and current_node.parent.analysis_ready:
                self.score.text = current_node.parent.format_score()
                self.win_rate.text = current_node.parent.format_win_rate()

            self.graph.update_value(current_node)

        self.info.text = info

    def configure_ais(self):
        if not self.ai_settings_popup:  # persist state of popup etc
            self.ai_settings_popup = Popup(title="Edit AI Settings", size_hint=(0.7, 0.8)).__self__
            self.ai_settings_popup.add_widget(ConfigAIPopup(self.katrain, self.ai_settings_popup, self.katrain.config("ai")))
        self.ai_settings_popup.open()

    def configure_teacher(self):
        if not self.teacher_settings_popup:
            self.teacher_settings_popup = Popup(title="Edit Teacher Settings", size_hint=(0.7, 0.8)).__self__
            self.teacher_settings_popup.add_widget(ConfigTeacherPopup(self.katrain, self.teacher_settings_popup))
        self.teacher_settings_popup.open()
