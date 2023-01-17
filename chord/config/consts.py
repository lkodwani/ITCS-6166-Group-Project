from config.config import build_settings

CHORD_SETTINGS = build_settings('config/settings.yaml', 'chord')
RING_SIZE = CHORD_SETTINGS['ring_size']
