# Streamlit Tasks App Con SqlAlchemy

**Aplicación de Tareas**

Aplicación de gestión de tareas, que tiene varias funciones como la de Crear, Editar, Eliminar y Buscar Tareas, también tiene la función tanto de importar desde un JSON como de exportar a un JSON las tareas. 

---

## Archivos Aplicativo

Los siguientes son los archivos del aplicativo y que contiene cada uno:

1. **database.py**: Me creará la respectiva base de datos en sqlite.
2. **main.py**: Contiene todas las funciones y también la lógica del streamlit.
3. **models.py**: Este archivo me creará la tabla en mi base de datos.
4. **requirements.txt**: Contiene las dependencias y paquetes necesarios para que la aplicación funcione.

---

## Librerías Usadas

Para el desarrollo de este aplicativo, se han utilizado las siguientes librerías:

1. **Streamlit**: Para construir la interfaz gráfica de usuario.
2. **SqlAlchemy**: Para cargar y mostrar imágenes en la interfaz.

---

## Imágenes del Aplicativo

### Pantalla Principal

![Pantalla Principal](/img/main_page.PNG)

- **Descripción:** Esta es la pantalla inicial de la aplicación, donde se pueden visualizar todas las tareas de la base de datos y a la izquierda un sidebar que contiene las funciones de importar y exportar las tareas.

![Barra Lateral](/img/sidebar.PNG)
- **Descripción:** En la barra lateral izquierda al darle al botón "Export Tasks" desplegará otro botón para descargar el JSON con todas las tareas. Para importar tareas desde un archivo ".json" daremos en el botón "Browse files" para buscar un archivo desde tu computadora. La siguiente imagen muestra el contenido que debe tener nuestro archivo JSON:

![Estructura Archivo para Importar JSON](/img/json_image.PNG)

### Agregar Tarea

![Agregar Tarea](/img/add_page.PNG)

- **Descripción:** Al presionar el botón "Add" se desplegará un formulario para agregar nuestra tarea a la base de datos.

### Editar Tarea

![Editar Tarea](/img/edit_page.PNG)

- **Descripción:** Para el botón "Edit" tendremos que proporcionar el "ID" de la tarea que queremos editar, al dar enter desplegará el formulario con los datos de dicha tarea.

### Buscar Tarea

![Buscar Tarea](/img/search_page.PNG)

- **Descripción:** En "Search" se podrá buscar tanto por el nombre de la tarea, cuerpo de la tarea y por estado de la tarea, ya sea poniendo "Pending" o "Completed".

### Eliminar Tarea

![Eliminar Tarea](/img/delete_page.PNG)

- **Descripción:** En "Delete" debemos proporcionar el "ID" de la tarea que desearemos eliminar.

---

## Cómo Ejecutar el Aplicativo

1. Clona este repositorio en tu máquina local.
   ```bash
   git clone https://github.com/JYupix/TasksApp.git
   ```
2. Crea un entorno virtual.
   ```bash
   python -m venv env
   ```
3. Y activalo de la siguiente manera.
   ```bash
   env/Scripts/activate
   ```
3. Luego Instala las dependencias necesarias.
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta el archivo principal.
   ```bash
   streamlit run main.py
   ```

---
