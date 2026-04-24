import tkinter as tk
from tkinter import messagebox

# ==========================================
# CLASE DE LOGICA (Motor de calculo)
# ==========================================
class OptimizacionFreelancer:
    def calcular_estrategia(self, pagos):
        n = len(pagos)
        dp = [0] * (n + 1)

        # Programacion Dinamica
        for i in range(1, n + 1):
            if i == 1:
                dp[i] = pagos[0]
            else:
                dp[i] = max(dp[i-1], pagos[i-1] + dp[i-2])

        # Backtracking
        decisiones = [False] * n
        i = n
        while i > 0:
            if i == 1:
                decisiones[0] = True
                break
            # Si el valor actual viene de trabajar (suma), marcamos True
            if dp[i] == pagos[i-1] + dp[i-2]:
                decisiones[i-1] = True
                i -= 2
            else:
                decisiones[i-1] = False
                i -= 1
        
        return dp, decisiones

# ==========================================
# CLASE DE INTERFAZ (UI)
# ==========================================
class Freelancer:
    def __init__(self, ventana):
        # Configuracion de la ventana
        self.ventana = ventana
        self.ventana.title("Freelancer")
        self.ventana.geometry("1350x850") 
        self.ventana.configure(bg="#f1f5f9") # Gris azulado muy claro 

        # Instancia del motor
        self.motor = OptimizacionFreelancer()

        # Definicion de paleta de colores
        self.NAVY = "#0f172a" # Azul marino oscuro
        self.ACCENT = "#3b82f6" # Azul brillante
        self.EMERALD = "#10b981" # Verde Esmeralda
        self.AMBER = "#f59e0b" # Dorado
        self.CARD_WHITE = "#ffffff" # Blanco
        self.TEXT_MAIN = "#1e293b" # Azul oscuro
        self.TEXT_MUTE = "#64748b" # Gris azulado

        # Variables de estado
        self.tarjetas = []
        self.pagos = []
        self.dp = []
        self.decisiones = [] 
        self.dias_semana = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO"]
        self.frame_reglas = None 
        self.paso = 0

        self.setup_ui()

    def setup_ui(self):
        # Barra Lateral
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

        tk.Frame(input_frame, bg=self.NAVY, height=120).pack() 

        tk.Label(input_frame, text="MONITOR DE LOGICA", fg="#94a3b8", bg=self.NAVY, 
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.log_text = tk.Text(input_frame, height=8, bg="#1e293b", fg="#94a3b8", 
                                font=("Consolas", 9), relief="flat", padx=10, pady=10, state="disabled")
        self.log_text.pack(fill="x")

        info_box = tk.Frame(sidebar, bg="#1e293b", pady=20, padx=20)
        info_box.pack(side="bottom", fill="x", padx=20, pady=(0, 40))
        
        metricas_texto = "Complejidad: O(n)\nHorario: Lun - Sab\nMetodo: Prog. Dinamica"
        tk.Label(info_box, text=metricas_texto, bg="#1e293b", fg="#94a3b8", 
                 font=("Consolas", 9), justify="left").pack(anchor="w")

        tk.Label(sidebar, text="METRICAS TECNICAS", fg="#94a3b8", bg=self.NAVY, 
                 font=("Segoe UI", 8, "bold")).pack(side="bottom", anchor="w", padx=20, pady=(0, 5))

        # Area Principal
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

    def escribir_log(self, texto):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, texto)
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def mostrar_reglas(self):
        self.frame_reglas = tk.Frame(self.content_wrapper, bg="white", padx=40, pady=40,
                                     highlightthickness=1, highlightbackground="#e2e8f0")
        self.frame_reglas.place(relx=0.5, rely=0.4, anchor="center")
        tk.Label(self.frame_reglas, text="COMO ORGANIZAR TU SEMANA", fg=self.ACCENT, bg="white", 
                 font=("Segoe UI", 14, "bold")).pack(pady=(0, 20))
        
        reglas = (
            "Bienvenido a Horario del Freelancer!\n\n"
            "Solo ingresa tus pagos diarios (separados por comas)\n"
            "y nosotros calculamos tu mejor plan de trabajo.\n\n"
            "Recuerda: Si trabajas un dia, el siguiente es descanso.\n"
            "El sistema elegira automaticamente los dias que\n"
            "mas dinero te dejen.\n\n"
            "Ingresa tus montos y presiona 'EJECUTAR ANALISIS'."
        )
        tk.Label(self.frame_reglas, text=reglas, fg=self.TEXT_MAIN, bg="white", 
                 font=("Segoe UI", 11), justify="left", wraplength=500).pack()

    def iniciar(self):
        # Validacion de entrada
        texto_entrada = self.entry_datos.get().strip()
        if not texto_entrada:
            messagebox.showwarning("Atencion", "Ingrese los pagos.")
            return

        try:
            self.pagos = [int(x.strip()) for x in texto_entrada.split(",") if x.strip()]
        except ValueError:
            messagebox.showerror("Error", "Use solo numeros y comas.")
            return

        # Llamada a la logica
        self.dp, self.decisiones = self.motor.calcular_estrategia(self.pagos)
        
        self.limpiar_pantalla()

        self.crear_tarjetas()

        self.btn_run.config(state="disabled")
        self.animar()

    def limpiar_pantalla(self):
        self.log_text.config(state="normal")
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state="disabled")

        if self.frame_reglas: self.frame_reglas.destroy()
        for t in self.tarjetas: t["frame"].destroy()
        self.tarjetas = []
        self.paso = 0

    def crear_tarjetas(self):
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
            self.tarjetas.append({"frame": card, "status": status_lbl, "valor": p})

    def animar(self):
        if self.paso < len(self.pagos):
            i = self.paso
            es_trabajo = self.decisiones[i]
            
            dp_prev = self.dp[i] 
            pago_actual = self.pagos[i]
            dp_prev_prev = self.dp[i-1] if i > 0 else 0
            
            if es_trabajo:
                razon = f"(${pago_actual}+{dp_prev_prev}) >= ${dp_prev}"
                texto_log = f"Dia {i+1}: Trabajo! {razon}\n"
                self.tarjetas[i]["frame"].config(bg="#fffbeb", highlightbackground=self.AMBER, highlightthickness=3)
                self.tarjetas[i]["status"].config(text="TRABAJAR", bg=self.AMBER, fg="white")
            else:
                razon = f"${dp_prev} > ${pago_actual}+{dp_prev_prev}"
                texto_log = f"Dia {i+1}: Descanso. {razon}\n"
                self.tarjetas[i]["frame"].config(bg="#eff6ff", highlightbackground=self.ACCENT, highlightthickness=3)
                self.tarjetas[i]["status"].config(text="DESCANSO", bg=self.ACCENT, fg="white")
            
            self.escribir_log(texto_log)
            self.paso += 1
            self.ventana.after(500, self.animar)
        else:
            self.escribir_log("--- Analisis Finalizado ---\n")
            self.lbl_ganancia.config(text=f"${self.dp[len(self.pagos)]}.00")
            self.btn_run.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = Freelancer(root)
    root.mainloop()