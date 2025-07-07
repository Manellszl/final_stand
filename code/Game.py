import pygame
from code.Menu import Menu
from code.PlayScene import PlayScene
from code.GameOverScene import GameOverScene
from code.ScoreScene import ScoreScene
from code.const import WIN_WIDTH, WIN_HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.is_running = True

        self.music_tracks = {
            'MENU': './assets/music/Menu.mp3',
            'PLAYING': './assets/music/gameplaymusic.mp3',
            'GAME_OVER': './assets/music/gameover.mp3'
        }
        self.current_playing_music = None

        self.scenes = {
            'MENU': Menu(self.window),
            'PLAYING': PlayScene(self.window),
            'GAME_OVER': GameOverScene(self.window),
            'SCORE': ScoreScene(self.window)
        }
        self.active_scene_name = 'MENU'

        self.play_music_for_scene(self.active_scene_name)

    def run(self):
        clock = pygame.time.Clock()

        while self.is_running:
            active_scene = self.scenes[self.active_scene_name]

            events = pygame.event.get()
            command_from_events = active_scene.handle_events(events)
            command_from_update = active_scene.update()

            command = command_from_events or command_from_update

            if command == 'QUIT':
                self.is_running = False
            elif command == 'GAME_OVER':
                stats = {
                    "level": active_scene.player.level,
                    "waves": active_scene.wave_number,
                    "kills": active_scene.enemies_killed
                }
                self.scenes['GAME_OVER'].set_stats(**stats)
                self.active_scene_name = 'GAME_OVER'
                self.play_music_for_scene('GAME_OVER')
            elif command is not None:
                if command == 'PLAYING':
                    self.scenes['PLAYING'] = PlayScene(self.window)

                if self.active_scene_name == 'GAME_OVER' and command == 'MENU':
                    self.scenes['MENU'] = Menu(self.window)

                self.active_scene_name = command
                self.play_music_for_scene(self.active_scene_name)

            active_scene.draw(self.window)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        quit()

    def play_music_for_scene(self, scene_name: str):
        track_path = self.music_tracks.get(scene_name)

        if track_path and track_path != self.current_playing_music:
            pygame.mixer_music.fadeout(500)
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play(-1, fade_ms=500)
            self.current_playing_music = track_path