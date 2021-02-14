# Scrapper de métros cúbicos.

Para hacer scrapping en python3:

		python3 adventure.py <items to scrap>
		
Si omites <items to scrap>, o no corresponde con un valor numérico entero, utilizará el default.

El scrapper crea "homes.db", y una carpeta con imágenes de las casas, la bd tiene la siguiente estructura:

1. houses
1. id (Primary key)
2. tipo de propiedad
3. precio
4. dirección
5. ciudad
6. estado
7. país
8. descripción
9. amenidades
10. terreno
11. número de recámaras
12. número de baños
13. ruta de la imagen

# Cargar los datos a dataframe de pandas


		from importer import import_houses
		
import_houses() regresa un dataframe de pandas listo para análsis.
