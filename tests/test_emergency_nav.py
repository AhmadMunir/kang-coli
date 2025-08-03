#!/usr/bin/env python3
"""
Test Emergency Protocol Menu
"""

print("🧪 Testing Emergency Protocol Menu...")

try:
    from src.bot.keyboards.inline_keyboards import BotKeyboards
    print("✅ BotKeyboards imported")
    
    # Test emergency protocol menu
    emergency_protocol_keyboard = BotKeyboards.emergency_protocol_menu()
    print("✅ Emergency protocol menu keyboard created")
    
    # Test emergency menu
    emergency_menu_keyboard = BotKeyboards.emergency_menu()
    print("✅ Emergency menu keyboard created")
    
    print("\n🎯 Navigation Flow:")
    print("1. Main Menu → 🆘 Mode Darurat")
    print("2. Emergency Menu → Select Protocol (e.g., 🌊 Urge Surfing)")  
    print("3. Protocol Page → [🆘 Kembali ke Emergency Mode] [🏠 Menu Utama]")
    print("4. User can go back to Emergency Mode or Main Menu")
    
    print("\n✅ Emergency navigation enhancement completed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
