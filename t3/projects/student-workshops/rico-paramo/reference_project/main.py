import argparse
import json
import os
from visual_show.config import load_config
from visual_show.paths import resource_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Portable Python Visual Show")
    parser.add_argument("--verify", action="store_true", help="Render 10 headless frames and exit for reproducible QA")
    args = parser.parse_args()
    if args.verify:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        os.environ["SDL_AUDIODRIVER"] = "dummy"
    from visual_show.app import VisualApp
    config = load_config(resource_path("config.json"))
    app = VisualApp(config)
    if args.verify:
        import pygame
        try:
            for _ in range(10):
                app.scene.update(1 / config.fps)
                app.scene.draw(app.screen)
            print(json.dumps({"status":"PASS","frames":10,"width":config.width,"orbit_speed":config.orbit_speed}))
        finally:
            pygame.quit()
    else:
        app.run()


if __name__ == "__main__":
    main()
