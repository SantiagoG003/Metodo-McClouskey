import tkinter as tk  
from tkinter import messagebox 

# Clase que contiene el algoritmo Quine-McCluskey para la simplificación booleana
class QuineMcCluskey:
    def __init__(self, minterminos, no_importa=None):
        # Inicializamos la clase con los minterms (minterminos) y las condiciones "no importa"
        if no_importa is None:
            no_importa = []
        # Eliminamos duplicados y ordenamos los minterminos y "no importa"
        self.minterminos = sorted(set(minterminos))
        self.no_importa = sorted(set(no_importa))
        # Combinamos ambos conjuntos de términos
        self.todos_terminos = self.minterminos + self.no_importa
        # Calculamos la cantidad de bits necesarios para representar los términos
        self.num_bits = len(format(max(self.todos_terminos), 'b')) if self.todos_terminos else 0
        self.grupos = {}  # Diccionario para almacenar los grupos de términos
        self.implicantes_primos = []  # Lista para almacenar los implicantes primos
        self.pasos = []  # Lista para almacenar los pasos del algoritmo

    # Método que ejecuta el algoritmo completo
    def ejecutar_algoritmo(self):
        self.agrupar_terminos()  # Agrupa los términos por el número de 1's en su representación binaria
        self.combinar_terminos()  # Combina términos que difieren en un solo bit
        self.encontrar_implicantes_primos()  # Encuentra los implicantes primos esenciales

    # Agrupa los términos por el número de 1's en su representación binaria
    def agrupar_terminos(self):
        todos_terminos = self.minterminos + self.no_importa  # Combina los minterminos y los "no importa"
        self.grupos = {i: [] for i in range(self.num_bits + 1)}  # Crea grupos basados en el número de bits en 1

        for termino in todos_terminos:
            binario = format(termino, f'0{self.num_bits}b')  # Convierte el término en binario
            cantidad_unos = binario.count('1')  # Cuenta la cantidad de 1's en el binario
            # Añade el término al grupo correspondiente según la cantidad de 1's
            self.grupos[cantidad_unos].append({'terminos': [termino], 'binario': binario, 'combinado': False})

        self.pasos.append("Grupos Iniciales:")  # Registra los grupos iniciales en los pasos
        for cantidad, grupo in self.grupos.items():
            for termino in grupo:
                self.pasos.append(f"{termino['binario']} -> {termino['terminos']}")

    # Método para combinar términos que difieren en solo un bit
    def combinar_terminos(self):
        contador_pasos = 1  # Contador de pasos de combinación
        while True:
            combinado = False  # Bandera para verificar si se realizó alguna combinación
            nuevos_grupos = {}  # Diccionario para los nuevos grupos tras la combinación
            llaves = sorted(self.grupos.keys())  # Ordena los grupos por cantidad de 1's

            self.pasos.append(f"\nPaso {contador_pasos}: Combinaciones\n")  # Agrega el paso a los registros

            for i in range(len(llaves) - 1):
                grupo1 = self.grupos[llaves[i]]  # Grupo con menos 1's
                grupo2 = self.grupos[llaves[i + 1]]  # Grupo con más 1's

                for termino1 in grupo1:
                    for termino2 in grupo2:
                        # Compara dos términos que difieren en solo un bit
                        if self.diferentes_bits(termino1['binario'], termino2['binario']) == 1:
                            combinado = True  # Marca que se hizo una combinación
                            # Combina los términos en uno solo con un guion en la posición del bit diferente
                            binario_combinado = self.combinar_binarios(termino1['binario'], termino2['binario'])
                            terminos = sorted(set(termino1['terminos'] + termino2['terminos']))  # Une los minterminos combinados
                            cantidad_unos = binario_combinado.count('1')  # Cuenta los 1's del binario combinado

                            # Crea un nuevo grupo para el término combinado
                            if cantidad_unos not in nuevos_grupos:
                                nuevos_grupos[cantidad_unos] = []
                            nuevos_grupos[cantidad_unos].append({'terminos': terminos, 'binario': binario_combinado, 'combinado': False})

                            self.pasos.append(f"{termino1['binario']} + {termino2['binario']} -> {binario_combinado} -> {terminos}")

                            # Marca ambos términos originales como combinados
                            termino1['combinado'] = termino2['combinado'] = True

            # Almacena los términos que no fueron combinados como implicantes primos
            for grupo in self.grupos.values():
                for termino in grupo:
                    if not termino['combinado'] and termino not in self.implicantes_primos:
                        self.implicantes_primos.append(termino)

            if not combinado:  # Si no se realizaron combinaciones, termina el ciclo
                break

            self.grupos = nuevos_grupos  # Actualiza los grupos con los términos combinados
            contador_pasos += 1  # Incrementa el contador de pasos

    # Encuentra los implicantes primos esenciales
    def encontrar_implicantes_primos(self):
        # Crea una tabla de cobertura para los minterminos
        tabla_cobertura = {m: [] for m in self.minterminos}
        for implicante in self.implicantes_primos:
            for mintermino in implicante['terminos']:
                if mintermino in self.minterminos:
                    tabla_cobertura[mintermino].append(implicante)

        implicantes_esenciales = []
        # Busca implicantes esenciales cubriendo minterminos que no han sido cubiertos
        while tabla_cobertura:
            for mintermino, implicantes in tabla_cobertura.items():
                if len(implicantes) == 1:
                    implicante_esencial = implicantes[0]
                    if implicante_esencial not in implicantes_esenciales:
                        implicantes_esenciales.append(implicante_esencial)
                    # Elimina los minterminos cubiertos por el implicante esencial de la tabla
                    for mintermino_cubierto in implicante_esencial['terminos']:
                        tabla_cobertura.pop(mintermino_cubierto, None)
                    break
            else:
                break

        self.implicantes_esenciales = implicantes_esenciales  # Almacena los implicantes esenciales

    # Devuelve el número de bits que difieren entre dos términos
    def diferentes_bits(self, b1, b2):
        return sum(bit1 != bit2 for bit1, bit2 in zip(b1, b2))

    # Combina dos binarios en un solo término con '-' donde los bits difieren
    def combinar_binarios(self, b1, b2):
        return ''.join(bit1 if bit1 == bit2 else '-' for bit1, bit2 in zip(b1, b2))

    # Genera la expresión booleana simplificada
    def obtener_resultados(self):
        variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'][:self.num_bits]  # Variables según la cantidad de bits
        expresion = []

        for implicante in self.implicantes_esenciales:
            termino = []
            for i, bit in enumerate(implicante['binario']):
                if bit == '1':
                    termino.append(variables[i])  # Si el bit es 1, se usa la variable
                elif bit == '0':
                    termino.append(f"{variables[i]}'")  # Si el bit es 0, se usa la negación de la variable
            expresion.append(''.join(termino))

        return ' + '.join(expresion)  # Devuelve la expresión simplificada


