import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from visual_show.config import load_config
from visual_show.paths import runtime_root

class PortableConfigTests(unittest.TestCase):
    def load(self, value):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'config.json'
            path.write_text(json.dumps(value), encoding='utf-8')
            return load_config(path)

    def test_non_object_defaults(self):
        for value in [None, [], 'text', 42]:
            self.assertEqual(self.load(value).width, 960)

    def test_invalid_values_fall_back_individually(self):
        cfg = self.load({'width':'invalid','fps':None,'orbit_speed':float('nan'),'background':[float('inf'),0,0], 'seed':True, 'pulse_speed':4})
        self.assertEqual((cfg.width,cfg.fps,cfg.orbit_speed,cfg.seed),(960,60,1.4,17))
        self.assertEqual(cfg.background,(18,22,38))
        self.assertEqual(cfg.pulse_speed,4)

    def test_values_are_bounded(self):
        cfg=self.load({'width':10**100,'height':-1,'fps':500,'particle_count':100000})
        self.assertEqual((cfg.width,cfg.height,cfg.fps,cfg.particle_count),(3840,180,240,2000))

    def test_packaged_config_is_external_and_movable(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/'moved folder'
            target.mkdir()
            (target/'config.json').write_text('{"orbit_speed":2.75}',encoding='utf-8')
            with patch.object(sys,'frozen',True,create=True), patch.object(sys,'executable',str(target/'PortableVisualShow.exe')):
                self.assertEqual(runtime_root(),target)
                self.assertEqual(load_config(runtime_root()/'config.json').orbit_speed,2.75)

if __name__=='__main__': unittest.main()
