#Genera un informe de venas para un mes especifico
def generate_sales_report(month, sales):
    return f"Sales Report - {month}: Total sales: ${sales}"

#Genera un informe de gastos para un mes especifico

def generate_expenses_report(month, expenses):
    return f"Expenses report - {month}: Total expenses ${expenses}"

def calculate_balance_mes(income, expenses):
    return income > expenses

def calculate_balance(meses):
    for mes in meses:
        
        print(f"{mes["mes"]} ha sido beneficioso? {calculate_balance_mes(mes["ingresos"],mes["gastos"])}")