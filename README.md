# SEC 1
## Miembros del equipo
- Arnaiz, Rodrigo
- Blum, Ariel
- Castro, Joaquin
- Morillo Meneses, Alen
- Romero, Tomas

 ## Herramientas usadas:
 - Python: 3.8.10
 - Django: 4.1.1


## Instalacion: 
1. Clonar el repositorio:
  `git clone https://github.com/UNPSJB/Sec1.git`
2. Crear el entorno virtual en el mismo directorio donde esta el repositorio:
   `python3 -m venv <nombre del entorno virtual> `
3. Activar el entorno virtual: `Scripts <nombre del entorno virtual>/Scripts/activate`
4. Ingresar al proyecto mediante: `cd sources/`
5. Instalar la carpeta requerimientos.txt que se encuentra dentro de la carpeta sources: `pip install -r requirements.txt`
6. Ingresar a la carpeta sec: `cd sources/sec/`
7. Realizar las migraciones:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
8. Crear un superusuario: `python manage.py createsuperuser`
9. Ejecutar el proyecto: `python manage.py runserver`
10. Loguearse.
