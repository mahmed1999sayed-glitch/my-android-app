import math
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window

# ضبط حجم الشاشة للمعاينة كأنه موبايل على الكمبيوتر
Window.size = (390, 680)

class FullSurveyApp(BoxLayout):
    def __init__(self, **kwargs):
        super(FullSurveyApp, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 12
        self.spacing = 10
        
        # متغيرات لتخزين نصوص الملفات المرفوعة
        self.s1_data = ""
        self.s2_data = ""

        self.build_ui()

    def build_ui(self):
        # --- TITLE ---
        self.add_widget(Label(text="Survey Volume Pro", font_size=22, bold=True, size_hint_y=None, height=35, color=[0, 0.7, 1, 1]))

        # --- SECTION 1: DATA INPUT ---
        self.add_widget(Label(text="1. Data Input (Select Files)", font_size=15, bold=True, size_hint_y=None, height=25))
        
        input_grid = GridLayout(cols=2, spacing=8, size_hint_y=None, height=150)
        
        # اختيار الفورمات
        input_grid.add_widget(Label(text="Format Type:", font_size=14))
        self.format_spinner = Spinner(text="PENZD", values=("PENZD", "PNEZD"))
        input_grid.add_widget(self.format_spinner)

        # رفع ملف السطح الأول
        input_grid.add_widget(Label(text="Surface 1 (Existing):", font_size=14))
        self.s1_btn = Button(text="Choose File (S1)", background_color=[0.2, 0.6, 0.2, 1], font_size=13)
        self.s1_btn.bind(on_press=lambda inst: self.open_file_popup("S1"))
        input_grid.add_widget(self.s1_btn)

        # رفع ملف السطح الثاني
        self.s2_label_title = Label(text="Surface 2 (Design):", font_size=14)
        input_grid.add_widget(self.s2_label_title)
        self.s2_btn = Button(text="Choose File (S2)", background_color=[0.2, 0.6, 0.2, 1], font_size=13)
        self.s2_btn.bind(on_press=lambda inst: self.open_file_popup("S2"))
        input_grid.add_widget(self.s2_btn)

        self.add_widget(input_grid)

        # --- SECTION 2: CALCULATION METHOD ---
        self.add_widget(Label(text="2. Calculation Method", font_size=15, bold=True, size_hint_y=None, height=25))
        
        method_grid = GridLayout(cols=2, spacing=5, size_hint_y=None, height=70)
        
        method_grid.add_widget(Label(text="Method:", font_size=14))
        self.method_spinner = Spinner(text="Surface to Surface", values=("Surface to Surface", "Surface to Level"))
        self.method_spinner.bind(text=self.on_method_change)
        method_grid.add_widget(self.method_spinner)

        self.level_label = Label(text="Fixed Level (m):", color=[0.5, 0.5, 0.5, 1], font_size=14)
        self.level_input = TextInput(hint_text="e.g. 10.50", disabled=True, multiline=False, font_size=13)
        method_grid.add_widget(self.level_label)
        method_grid.add_widget(self.level_input)

        self.add_widget(method_grid)

        # --- PROCESS BUTTON ---
        self.calc_btn = Button(text="Calculate Quantities", background_color=[0, 0.5, 0.9, 1], font_size=16, bold=True, size_hint_y=None, height=45)
        self.calc_btn.bind(on_press=self.calculate_volumes)
        self.add_widget(self.calc_btn)

        # --- SECTION 3: RESULTS ---
        self.add_widget(Label(text="3. Results", font_size=15, bold=True, size_hint_y=None, height=25))
        
        scroll = ScrollView()
        res_layout = GridLayout(cols=1, spacing=8, size_hint_y=None)
        res_layout.bind(minimum_height=res_layout.setter('height'))

        self.cut_label = Label(text="Cut Volume: 0.000 m³", font_size=18, bold=True, color=[1, 0.2, 0.2, 1], size_hint_y=None, height=35)
        self.fill_label = Label(text="Fill Volume: 0.000 m³", font_size=18, bold=True, color=[0.2, 1, 0.2, 1], size_hint_y=None, height=35)
        self.net_label = Label(text="Net Difference: 0.000 m³", font_size=16, bold=True, size_hint_y=None, height=35)

        res_layout.add_widget(self.cut_label)
        res_layout.add_widget(self.fill_label)
        res_layout.add_widget(self.net_label)
        scroll.add_widget(res_layout)
        self.add_widget(scroll)

    def on_method_change(self, spinner, text):
        if text == "Surface to Level":
            self.level_input.disabled = False
            self.level_label.color = [1, 1, 1, 1]
            self.s2_btn.disabled = True
            self.s2_btn.text = "Disabled"
        else:
            self.level_input.disabled = True
            self.level_input.text = ""
            self.level_label.color = [0.5, 0.5, 0.5, 1]
            self.s2_btn.disabled = False
            self.s2_btn.text = "Choose File (S2)" if not self.s2_data else "File Loaded ✓"

    # --- نافذة تصفح ملفات الموبايل والكمبيوتر ---
    def open_file_popup(self, surface_target):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # مستعرض الملفات الأيقوني المدمج
        file_chooser = FileChooserIconView(path=os.path.expanduser("~"), filters=['*.csv', '*.txt', '*.sdr', '*.gsi'])
        popup_layout.add_widget(file_chooser)
        
        buttons_layout = BoxLayout(size_hint_y=None, height=45, spacing=10)
        cancel_btn = Button(text="Cancel", font_size=14)
        select_btn = Button(text="Select File", background_color=[0, 0.6, 0.8, 1], font_size=14)
        
        buttons_layout.add_widget(cancel_btn)
        buttons_layout.add_widget(select_btn)
        popup_layout.add_widget(buttons_layout)
        
        popup = Popup(title=f"Select Data File for {surface_target}", content=popup_layout, size_hint=(0.95, 0.95))
        
        cancel_btn.bind(on_press=popup.dismiss)
        
        def load_file(instance):
            if file_chooser.selection:
                file_path = file_chooser.selection[0]
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()
                    
                    filename = os.path.basename(file_path)
                    if surface_target == "S1":
                        self.s1_data = file_content
                        self.s1_btn.text = f"{filename} ✓"
                    else:
                        self.s2_data = file_content
                        self.s2_btn.text = f"{filename} ✓"
                except Exception as e:
                    if surface_target == "S1": self.s1_btn.text = "Error Loading!"
                    else: self.s2_btn.text = "Error Loading!"
                popup.dismiss()

        select_btn.bind(on_press=load_file)
        popup.open()

    def parse_data(self, text_content, fmt):
        points = []
        lines = text_content.strip().split('\n')
        for line in lines:
            if not line.strip():
                continue
            cleaned = line.replace('\t', ' ').replace(',', ' ')
            parts = [p.strip() for p in cleaned.split(' ') if p.strip()]
            if len(parts) < 4:
                continue
            try:
                p_id = parts[0]
                if fmt == "PENZD":
                    e, n, z = float(parts[1]), float(parts[2]), float(parts[3])
                else:
                    n, e, z = float(parts[1]), float(parts[2]), float(parts[3])
                points.append({'E': e, 'N': n, 'Z': z})
            except ValueError:
                continue
        return points

    def generate_surface_grid(self, points):
        if len(points) < 3:
            return None
        e_vals = [p['E'] for p in points]
        n_vals = [p['N'] for p in points]
        min_e, max_e = min(e_vals), max(e_vals)
        min_n, max_n = min(n_vals), max(n_vals)
        
        grid_res = 1.0  
        cols = int((max_e - min_e) / grid_res) + 1
        rows = int((max_n - min_n) / grid_res) + 1
        
        grid = {}
        for r in range(rows):
            for c in range(cols):
                ge = min_e + c * grid_res
                gn = min_n + r * grid_res
                w_sum = 0
                z_sum = 0
                for p in points:
                    d = math.hypot(p['E'] - ge, p['N'] - gn)
                    if d == 0:
                        z_sum = p['Z']
                        w_sum = 1
                        break
                    w = 1.0 / (d ** 2)
                    z_sum += p['Z'] * w
                    w_sum += w
                grid[(r, c)] = {'Z': (z_sum / w_sum) if w_sum > 0 else 0, 'area': grid_res * grid_res}
        return grid

    def calculate_volumes(self, instance):
        fmt = self.format_spinner.text
        method = self.method_spinner.text
        
        if not self.s1_data:
            self.cut_label.text = "Error: Please select Surface 1 file!"
            return
            
        s1_pts = self.parse_data(self.s1_data, fmt)
        if not s1_pts or len(s1_pts) < 3:
            self.cut_label.text = "Error: S1 needs at least 3 valid points!"
            return
            
        grid1 = self.generate_surface_grid(s1_pts)
        total_cut = 0.0
        total_fill = 0.0

        if method == "Surface to Surface":
            if not self.s2_data:
                self.fill_label.text = "Error: Please select Surface 2 file!"
                return
            s2_pts = self.parse_data(self.s2_data, fmt)
            if not s2_pts or len(s2_pts) < 3:
                self.fill_label.text = "Error: S2 needs at least 3 valid points!"
                return
            grid2 = self.generate_surface_grid(s2_pts)
            
            for coord, cell1 in grid1.items():
                if coord in grid2:
                    cell2 = grid2[coord]
                    diff = cell1['Z'] - cell2['Z']
                    vol = diff * cell1['area']
                    if vol > 0: total_cut += vol
                    else: total_fill += abs(vol)
                        
        elif method == "Surface to Level":
            try:
                lvl = float(self.level_input.text)
            except ValueError:
                self.cut_label.text = "Error: Input valid level number!"
                return
                
            for coord, cell1 in grid1.items():
                diff = cell1['Z'] - lvl
                vol = diff * cell1['area']
                if vol > 0: total_cut += vol
                else: total_fill += abs(vol)

        net_diff = total_cut - total_fill
        
        self.cut_label.text = f"Cut Volume: {total_cut:.3f} m³"
        self.fill_label.text = f"Fill Volume: {total_fill:.3f} m³"
        self.net_label.text = f"Net (Cut-Fill): {net_diff:.3f} m³"

class SurveyApp(App):
    def build(self):
        return FullSurveyApp()

if __name__ == '__main__':
    SurveyApp().run()