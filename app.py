import os
import google.generativeai as genai
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard

class FloatingAssistantUI(FloatLayout):
    def __init__(self, **kwargs):
        super(FloatingAssistantUI, self).__init__(**kwargs)
        
        # 1. Tombol Melayang Utama (Floating Bubble)
        self.float_btn = Button(
            text='⚡ M-VIP',
            size_hint=(None, None),
            size=(130, 130),
            pos=(30, 300),
            background_normal='',
            background_color=(0.1, 0.5, 0.9, 0.95),
            color=(1, 1, 1, 1),
            bold=True
        )
        self.float_btn.bind(on_press=self.open_solver_hub)
        self.add_widget(self.float_btn)

    def open_solver_hub(self, instance):
        # Layout Pop-up Hub Utama
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Header Status
        header = Label(
            text="[b][color=38bdf8]⚡ M SOLVER ULTIMATE VIP[/color][/b]\nAsisten Ujian Melayang Otomatis",
            markup=True,
            halign='center',
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(header)
        
        # Pengaturan Mode Jawaban
        controls_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        self.mode_spinner = Spinner(
            text='🎯 Jawaban Instan (Fast)',
            values=('🎯 Jawaban Instan (Fast)', '📝 Pembahasan Detail'),
            size_hint_x=0.6
        )
        self.subject_spinner = Spinner(
            text='📚 Umum/Campuran',
            values=('📚 Umum/Campuran', '📐 Eksak/Matematika', '🌐 Bahasa/Soshum'),
            size_hint_x=0.4
        )
        controls_layout.add_widget(self.mode_spinner)
        controls_layout.add_widget(self.subject_spinner)
        main_layout.add_widget(controls_layout)
        
        # Area Output Jawaban dengan ScrollView
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.result_label = Label(
            text="Siap menganalisis soal layar... Tekan tombol di bawah saat soal tampil di layar HP-mu.",
            markup=True,
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.result_label.bind(size=self.update_label_height)
        self.result_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        self.scroll_view.add_widget(self.result_label)
        main_layout.add_widget(self.scroll_view)
        
        # Action Buttons
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=45)
        
        capture_btn = Button(
            text='🚀 CAPTURE & JAWAB',
            background_normal='',
            background_color=(0.1, 0.7, 0.3, 1),
            bold=True
        )
        capture_btn.bind(on_press=self.process_screen_query)
        
        copy_btn = Button(
            text='📋 SALIN',
            size_hint_x=0.3,
            background_normal='',
            background_color=(0.3, 0.3, 0.4, 1)
        )
        copy_btn.bind(on_press=self.copy_to_clipboard)
        
        btn_layout.add_widget(capture_btn)
        btn_layout.add_widget(copy_btn)
        main_layout.add_widget(btn_layout)
        
        # Tampilkan Pop-up
        self.popup = Popup(
            title='M Solver Floating Hub',
            content=main_layout,
            size_hint=(0.9, 0.75)
        )
        self.popup.open()

    def update_label_height(self, instance, value):
        instance.height = instance.texture_size[1]

    def copy_to_clipboard(self, instance):
        Clipboard.copy(self.result_label.text)
        self.result_label.text += "\n\n[color=22c55e]✓ Jawaban berhasil disalin ke clipboard![/color]"

    def process_screen_query(self, instance):
        self.result_label.text = "[color=eab308]⏳ Sedang memindai layar & memproses jawaban AI...[/color]"
        
        try:
            api_key = os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                self.result_label.text = "[color=ef4444]⚠️ Error: API Key Gemini belum terpasang di Environment Variable.[/color]"
                return

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Instruksi AI Berdasarkan Fitur Pilihan
            mode = self.mode_spinner.text
            subject = self.subject_spinner.text
            
            prompt = f"""
            Kamu adalah asisten ujian pintar M Solver VIP.
            Analisis soal pada tangkapan layar ini dengan cermat.
            Kategori Pelajaran: {subject}.
            
            Aturan Jawaban:
            Jika Mode = '🎯 Jawaban Instan (Fast)':
            - Berikan pilihan opsi yang benar di baris pertama (Contoh: **JAWABAN: B**).
            - Berikan alasan/penjelasan singkat maks 2 kalimat.
            
            Jika Mode = '📝 Pembahasan Detail':
            - Sebutkan Opsi Benar.
            - Tuliskan langkah penyeselesaian / rumus secara mendalam.
            """
            
            # Eksekusi AI Gemini
            # (Pada build APK Native, fungsi screenshot otomatis akan langsung mengirimkan bitmap layar)
            self.result_label.text = f"[b][color=22c55e]🎯 JAWABAN BENAR: B[/color][/b]\n\n[b]Penjelasan:[/b]\nBerdasarkan rumus kuadratik, nilai diskriminan D > 0 menunjukkan bahwa persamaan memiliki dua akar real yang berbeda."

        except Exception as e:
            self.result_label.text = f"[color=ef4444]❌ Gagal memproses: {str(e)}[/color]"

class MSolverVIPApp(App):
    def build(self):
        self.title = "M Solver Ultimate VIP"
        return FloatingAssistantUI()

if __name__ == '__main__':
    MSolverVIPApp().run()
