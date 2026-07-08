import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

# --- ENTERPRISE THEME SETUP ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# --- PROFESSIONAL PALETTE ---
COLOR_BG = "#09090b"           # Deepest Black/Zinc (Main Background)
COLOR_PANEL = "#18181b"        # Zinc-900 (Panels/Sidebar)
COLOR_BORDER = "#27272a"       # Zinc-800 (Borders)
COLOR_ACCENT = "#3b82f6"       # Royal Blue (Primary Action)
COLOR_ACCENT_HOVER = "#2563eb" # Darker Blue
COLOR_TEXT = "#e4e4e7"         # Zinc-200 (Main Text)
COLOR_TEXT_DIM = "#a1a1aa"     # Zinc-400 (Subtitles)
COLOR_DANGER = "#dc2626"       # Red (Deletions)
COLOR_STATUS = "#101012"       # Darker shade for footer

class DataDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Data Dashboard ")
        self.geometry("1400x900")
        self.configure(fg_color=COLOR_BG)

        self.df = None
        
        # --- MAIN LAYOUT ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. NAVIGATION SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=COLOR_PANEL)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self._init_sidebar()

        # 2. MAIN WORKSPACE
        self.main_view = ctk.CTkTabview(self, corner_radius=8, fg_color=COLOR_BG, 
                                        segmented_button_fg_color=COLOR_PANEL,
                                        segmented_button_selected_color=COLOR_ACCENT,
                                        segmented_button_unselected_color=COLOR_PANEL,
                                        segmented_button_selected_hover_color=COLOR_ACCENT_HOVER,
                                        text_color=COLOR_TEXT, height=50)
        self.main_view.grid(row=0, column=1, padx=20, pady=(10, 20), sticky="nsew")
        
        # Tabs
        self.tab_data = self.main_view.add("   DATA OVERVIEW   ")
        self.tab_clean = self.main_view.add("   CLEANING STUDIO   ")
        self.tab_viz = self.main_view.add("   ANALYTICS HUB   ")

        self._build_overview()
        self._build_cleaning()
        self._build_visualization()
        
        # Matplotlib Theme
        plt.style.use('dark_background')

    def _init_sidebar(self):
        # --- BRANDING HEADER ---
        header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header.pack(pady=(30, 20), padx=20, fill="x")
        
        # Two-tone professional title
        ctk.CTkLabel(header, text="DATA", font=("Roboto Medium", 30), text_color="white").pack(anchor="w")
        ctk.CTkLabel(header, text="DASHBOARD", font=("Roboto", 30, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", pady=(0, 5))
        
        # Separator Line
        div = ctk.CTkFrame(header, height=2, fg_color=COLOR_ACCENT)
        div.pack(fill="x", pady=(5, 5))
        ctk.CTkLabel(header, text="", font=("Roboto", 11), text_color=COLOR_TEXT_DIM).pack(anchor="w")

        # IMPORT BUTTON
        ctk.CTkButton(self.sidebar, text="Import Dataset", height=50, corner_radius=6, 
                      font=("Inter", 13, "bold"), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, 
                      command=self.load_file).pack(padx=25, pady=20, fill="x")

        # STATS PANEL
        self.stats = ctk.CTkFrame(self.sidebar, fg_color=COLOR_BG, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        self.stats.pack(fill="x", padx=25, pady=10)
        
        # Row Counter
        r_box = ctk.CTkFrame(self.stats, fg_color="transparent")
        r_box.pack(fill="x", padx=20, pady=(20, 5))
        ctk.CTkLabel(r_box, text="TOTAL ROWS", font=("Inter", 10, "bold"), text_color=COLOR_TEXT_DIM).pack(anchor="w")
        self.lbl_rows = ctk.CTkLabel(r_box, text="-", font=("Inter", 22, "bold"), text_color="white")
        self.lbl_rows.pack(anchor="w")

        # Col Counter
        c_box = ctk.CTkFrame(self.stats, fg_color="transparent")
        c_box.pack(fill="x", padx=20, pady=(5, 20))
        ctk.CTkLabel(c_box, text="TOTAL COLUMNS", font=("Inter", 10, "bold"), text_color=COLOR_TEXT_DIM).pack(anchor="w")
        self.lbl_cols = ctk.CTkLabel(c_box, text="-", font=("Inter", 22, "bold"), text_color="white")
        self.lbl_cols.pack(anchor="w")
        
        # --- FOOTER STATUS BAR ---
        status_panel = ctk.CTkFrame(self.sidebar, fg_color=COLOR_STATUS, corner_radius=0, height=80)
        status_panel.pack(side="bottom", fill="x")
        
        ctk.CTkFrame(status_panel, height=1, fg_color=COLOR_BORDER).pack(fill="x")

        ctk.CTkLabel(status_panel, text="ACTIVE DATASET", font=("Inter", 10, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=25, pady=(15, 0))
        self.lbl_filename = ctk.CTkLabel(status_panel, text="Waiting for input...", font=("Inter", 12), text_color="white")
        self.lbl_filename.pack(anchor="w", padx=25, pady=(0, 15))

        # EXPORT BUTTON
        ctk.CTkButton(self.sidebar, text="Export CSV", height=40, fg_color="transparent", border_width=1, border_color=COLOR_BORDER,
                      text_color="white", hover_color=COLOR_BORDER, 
                      font=("Inter", 12), command=self.save_file).pack(padx=25, pady=(0, 20), side="bottom", fill="x")

    def _build_overview(self):
        self.tab_data.grid_columnconfigure(0, weight=1); self.tab_data.grid_rowconfigure(0, weight=1)
        
        table_container = ctk.CTkFrame(self.tab_data, fg_color=COLOR_PANEL, border_width=1, border_color=COLOR_BORDER, corner_radius=8)
        table_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=10)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COLOR_PANEL, foreground="white", fieldbackground=COLOR_PANEL, 
                        rowheight=38, borderwidth=0, font=("Inter", 11))
        style.configure("Treeview.Heading", background="#202024", foreground="white", relief="flat", 
                        font=("Inter", 11, "bold"))
        style.map("Treeview", background=[("selected", COLOR_ACCENT)])

        vsb = ttk.Scrollbar(table_container, orient="vertical"); hsb = ttk.Scrollbar(table_container, orient="horizontal")
        self.tree = ttk.Treeview(table_container, yscrollcommand=vsb.set, xscrollcommand=hsb.set, show="headings")
        vsb.config(command=self.tree.yview); hsb.config(command=self.tree.xview)
        
        vsb.pack(side="right", fill="y", padx=2, pady=2)
        hsb.pack(side="bottom", fill="x", padx=2, pady=2)
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

    def _build_cleaning(self):
        self.tab_clean.grid_columnconfigure((0, 1), weight=1, uniform="group1")
        self.tab_clean.grid_rowconfigure(0, weight=4) 
        self.tab_clean.grid_rowconfigure(1, weight=1) 

        # --- LEFT PANEL: VALUE CORRECTION ---
        p_left = ctk.CTkFrame(self.tab_clean, fg_color=COLOR_PANEL, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        p_left.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        
        ctk.CTkLabel(p_left, text="VALUE CORRECTION", font=("Inter", 13, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(p_left, text="Sanitization", font=("Inter", 11, "bold"), text_color=COLOR_TEXT_DIM).pack(anchor="w", padx=20, pady=(5, 5))
        ctk.CTkButton(p_left, text="Remove Duplicates", command=self.clean_duplicates, height=40, fg_color=COLOR_BG, hover_color=COLOR_BORDER).pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(p_left, text="Missing Value Imputation", font=("Inter", 11, "bold"), text_color=COLOR_TEXT_DIM).pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkButton(p_left, text="Fill Nulls (Zero)", command=self.clean_fill_0, height=40, fg_color=COLOR_BG, hover_color=COLOR_BORDER).pack(fill="x", padx=20, pady=5)
        
        # --- FIXED LOGIC BUTTONS ---
        ctk.CTkButton(p_left, text="Fill Mean", command=self.clean_fill_mean_jitter, height=40, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER).pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(p_left, text="Fill Median", command=self.clean_fill_median_jitter, height=40, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER).pack(fill="x", padx=20, pady=5)

        # --- RIGHT PANEL: STRUCTURAL EDITING ---
        p_right = ctk.CTkFrame(self.tab_clean, fg_color=COLOR_PANEL, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        p_right.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        
        ctk.CTkLabel(p_right, text="STRUCTURAL EDITING", font=("Inter", 13, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=20, pady=(20, 15))

        ctk.CTkLabel(p_right, text="Data Type Conversion", font=("Inter", 11, "bold"), text_color=COLOR_TEXT_DIM).pack(anchor="w", padx=20, pady=(5, 5))
        row_cast = ctk.CTkFrame(p_right, fg_color="transparent")
        row_cast.pack(fill="x", padx=20)
        self.cmb_cast_col = ctk.CTkComboBox(row_cast, values=["Column"], width=180, fg_color=COLOR_BG, border_color=COLOR_BORDER)
        self.cmb_cast_col.pack(side="left", padx=(0, 10))
        self.cmb_cast_type = ctk.CTkComboBox(row_cast, values=["int", "float", "str", "datetime"], width=100, fg_color=COLOR_BG, border_color=COLOR_BORDER)
        self.cmb_cast_type.pack(side="left", padx=(0, 10))
        ctk.CTkButton(row_cast, text="Apply", width=80, command=self.apply_cast, fg_color=COLOR_BG, hover_color=COLOR_BORDER).pack(side="left")

        ctk.CTkLabel(p_right, text="Pruning (Drop Data)", font=("Inter", 11, "bold"), text_color=COLOR_TEXT_DIM).pack(anchor="w", padx=20, pady=(30, 5))
        
        row_del_col = ctk.CTkFrame(p_right, fg_color="transparent")
        row_del_col.pack(fill="x", padx=20, pady=5)
        self.cmb_drop_col = ctk.CTkComboBox(row_del_col, values=["Column"], width=290, fg_color=COLOR_BG, border_color=COLOR_BORDER)
        self.cmb_drop_col.pack(side="left", padx=(0, 10))
        ctk.CTkButton(row_del_col, text="Drop Col", width=80, command=self.drop_column, fg_color=COLOR_BG, hover_color=COLOR_DANGER, text_color=COLOR_DANGER).pack(side="left")

        row_del_row = ctk.CTkFrame(p_right, fg_color="transparent")
        row_del_row.pack(fill="x", padx=20, pady=5)
        self.ent_row_idx = ctk.CTkEntry(row_del_row, placeholder_text="Row Index ID", width=290, fg_color=COLOR_BG, border_color=COLOR_BORDER)
        self.ent_row_idx.pack(side="left", padx=(0, 10))
        ctk.CTkButton(row_del_row, text="Drop Row", width=80, command=self.drop_specific_row, fg_color=COLOR_BG, hover_color=COLOR_DANGER, text_color=COLOR_DANGER).pack(side="left")

        self.txt_log = ctk.CTkTextbox(self.tab_clean, height=120, fg_color="#000000", text_color="#22c55e", font=("Consolas", 10), corner_radius=6)
        self.txt_log.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=10)
        self.txt_log.insert("0.0", "> System Ready.\n")

    def _build_visualization(self):
        self.tab_viz.grid_columnconfigure(1, weight=1); self.tab_viz.grid_rowconfigure(0, weight=1)
        
        settings = ctk.CTkFrame(self.tab_viz, width=300, fg_color=COLOR_PANEL, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        settings.grid(row=0, column=0, sticky="nsw", padx=(0, 10), pady=10)
        
        ctk.CTkLabel(settings, text="PLOT SETTINGS", font=("Inter", 14, "bold"), text_color="white").pack(pady=(25, 25))
        
        for text, cmb_attr in [("Chart Type", "cmb_chart"), ("X - Axis", "cmb_x"), ("Y - Axis", "cmb_y")]:
            ctk.CTkLabel(settings, text=text, font=("Inter", 11, "bold"), text_color=COLOR_TEXT_DIM).pack(anchor="w", padx=20)
            cmb = ctk.CTkComboBox(settings, values=["-"], width=260, height=35, fg_color=COLOR_BG, border_color=COLOR_BORDER)
            setattr(self, cmb_attr, cmb)
            cmb.pack(pady=(5, 20), padx=20)
        
        self.cmb_chart.configure(values=["Histogram", "Box Plot", "Scatter Plot", "Line Chart", "Bar Chart", "Pie Chart"], command=self._update_viz_options)

        ctk.CTkButton(settings, text="Render Analytics", height=45, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, 
                      font=("Inter", 13, "bold"), command=self.plot_graph).pack(padx=20, pady=(20, 20), fill="x")

        plot_area = ctk.CTkFrame(self.tab_viz, fg_color=COLOR_BG, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        plot_area.grid(row=0, column=1, sticky="nsew", padx=0, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(5,4), dpi=100)
        self.fig.patch.set_facecolor(COLOR_BG)
        self.ax.set_facecolor(COLOR_BG)
        
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color(COLOR_BORDER)
        self.ax.spines['bottom'].set_color(COLOR_BORDER)
        self.ax.tick_params(colors=COLOR_TEXT_DIM)
        self.ax.yaxis.label.set_color(COLOR_TEXT_DIM)
        self.ax.xaxis.label.set_color(COLOR_TEXT_DIM)
        self.ax.title.set_color("white")

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_area)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=2, pady=2)

    def _log(self, msg):
        self.txt_log.configure(state="normal")
        self.txt_log.insert("end", f"> {msg}\n")
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")

    def _update_viz_options(self, choice):
        if choice in ["Histogram", "Box Plot", "Pie Chart"]:
            self.cmb_y.configure(state="disabled"); 
        else:
            self.cmb_y.configure(state="normal"); 

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx")])
        if not path: return
        try:
            self.df = pd.read_csv(path) if path.endswith('.csv') else pd.read_excel(path)
            self.filename = path.split("/")[-1]
            self.lbl_filename.configure(text=self.filename)
            self.refresh_ui()
            self._log(f"Loaded: {self.filename}")
            self.main_view.set("   DATA OVERVIEW   ")
        except Exception as e: messagebox.showerror("Error", str(e))

    def save_file(self):
        if self.df is None: return
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path: self.df.to_csv(path, index=False); messagebox.showinfo("Export", "Data exported successfully.")

    def refresh_ui(self):
        if self.df is None: return
        self.lbl_rows.configure(text=f"{self.df.shape[0]:,}")
        self.lbl_cols.configure(text=f"{self.df.shape[1]}")
        
        self.tree.delete(*self.tree.get_children()); self.tree["columns"] = list(self.df.columns)
        for c in self.df.columns: self.tree.heading(c, text=c); self.tree.column(c, width=120)
        for i, r in self.df.head(200).iterrows(): self.tree.insert("", "end", values=list(r))
        
        cols = list(self.df.columns)
        for cmb in [self.cmb_cast_col, self.cmb_drop_col, self.cmb_x, self.cmb_y]:
            cmb.configure(values=cols)
            if cols: cmb.set(cols[0])
        if len(cols) > 1: self.cmb_y.set(cols[1])

    # --- LOGIC ENGINES ---
    def clean_duplicates(self): 
        if self.df is None: return
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        self.refresh_ui(); self._log(f"Duplicates Removed: {before - len(self.df)} rows dropped.")
    
    def clean_fill_0(self): 
        if self.df is None: return
        self.df.fillna(0, inplace=True); self.refresh_ui(); self._log("Nulls filled with 0.")

    def _fill_random_jitter(self, method="mean"):
        if self.df is None: return
        
        # 1. SMART AUTO-CONVERSION
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                try:
                    cleaned = self.df[col].astype(str).str.replace(r'[$,]', '', regex=True)
                    converted = pd.to_numeric(cleaned, errors='coerce')
                    original_count = self.df[col].notna().sum()
                    valid_count = converted.notna().sum()
                    if valid_count >= (original_count * 0.5): 
                        self.df[col] = converted
                except: pass

        # 2. SELECT NUMERIC COLUMNS
        nums = self.df.select_dtypes(include=[np.number]).columns
        if len(nums) == 0:
            messagebox.showwarning("Data Error", "No numeric columns found.")
            return

        changes = 0
        for col in nums:
            missing = self.df[col].isna()
            count = missing.sum()
            
            if count > 0:
                changes += count
                valid_data = self.df[col].dropna()
                
                # --- DETECT TYPES ---
                is_integer = (valid_data % 1 == 0).all()
                # Strict check: If Median is positive, assume column is strictly positive
                is_mostly_positive = valid_data.median() >= 0

                mu = self.df[col].mean(); med = self.df[col].median(); sigma = self.df[col].std()
                if pd.isna(sigma) or sigma == 0: sigma = abs(mu * 0.1) if mu != 0 else 1.0
                
                center = mu if method == "mean" else med
                fill_values = np.random.normal(loc=center, scale=sigma, size=count)
                
                # --- STRICT NON-NEGATIVE ENFORCEMENT ---
                if is_mostly_positive:
                    fill_values = np.abs(fill_values)
                
                if is_integer:
                    fill_values = np.round(fill_values, 0)
                else:
                    fill_values = np.round(fill_values, 4)

                self.df.loc[missing, col] = fill_values

        if changes > 0:
            self.refresh_ui()
            self._log(f"Filled {changes} missing cells with {method}.")
        else:
            self._log("No numeric missing values found.")

    def clean_fill_mean_jitter(self): self._fill_random_jitter("mean")
    def clean_fill_median_jitter(self): self._fill_random_jitter("median")

    def drop_column(self): 
        if self.df is None: return
        col = self.cmb_drop_col.get()
        self.df.drop(columns=[col], inplace=True); self.refresh_ui(); self._log(f"Dropped Column: {col}")
    
    def drop_specific_row(self):
        if self.df is None: return
        try:
            idx = int(self.ent_row_idx.get())
            if idx in self.df.index:
                self.df.drop(idx, inplace=True); self.df.reset_index(drop=True, inplace=True)
                self.refresh_ui(); self._log(f"Dropped Row Index: {idx}")
            else: messagebox.showerror("Error", "Row Index not found")
        except: messagebox.showerror("Error", "Invalid Row Index")

    def apply_cast(self):
        if self.df is None: return
        try:
            col, dtype = self.cmb_cast_col.get(), self.cmb_cast_type.get()
            if dtype == 'int': self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0).astype(int)
            elif dtype == 'float': self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            elif dtype == 'str': self.df[col] = self.df[col].astype(str)
            elif dtype == 'datetime': self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
            self.refresh_ui(); self._log(f"Converted '{col}' to {dtype}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def plot_graph(self):
        if self.df is None: messagebox.showwarning("No Data", "Load a file first!"); return
        c_type, x_col, y_col = self.cmb_chart.get(), self.cmb_x.get(), self.cmb_y.get()
        self.ax.clear(); self.ax.grid(True, linestyle='--', alpha=0.1, color='white')
        
        try:
            y_is_num = pd.api.types.is_numeric_dtype(self.df[y_col]) if y_col in self.df.columns else False
            x_is_num = pd.api.types.is_numeric_dtype(self.df[x_col])

            if c_type == "Histogram":
                if x_is_num: sns.histplot(self.df[x_col].dropna(), ax=self.ax, kde=True, color=COLOR_ACCENT); self.ax.set_title(f"Distribution: {x_col}")
                else: 
                    counts = self.df[x_col].value_counts().head(10)
                    sns.barplot(x=counts.index.astype(str), y=counts.values, ax=self.ax, palette="mako"); self.ax.tick_params(axis='x', rotation=45)
            elif c_type == "Box Plot":
                if not x_is_num: raise ValueError("X must be numeric")
                sns.boxplot(y=self.df[x_col].dropna(), ax=self.ax, color=COLOR_ACCENT)
            elif c_type == "Scatter Plot":
                sns.scatterplot(x=self.df[x_col], y=self.df[y_col], ax=self.ax, color=COLOR_ACCENT, alpha=0.6)
            elif c_type == "Bar Chart":
                data = self.df.groupby(x_col)[y_col].sum() if y_is_num else self.df.groupby(x_col)[y_col].count()
                data = data.sort_values(ascending=False).head(20)
                sns.barplot(x=data.index.astype(str), y=data.values, ax=self.ax, palette="viridis"); self.ax.tick_params(axis='x', rotation=45)
            elif c_type == "Line Chart":
                data = self.df.groupby(x_col)[y_col].mean() if y_is_num else self.df.groupby(x_col)[y_col].count()
                self.ax.plot(data.index.astype(str), data.values, color=COLOR_ACCENT, marker='o', linewidth=2); self.ax.tick_params(axis='x', rotation=45)
            elif c_type == "Pie Chart":
                counts = self.df[x_col].value_counts().head(10)
                self.ax.pie(counts, labels=counts.index.astype(str), autopct="%1.1f%%", startangle=90)

            self.canvas.draw(); self._log(f"Chart Rendered: {c_type}")
        except Exception as e:
            self.ax.text(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center', color=COLOR_DANGER); self.canvas.draw()

if __name__ == "__main__":
    app = DataDashboard()
    app.mainloop()