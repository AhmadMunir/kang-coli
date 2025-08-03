# Application constants

# Bot information
BOT_NAME = "PMO Recovery Coach AI"
BOT_VERSION = "1.0.0"

# Commands
COMMANDS = {
    'start': 'Mulai menggunakan bot',
    'help': 'Tampilkan bantuan',
    'streak': 'Cek current streak',
    'motivation': 'Dapatkan motivasi harian',
    'emergency': 'Mode darurat',
    'checkin': 'Daily check-in',
    'relapse': 'Lapor relapse',
    'stats': 'Lihat statistik',
    'journal': 'Buka menu journaling',
    'tips': 'Coping strategies',
    'education': 'Materi edukasi'
}

# Streak milestones (in days)
MILESTONES = [1, 3, 7, 14, 21, 30, 45, 60, 90, 120, 180, 365]

# Default reminder time
DEFAULT_REMINDER_TIME = "08:00"

# Maximum text lengths
MAX_JOURNAL_LENGTH = 2000
MAX_NOTES_LENGTH = 500
MAX_USERNAME_LENGTH = 32

# Mood scale
MOOD_SCALE_MIN = 1
MOOD_SCALE_MAX = 10

# Emergency protocol types
EMERGENCY_PROTOCOLS = [
    'immediate_distraction',
    'mindfulness_intervention', 
    'accountability_check',
    'urge_surfing',
    'trigger_analysis'
]

# Coping tip categories
COPING_CATEGORIES = [
    'physical',
    'mental',
    'distraction', 
    'mindfulness',
    'productive'
]

# Education topics
EDUCATION_TOPICS = [
    'dopamine',
    'benefits',
    'neuroplasticity',
    'timeline'
]

# Success rate thresholds
SUCCESS_RATE_EXCELLENT = 80
SUCCESS_RATE_GOOD = 60
SUCCESS_RATE_FAIR = 40

# Recovery phases (in days)
RECOVERY_PHASES = {
    'withdrawal': (0, 14),
    'adjustment': (15, 30),
    'stabilization': (31, 90),
    'maintenance': (91, float('inf'))
}

# Daily reminder messages
REMINDER_MESSAGES = [
    "🌅 Selamat pagi! Hari baru, kesempatan baru untuk tetap strong!",
    "💪 Good morning, warrior! Hari ini adalah hari untuk melanjutkan victory streak!",  
    "🌟 Rise and shine! Recovery journey mu berlanjut hari ini!",
    "🔥 Morning motivation: Kamu sudah membuktikan kekuatanmu. Keep going!",
    "🌱 Pagi yang baik untuk pertumbuhan! Stay committed to your goals!"
]

# Emergency quick responses
EMERGENCY_QUICK_RESPONSES = [
    "🛑 STOP! Tarik napas dalam-dalam.",
    "💪 Kamu lebih kuat dari yang kamu kira!",
    "🌟 Dorongan ini akan berlalu. Stay strong!",
    "🎯 Ingat goals jangka panjangmu!",
    "⚡ Channel energi ini untuk sesuatu yang produktif!"
]

# Journal prompts
JOURNAL_PROMPTS = [
    "Bagaimana perasaanmu hari ini?",
    "Apa yang membuatmu bangga dari dirimu hari ini?", 
    "Trigger apa yang kamu rasakan dan bagaimana mengatasinya?",
    "Apa goal yang ingin kamu capai minggu ini?",
    "Ceritakan satu hal positif yang terjadi hari ini.",
    "Bagaimana progress recovery-mu minggu ini?",
    "Apa yang kamu pelajari tentang dirimu hari ini?"
]

# Motivational categories
MOTIVATION_CATEGORIES = [
    'strength',
    'progress', 
    'future_vision',
    'self_worth',
    'resilience'
]
