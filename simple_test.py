import sys
import os

print("Testing imports...")

try:
    import telegram
    print(f"✅ telegram imported: {telegram.__version__}")
except Exception as e:
    print(f"❌ telegram error: {e}")

try:
    import config
    print("✅ config imported")
except Exception as e:
    print(f"❌ config error: {e}")

try:
    from src.bot.handlers.start_handler import start
    print("✅ start_handler imported")
except Exception as e:
    print(f"❌ start_handler error: {e}")

print("Test complete!")
