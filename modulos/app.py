import reports

#Generar reportes de ventas y gastos usando funciones del modulo reports
sales_report = reports.generate_sales_report("Octubre",10000)
expenses_report = reports.generate_expenses_report("Octubre",5000)

print(sales_report)
print(expenses_report)