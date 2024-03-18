import os
import re
from collections import defaultdict

def extract_dependencies_from_manifest(manifest_file, current_directory, dependencies_dict):
    if not os.path.isfile(manifest_file):
        print(f"El archivo {manifest_file} no existe.")
        return
    
    # Leer el contenido del archivo
    with open(manifest_file, 'r') as f:
        manifest_content = f.read()

    # Buscar las dependencias dentro del contenido del archivo
    match = re.search(r'"depends"\s*:\s*\[\s*([^\]]+)\s*\]', manifest_content)
    if match:
        dependencies_text = match.group(1)
        dependencies = re.findall(r'"([^"]+)"', dependencies_text)
        for dependency in dependencies:
            # Verificar si la dependencia es otro módulo en la misma carpeta
            dependency_path = os.path.join(current_directory, dependency)
            if os.path.isdir(dependency_path):
                dependencies_dict[dependency] += 1
                # Imprimir las dependencias del módulo dependiente
                print("\t", dependency)
                dependency_manifest = os.path.join(dependency_path, "__manifest__.py")
                extract_dependencies_from_manifest(dependency_manifest, dependency_path, dependencies_dict)

# Directorio donde se ejecuta el script
current_directory = os.getcwd()

# Diccionario para almacenar las dependencias y su cantidad de dependientes
dependencies_dict = defaultdict(int)

# Obtener la lista de archivos en el directorio actual y ordenarla
files = os.listdir(current_directory)
files.sort()

# Iterar sobre los archivos ordenados
for file in files:
    manifest_file = os.path.join(current_directory, file, "__manifest__.py")
    if os.path.isfile(manifest_file):
        print(f"\nMódulo: {file}")
        extract_dependencies_from_manifest(manifest_file, current_directory, dependencies_dict)

# Imprimir el número total de dependientes para cada módulo
print("\nNúmero total de dependientes para cada módulo:")
for module, dependents in dependencies_dict.items():
    print(f"{module}: {dependents} dependiente(s)")
