from reports import generate_sales_report
from reports import calculate_balance
from reports import calculate_balance_mes
print(generate_sales_report("Noviembre",7000))

meses = [
    {"mes":"Enero","ingresos":5000,"gastos":3000},
    {"mes":"Febrero","ingresos":10000,"gastos":11000},
    {"mes":"Marzo","ingresos":6000,"gastos":5000},
    {"mes":"Abril","ingresos":5000,"gastos":6000},
    {"mes":"Mayo","ingresos":5000,"gastos":2000},
 
]

calculate_balance(meses)