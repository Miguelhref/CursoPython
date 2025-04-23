import csv

file_path = "products.csv"
updated_file_path = "products_updated.csv"

with open("products.csv",mode="r") as archivo:
    csv_reader = csv.DictReader(archivo)

    #Obtener los nombres de las columnas existentes
    fieldnames = csv_reader.fieldnames+ ["total_value"]

    with open(updated_file_path,mode="w",newline= "") as archivo_actualizado:
        csv_writer = csv.DictWriter(archivo_actualizado,fieldnames=fieldnames)
        csv_writer.writeheader()

        for row in csv_reader:
             row["total_value"]=float(row["price"])*int(row["quantity"])
             csv_writer.writerow(row)