# Clase para la interfaz gráfica usando Tkinter
class AplicacionMcCluskey:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Reducción de McCluskey")

        self.etiqueta_minterminos = tk.Label(raiz, text="Ingresa los minterminos separados por comas:")
        self.etiqueta_minterminos.pack()

        self.entrada_minterminos = tk.Entry(raiz)
        self.entrada_minterminos.pack()

        self.boton_ejecutar = tk.Button(raiz, text="Iniciar reducción", command=self.ejecutar_mccluskey)
        self.boton_ejecutar.pack()

        self.texto_resultados = tk.Text(raiz, height=20, width=60)
        self.texto_resultados.pack()

    def ejecutar_mccluskey(self):
        try:
            minterminos = [int(termino.strip()) for termino in self.entrada_minterminos.get().split(',') if termino.strip().isdigit()]
            if not minterminos:
                messagebox.showerror("Error", "Por favor, introduce al menos un mintermino válido.")
                return
            qmc = QuineMcCluskey(minterminos)
            qmc.ejecutar_algoritmo()
            resultados = qmc.obtener_resultados()
            self.mostrar_resultados(qmc, resultados)
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce números válidos.")

    def mostrar_resultados(self, qmc, resultados):
        self.texto_resultados.delete(1.0, tk.END)

        self.texto_resultados.insert(tk.END, "Implicantes Primos:\n")
        for implicante in qmc.implicantes_primos:
            terminos = ','.join(map(str, implicante['terminos']))
            self.texto_resultados.insert(tk.END, f"{implicante['binario']} -> {terminos}\n")

        self.texto_resultados.insert(tk.END, "\nPasos de la reducción:\n")
        for paso in qmc.pasos:
            self.texto_resultados.insert(tk.END, f"{paso}\n")

        self.texto_resultados.insert(tk.END, "\nExpresión Booleana Simplificada:\n")
        self.texto_resultados.insert(tk.END, f"{resultados}\n")

# Ejecuta la aplicación
if __name__ == "__main__":
    raiz = tk.Tk()
    aplicacion = AplicacionMcCluskey(raiz)
    raiz.mainloop()
