import random
from typing import List, Dict
from src.services.motivational_service import MotivationalService

class EmergencyService:
    """Service untuk menangani mode darurat saat user ingin relapse"""
    
    def __init__(self):
        self.motivational_service = MotivationalService()
        self.emergency_protocols = self._load_emergency_protocols()
    
    def _load_emergency_protocols(self) -> List[Dict]:
        """Load emergency intervention protocols"""
        return [
            {
                "name": "immediate_distraction",
                "title": "🚨 Immediate Distraction Protocol",
                "steps": [
                    "Berdiri dan tinggalkan area sekarang juga",
                    "Nyalakan musik favorit dengan volume keras",
                    "Lakukan 20 jumping jacks atau push-ups",
                    "Ambil air dingin dan minum/basuh wajah",
                    "Hubungi teman atau keluarga"
                ],
                "duration": "5-10 menit"
            },
            {
                "name": "mindfulness_intervention",
                "title": "🧘 Mindfulness Emergency Protocol",
                "steps": [
                    "Duduk dengan posisi tegak",
                    "Tutup mata dan fokus pada napas",
                    "Amati sensasi urge tanpa menghakimi",
                    "Ingat: 'Ini hanya perasaan, akan berlalu'",
                    "Visualisasi diri masa depan yang bebas dari PMO"
                ],
                "duration": "10-15 menit"
            },
            {
                "name": "accountability_check",
                "title": "🤝 Accountability Emergency Check",
                "steps": [
                    "Buka catatan goals dan reason kenapa quit PMO",
                    "Lihat progress streak yang sudah dibuat",
                    "Bayangkan perasaan menyesal setelah relapse",
                    "Ingat komitmen pada diri sendiri",
                    "Tulis jurnal tentang perasaan sekarang"
                ],
                "duration": "15-20 menit"
            }
        ]
    
    def get_emergency_intervention(self) -> Dict:
        """Get complete emergency intervention package"""
        protocol = random.choice(self.emergency_protocols)
        emergency_message = self.motivational_service.get_emergency_message()
        coping_tip = self.motivational_service.get_coping_tip()
        
        return {
            "alert_message": emergency_message,
            "protocol": protocol,
            "coping_tip": coping_tip,
            "motivational_quote": self.motivational_service.get_daily_quote(),
            "reminder": "🎯 Remember: Urges are temporary, but your recovery is permanent. You've got this!"
        }
    
    def get_urge_surfing_guide(self) -> Dict:
        """Get urge surfing technique guide"""
        return {
            "title": "🌊 Urge Surfing Technique",
            "description": "Teknik untuk 'menunggangi' urge sampai berlalu tanpa melawan atau menyerah",
            "steps": [
                {
                    "step": 1,
                    "instruction": "Acknowledge the urge",
                    "detail": "Sadari dan akui bahwa urge sedang datang. Jangan lawan atau coba hilangkan."
                },
                {
                    "step": 2,
                    "instruction": "Observe without judgment",
                    "detail": "Amati sensasi fisik dan mental tanpa menghakimi. 'Oh, ini urge yang datang.'"
                },
                {
                    "step": 3,
                    "instruction": "Breathe mindfully",
                    "detail": "Fokus pada napas. Napas dalam, tahan, hembuskan perlahan."
                },
                {
                    "step": 4,
                    "instruction": "Wait for the peak",
                    "detail": "Urge akan naik ke puncak seperti gelombang, lalu turun sendiri."
                },
                {
                    "step": 5,
                    "instruction": "Ride it out",
                    "detail": "Tunggu sampai intensitas turun. Biasanya 10-20 menit."
                }
            ],
            "key_points": [
                "Urge adalah sensasi sementara yang pasti berlalu",
                "Melawan urge membuat semakin kuat (resistance)",
                "Menyerah pada urge membuat semakin sering datang",
                "Urge surfing melatih resilience dan self-control"
            ]
        }
    
    def get_trigger_analysis(self) -> Dict:
        """Get trigger analysis and prevention guide"""
        return {
            "title": "🎯 Trigger Analysis & Prevention",
            "common_triggers": {
                "emotional": [
                    "Stress dari kerja/sekolah",
                    "Kesepian atau boredom",
                    "Depresi atau anxiety",
                    "Kemarahan atau frustasi",
                    "Perasaan tidak berharga"
                ],
                "environmental": [
                    "Sendirian di kamar",
                    "Malam hari atau waktu luang",
                    "Akses internet tanpa filter",
                    "Social media tertentu",
                    "Konten yang memicu (ads, film, dll)"
                ],
                "physical": [
                    "Kelelahan atau kurang tidur",
                    "Hormon cycle (morning/evening)",
                    "Setelah olahraga atau mandi",
                    "Idle time tanpa aktivitas",
                    "Posisi tertentu (lying in bed)"
                ]
            },
            "prevention_strategies": {
                "emotional": "Develop healthy coping mechanisms: journaling, meditation, talking to friends",
                "environmental": "Modify your environment: use website blockers, stay in public areas",
                "physical": "Maintain good sleep schedule, stay busy with productive activities"
            },
            "action_plan": [
                "Identify your top 3 triggers",
                "Create specific action plan for each trigger",
                "Practice new responses consistently",
                "Track trigger patterns in journal",
                "Adjust strategies based on what works"
            ]
        }
    
    def get_emergency_contacts(self) -> Dict:
        """Get emergency support contacts and resources"""
        return {
            "title": "🆘 Emergency Support Resources",
            "immediate_help": [
                "Call a trusted friend or family member",
                "Go to a public place (cafe, mall, park)",
                "Use accountability app or partner",
                "Join online support community chat",
                "Contact professional counselor if available"
            ],
            "hotlines": {
                "indonesia": {
                    "sejiwa": "119 ext 8",
                    "halo_kemkes": "1500-567",
                    "description": "Free psychological support hotlines in Indonesia"
                },
                "international": {
                    "crisis_text_line": "Text HOME to 741741",
                    "description": "24/7 crisis support via text message"
                }
            },
            "online_communities": [
                "Reddit: r/NoFap, r/pornfree",
                "Discord: NoFap communities",
                "Local support groups (search online)",
                "Professional therapy platforms"
            ],
            "reminder": "It's okay to ask for help. Recovery is easier with support from others."
        }
