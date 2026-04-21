import tkinter as tk
from tkinter import messagebox

class FreelancerFinalEdition:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Freelancer")
        self.ventana.geometry("1350x850") 
        self.ventana.configure(bg="#f1f5f9")

        # Configuración de colores
        self.NAVY = "#0f172a"
        self.ACCENT = "#3b82f6"
        self.EMERALD = "#10b981"
        self.AMBER = "#f59e0b"
        self.CARD_WHITE = "#ffffff"
        self.TEXT_MAIN = "#1e293b"
        self.TEXT_MUTE = "#64748b"

        self.tarjetas = []
        self.pagos = []
        self.dp = []
        self.dias_semana = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO"]
        self.frame_reglas = None 

        self.setup_ui()

    def setup_ui(self):
        # Configuración inicial de la interfaz
        sidebar = tk.Frame(self.ventana, bg=self.NAVY, width=280)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="HORARIO DEL\nFREELANCER", fg="white", bg=self.NAVY, 
                 font=("Segoe UI", 20, "bold"), justify="center").pack(pady=(20, 30))

        input_frame = tk.Frame(sidebar, bg=self.NAVY, padx=20)
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="PAGOS SEMANALES", fg="#94a3b8", bg=self.NAVY, 
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        
        self.entry_datos = tk.Entry(input_frame, font=("Consolas", 11), bg="#1e293b", 
                                    fg="white", relief="flat", insertbackground="white")
        self.entry_datos.pack(fill="x", pady=(8, 20), ipady=10)

        self.btn_run = tk.Button(input_frame, text="EJECUTAR ANALISIS", command=self.iniciar,
                                 bg=self.EMERALD, fg="white", font=("Segoe UI", 10, "bold"),
                                 relief="flat", cursor="hand2", pady=10)
        self.btn_run.pack(fill="x")

        # Panel de informacion tecnica
        info_box = tk.Frame(sidebar, bg="#1e293b", pady=20, padx=20)
        info_box.pack(side="bottom", fill="x", padx=20, pady=40)
        metricas_texto = "Complejidad: O(n)\nHorario: Lun - Sab\nMetodo: Prog. Dinamica"
        tk.Label(info_box, text=metricas_texto, bg="#1e293b", fg="#94a3b8", 
                 font=("Consolas", 9), justify="left").pack(anchor="w")

        # Contenedor principal de resultados
        self.main = tk.Frame(self.ventana, bg="#f1f5f9")
        self.main.pack(side="right", fill="both", expand=True, padx=40, pady=30)

        header = tk.Frame(self.main, bg="white", highlightthickness=1, highlightbackground="#e2e8f0", pady=30)
        header.pack(fill="x", pady=(0, 30))
        tk.Label(header, text="PROYECCION DE INGRESOS", fg=self.TEXT_MUTE, bg="white", font=("Segoe UI", 9, "bold")).pack()
        self.lbl_ganancia = tk.Label(header, text="$0.00", fg=self.TEXT_MAIN, bg="white", font=("Segoe UI", 42, "bold"))
        self.lbl_ganancia.pack()

        self.content_wrapper = tk.Frame(self.main, bg="#f1f5f9")
        self.content_wrapper.pack(fill="both", expand=True)

        self.mostrar_reglas()

    def mostrar_reglas(self):
        self.frame_reglas = tk.Frame(self.content_wrapper, bg="white", padx=40, pady=40,
                                     highlightthickness=1, highlightbackground="#e2e8f0")
        self.frame_reglas.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(self.frame_reglas, text="COMO ORGANIZAR TU SEMANA", fg=self.ACCENT, bg="white", 
                 font=("Segoe UI", 14, "bold")).pack(pady=(0, 20))
        
        reglas = (
            "Bienvenido a Freelancer Pro!\n\n"
            "Solo ingresa tus pagos diarios (separados por comas)\n"
            "y nosotros calculamos tu mejor plan de trabajo.\n\n"
            "Recuerda: Si trabajas un dia, el siguiente es descanso.\n"
            "El sistema elegira automaticamente los dias que\n"
            "mas dinero te dejen.\n\n"
            "Ingresa tus montos y presiona 'Ejecutar'."
        )
        
        tk.Label(self.frame_reglas, text=reglas, fg=self.TEXT_MAIN, bg="white", 
                 font=("Segoe UI", 11), justify="left", wraplength=500).pack()

    def iniciar(self):
        # Validacion y conversion de entrada a lista de pagos
        texto_entrada = self.entry_datos.get().strip()
        if not texto_entrada:
            messagebox.showwarning("Atencion", "Ingrese los pagos.")
            return

        try:
            self.pagos = [int(x.strip()) for x in texto_entrada.split(",") if x.strip()]
        except ValueError:
            messagebox.showerror("Error", "Use solo numeros y comas.")
            return

        if self.frame_reglas:
            self.frame_reglas.destroy()
            self.frame_reglas = None

        for t in self.tarjetas:
            t["frame"].destroy()
        self.tarjetas = []

        # Inicializacion de variables para el algoritmo
        self.n = len(self.pagos)
        self.dp = [0] * (self.n + 1)
        self.paso = 1

        # Creacion visual de las tarjetas por dia
        for i, p in enumerate(self.pagos):
            nombre = self.dias_semana[i] if i < len(self.dias_semana) else f"DIA {i+1}"
            card = tk.Frame(self.content_wrapper, bg=self.CARD_WHITE, width=160, height=200, 
                            highlightthickness=1, highlightbackground="#e2e8f0")
            card.pack_propagate(False)
            card.pack(side="left", padx=5)
            
            tk.Label(card, text=nombre, bg="#f8fafc", fg=self.TEXT_MUTE, font=("Segoe UI", 8, "bold")).pack(fill="x", ipady=8)
            tk.Label(card, text=f"${p}", bg=self.CARD_WHITE, fg=self.TEXT_MAIN, font=("Segoe UI", 24, "bold")).pack(expand=True)
            status_lbl = tk.Label(card, text="...", bg="#f1f5f9", fg=self.TEXT_MUTE, font=("Segoe UI", 7, "bold"))
            status_lbl.pack(fill="x", side="bottom")
            self.tarjetas.append({"frame": card, "status": status_lbl})

        self.btn_run.config(state="disabled", bg="#475569")
        self.animar()

    def animar(self):
        # Calcula la ganancia maxima acumulada mediante Programacion Dinamica
        if self.paso <= self.n:
            i = self.paso
            ayer = self.dp[i-1]
            antier = self.dp[i-2] if i > 1 else 0
            self.dp[i] = max(ayer, self.pagos[i-1] + antier)
            self.lbl_ganancia.config(text=f"${self.dp[i]}.00")
            self.tarjetas[i-1]["frame"].config(highlightbackground=self.ACCENT, highlightthickness=2)
            self.paso += 1
            self.ventana.after(150, self.animar)
        else:
            self.reconstruir()

    def reconstruir(self):
        # Backtracking: Determina que dias se trabajo basandose en la tabla DP calculada
        i = self.n
        while i > 0:
            pago_hoy = self.pagos[i-1]
            antier = self.dp[i-2] if i > 1 else 0
            
            if self.dp[i] == pago_hoy + antier:
                self.tarjetas[i-1]["frame"].config(bg="#fffbeb", highlightbackground=self.AMBER, highlightthickness=3)
                self.tarjetas[i-1]["status"].config(text="TRABAJAR", bg=self.AMBER, fg="white")
                
                if i > 1:
                    self.tarjetas[i-2]["status"].config(text="DESCANSO", bg="#f1f5f9", fg=self.TEXT_MUTE)
                
                i -= 2
            else:
                self.tarjetas[i-1]["status"].config(text="DESCANSO", bg="#f1f5f9", fg=self.TEXT_MUTE)
                i -= 1
        
        self.btn_run.config(state="normal", bg=self.EMERALD)

if __name__ == "__main__":
    root = tk.Tk()
    app = FreelancerFinalEdition(root)
    root.mainloop()