import random
import json
import os
from typing import List, Dict

class MotivationalService:
    """Service untuk menyediakan quotes motivasi dan tips coping"""
    
    def __init__(self):
        self.quotes = self._load_quotes()
        self.tips = self._load_tips()
        self.emergency_messages = self._load_emergency_messages()
    
    def _load_quotes(self) -> List[Dict]:
        """Load motivational quotes from JSON file"""
        quotes_file = "data/quotes.json"
        if os.path.exists(quotes_file):
            with open(quotes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Default quotes if file doesn't exist
        return [
            {
                "text": "Setiap hari adalah kesempatan baru untuk menjadi versi terbaik dari diri Anda.",
                "author": "PMO Recovery Coach"
            },
            {
                "text": "Kekuatan sejati datang dari kemampuan mengendalikan diri sendiri.",
                "author": "PMO Recovery Coach"
            },
            {
                "text": "Recovery bukan tentang kesempurnaan, tapi tentang kemajuan yang konsisten.",
                "author": "PMO Recovery Coach"
            },
            {
                "text": "Saat Anda merasa lemah, ingatlah bahwa Anda sudah terbukti kuat sampai sejauh ini.",
                "author": "PMO Recovery Coach"
            },
            {
                "text": "Otak Anda sedang healing. Beri waktu dan kesabaran pada prosesnya.",
                "author": "PMO Recovery Coach"
            }
        ]
    
    def _load_tips(self) -> List[Dict]:
        """Load coping tips from JSON file"""
        tips_file = "data/tips.json"
        if os.path.exists(tips_file):
            with open(tips_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Default tips if file doesn't exist
        return [
            {
                "category": "physical",
                "title": "Olahraga Ringan",
                "description": "Lakukan push-up, sit-up, atau jalan kaki selama 10-15 menit untuk mengalihkan energi.",
                "duration": "10-15 menit"
            },
            {
                "category": "mental",
                "title": "Teknik Pernapasan",
                "description": "Tarik napas dalam 4 detik, tahan 4 detik, hembuskan 6 detik. Ulangi 5-10 kali.",
                "duration": "5-10 menit"
            },
            {
                "category": "distraction",
                "title": "Cold Shower",
                "description": "Mandi air dingin dapat mengurangi dorongan dan meningkatkan mental clarity.",
                "duration": "5-10 menit"
            },
            {
                "category": "mindfulness",
                "title": "Meditation",
                "description": "Duduk tenang, fokus pada napas, dan amati pikiran tanpa menghakimi.",
                "duration": "10-20 menit"
            },
            {
                "category": "productive",
                "title": "Journaling",
                "description": "Tulis perasaan dan pikiran Anda untuk memahami trigger dan emosi.",
                "duration": "15-30 menit"
            }
        ]
    
    def _load_emergency_messages(self) -> List[str]:
        """Load emergency intervention messages"""
        return [
            "🛑 STOP! Tarik napas dalam-dalam. Kamu lebih kuat dari yang kamu kira.",
            "💪 Ingat kenapa kamu memulai journey ini. Jangan sia-siakan progress yang sudah kamu buat.",
            "🌟 Dorongan ini akan berlalu. Semua urge bersifat sementara, tapi keputusan baik berdampak permanen.",
            "🔥 Kamu sudah berhasil menolak berkali-kali sebelumnya. Kamu bisa melakukannya lagi!",
            "🎯 Fokus pada tujuan jangka panjang. 10 menit kesenangan tidak sepadan dengan kehancuran streak.",
            "⚡ Channel energi ini untuk sesuatu yang produktif. Olahraga, belajar, atau creative activity.",
            "🧠 Otakmu sedang healing. Jangan beri dia racun yang akan menghentikan proses recovery.",
            "👑 Kamu adalah raja/ratu dari kehidupanmu sendiri. Jangan biarkan impuls mengendalikanmu."
        ]
    
    def get_daily_quote(self) -> Dict:
        """Get random daily motivational quote"""
        return random.choice(self.quotes)
    
    def get_coping_tip(self, category: str = None) -> Dict:
        """Get coping strategy tip, optionally filtered by category"""
        if category:
            filtered_tips = [tip for tip in self.tips if tip.get('category') == category]
            if filtered_tips:
                return random.choice(filtered_tips)
        
        return random.choice(self.tips)
    
    def get_emergency_message(self) -> str:
        """Get emergency intervention message"""
        return random.choice(self.emergency_messages)
    
    def get_streak_encouragement(self, streak_days: int) -> str:
        """Get encouragement message based on streak length"""
        if streak_days == 0:
            return "🌱 Setiap journey dimulai dari langkah pertama. Hari ini adalah hari pertamamu menuju kebebasan!"
        elif streak_days == 1:
            return "🎉 Hari pertama selesai! Kamu sudah membuktikan bahwa kamu bisa melakukannya!"
        elif streak_days < 7:
            return f"💪 {streak_days} hari clean! Tubuh dan pikiranmu mulai merasakan perubahan positif!"
        elif streak_days < 30:
            return f"🔥 {streak_days} hari! Sistem dopamine-mu mulai recovery. Keep going strong!"
        elif streak_days < 90:
            return f"🌟 {streak_days} hari clean! Perubahan besar sedang terjadi dalam hidupmu!"
        else:
            return f"👑 {streak_days} hari! Kamu sudah menjadi master of self-control. Incredible achievement!"
    
    def get_relapse_support(self) -> str:
        """Get supportive message after relapse"""
        messages = [
            "💙 Relapse bukan akhir dari segalanya. Ini adalah bagian dari journey recovery. Yang penting adalah bangkit kembali.",
            "🌅 Setiap matahari terbit adalah kesempatan baru. Hari ini kamu bisa memulai lagi dengan lebih kuat.",
            "📈 Progress bukan garis lurus. Ada naik turun, tapi trend umumnya tetap ke atas. Keep fighting!",
            "💎 Berlian terbentuk dari tekanan. Pengalaman ini membuatmu lebih kuat dan bijak.",
            "🎯 Focus pada lesson yang bisa dipelajari. Apa trigger-nya? Bagaimana mencegahnya di masa depan?",
            "🤝 Kamu tidak sendirian dalam journey ini. Banyak orang yang melewati path yang sama dan berhasil recover."
        ]
        return random.choice(messages)
    
    def get_educational_content(self, topic: str = "general") -> Dict:
        """Get educational content about PMO effects"""
        education_content = {
            "dopamine": {
                "title": "🧠 Sistem Dopamine dan Recovery",
                "content": """Dopamine adalah neurotransmitter yang mengatur reward dan motivasi. PMO menyebabkan lonjakan dopamine yang tidak natural, membuat aktivitas normal terasa kurang memuaskan.

Selama recovery:
• Minggu 1-2: Withdrawal symptoms (mood swing, low motivation)
• Minggu 3-4: Dopamine sensitivity mulai recovery
• Bulan 2-3: Mental clarity dan motivasi meningkat
• Bulan 3+: Sistem reward kembali normal

Recovery adalah proses. Bersabarlah dengan dirimu sendiri."""
            },
            "benefits": {
                "title": "✨ Manfaat NoFap/PMO Recovery",
                "content": """Benefits yang dilaporkan banyak orang:

Physical:
• Energi meningkat
• Kualitas tidur lebih baik
• Kulit lebih sehat
• Postur tubuh lebih tegap

Mental:
• Konsentrasi meningkat
• Mental clarity
• Kepercayaan diri naik
• Motivasi untuk goals lain

Social:
• Eye contact lebih baik
• Social anxiety berkurang
• Relationship lebih dalam
• Charisma natural

Remember: Results vary per person. Focus on your own journey."""
            },
            "neuroplasticity": {
                "title": "🔄 Neuroplasticity dan Brain Rewiring",
                "content": """Otak memiliki kemampuan neuroplasticity - kemampuan membentuk koneksi neural baru dan mengubah yang lama.

Saat PMO:
• Pathway reward terfokus pada PMO
• Aktivitas lain jadi kurang rewarding
• Tolerance meningkat (butuh stimulasi lebih)

Saat Recovery:
• Old pathways gradually weaken
• New healthy pathways strengthen
• Natural rewards jadi meaningful lagi

Setiap hari clean = reinforcement positive pathways
Setiap relapse = strengthening old patterns

That's why consistency matters more than perfection!"""
            }
        }
        
        return education_content.get(topic, education_content["general"] if "general" in education_content else education_content["dopamine"])
