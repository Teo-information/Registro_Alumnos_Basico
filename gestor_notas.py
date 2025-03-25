import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
# Conectar con MySQL
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",   
        password="12345", 
        database="gestor_notas"
    )

try:
    conn = conectar()
    print("Conexión exitosa a MySQL")
except mysql.connector.Error as err:
    print(f"Error: {err}")

# Función para agregar una nota
def agregar_nota():
    estudiante = entrada_nombre.get()
    nota = entrada_nota.get()

    if estudiante and nota:
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO notas (estudiante, nota) VALUES (%s, %s)", (estudiante, nota))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Nota agregada correctamente")
            entrada_nombre.delete(0, tk.END)
            entrada_nota.delete(0, tk.END)
            entrada_nombre.focus()
            mostrar_notas() 
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la nota: {str(e)}")
    else:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

# Función para mostrar todas las notas
def mostrar_notas():
    for row in tabla.get_children():
        tabla.delete(row)  # Limpiar la tabla

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM notas")
    for fila in cursor.fetchall():
        tabla.insert("", "end", values=fila)
    conexion.close()

# Función para eliminar una nota
def eliminar_nota():
    try:
        item = tabla.selection()[0]
        id_nota = tabla.item(item, "values")[0]
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM notas WHERE id = %s", (id_nota,))
        conexion.commit()
        conexion.close()
        tabla.delete(item)
        messagebox.showinfo("Éxito", "Nota eliminada correctamente")
        entrada_nombre.delete(0, tk.END)
        entrada_nota.delete(0, tk.END)
    except IndexError:
        messagebox.showwarning("Advertencia", "Selecciona una nota para eliminar")

# Función para actualizar una nota
def editar_nota():
    """Selecciona una fila y permite modificar los valores en los Entry antes de guardarlos."""
    try:
        item = tabla.selection()[0]
        valores = tabla.item(item, "values")

        # Verificar si los Entry ya tienen valores
        if not entrada_nombre.get() and not entrada_nota.get():
            # Insertar los valores en los Entry para edición
            entrada_nombre.delete(0, tk.END)
            entrada_nombre.insert(0, valores[1])  # Columna "Estudiante"

            entrada_nota.delete(0, tk.END)
            entrada_nota.insert(0, valores[2])  # Columna "Nota"
        
        else:
            # Si los Entry ya tienen valores, entonces actualiza la base de datos
            nueva_nota = entrada_nota.get()

            if nueva_nota:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("UPDATE notas SET nota = %s WHERE id = %s", (nueva_nota, valores[0]))
                conexion.commit()
                conexion.close()
                messagebox.showinfo("Éxito", "Nota actualizada correctamente")
                mostrar_notas()

                # Limpiar los Entry después de la edición
                entrada_nombre.delete(0, tk.END)
                entrada_nota.delete(0, tk.END)

            else:
                messagebox.showwarning("Advertencia", "Ingresa una nueva nota")

    except IndexError:
        messagebox.showwarning("Advertencia", "Selecciona una nota para editar")



def confirmar_cierre():
    respuesta = messagebox.askyesno("Confirmación", "¿Desea salir del registro?")
    if respuesta:
        ventana.destroy() 
        
# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Notas")
ventana.geometry("700x420")
ventana.resizable(0, False) 
ventana.configure(bg="#c6d9e3")
ventana.iconbitmap(r"C:\ArchivoPadreTeo\Recursos de la web\PYTHON TAREAS\GESTOR DE NOTAS\iconos\lapiz.ico")
ventana.protocol("WM_DELETE_WINDOW", confirmar_cierre)


ancho_ventana = 700
alto_ventana = 420
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

pos_x = (ancho_pantalla // 2) - (ancho_ventana // 2)
pos_y = (alto_pantalla // 2) - (alto_ventana // 2)
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
# Marco formulario 3D
frame_formulario = tk.Frame(ventana, bg="#c6d9e3", bd=5, relief="ridge")
frame_formulario.place(x=20, y=80, width=300, height=300)

# Título 
tk.Label(
    ventana, 
    text="Registro de Notas", 
    font=("Algerian", 20, "bold"), 
    fg="blue",
    bg="#c6d9e3",
    bd=3
).place(x=180, y=20)

# Etiquetas y entradas 
tk.Label(frame_formulario, text="Nombre del estudiante", font=("Consolas", 13, "bold"), fg="black", bg="#c6d9e3").place(x=30, y=10)
entrada_nombre = tk.Entry(frame_formulario, bd=3, relief="sunken")
entrada_nombre.place(x=30, y=40, width=200 ,height=25)
entrada_nombre.focus()

tk.Label(frame_formulario, text="Nota", font=("Consolas", 12, "bold"), fg="black", bg="#c6d9e3").place(x=30, y=70)
entrada_nota = tk.Entry(frame_formulario, bd=3, relief="sunken")
entrada_nota.place(x=30, y=100, width=200 ,height=25)

#Imagenes
imagenes = {
    "agregar": PhotoImage(file=r"C:\ArchivoPadreTeo\Recursos de la web\PYTHON TAREAS\GESTOR DE NOTAS\iconos\agregar.png"),
    "editar": PhotoImage(file=r"C:\ArchivoPadreTeo\Recursos de la web\PYTHON TAREAS\GESTOR DE NOTAS\iconos\nota.png"),
    "eliminar": PhotoImage(file=r"C:\ArchivoPadreTeo\Recursos de la web\PYTHON TAREAS\GESTOR DE NOTAS\iconos\portapapeles.png")
}


# Botones con Imagenes
tk.Button( text="Agregar", font=("Agency FB", 12), image=imagenes["agregar"], compound="top", bd=3, command=agregar_nota).place(x=55, y=280)
tk.Button( text=" Editar ", font=("Agency FB", 12), image=imagenes["editar"], compound="top", bd=3, command=editar_nota).place(x=135, y=280)
tk.Button( text="Eliminar", font=("Agency FB", 12), image=imagenes["eliminar"], compound="top", bd=3, command=eliminar_nota).place(x=215, y=280)

# Tabla 
frame_tabla = tk.Frame(ventana, bd=5, relief="ridge", bg="white")
frame_tabla.place(x=350, y=90, width=310, height=220)

columnas = ("ID", "Estudiante", "Nota")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

tabla.heading("ID", text="ID", anchor="center")
tabla.heading("Estudiante", text="Estudiante", anchor="center")
tabla.heading("Nota", text="Nota", anchor="center")

tabla.column("ID", width=50, anchor="center") 
tabla.column("Estudiante", width=150, anchor="center") 
tabla.column("Nota", width=80, anchor="center")  

tabla.pack(fill="both", expand=True)


# Mostrar las notas al iniciar
mostrar_notas()

# Ejecutar la ventana
ventana.mainloop()
