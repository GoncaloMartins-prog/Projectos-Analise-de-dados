import pandas as pd
import numpy as np
from faker import Faker  # Para gerar nomes e cidades fictícias

# Configuração
np.random.seed(42)  # Para resultados reproduzíveis
fake = Faker('pt_PT')  # Dados em português de Portugal

# --- Gerar customers.csv ---
num_customers = 100
customers = pd.DataFrame({
    'customer_id': np.arange(1, num_customers + 1),
    'name': [fake.name() for _ in range(num_customers)],
    'age': np.random.randint(18, 70, size=num_customers),
    'gender': np.random.choice(['M', 'F'], size=num_customers),
    'city': [fake.city() for _ in range(num_customers)]
})

# --- Gerar sales_data.csv ---
num_orders = 1000
products = ['P' + str(i).zfill(3) for i in range(1, 21)]  # P001 a P020

sales = pd.DataFrame({
    'order_id': np.arange(1, num_orders + 1),
    'customer_id': np.random.choice(customers['customer_id'], size=num_orders),
    'product_id': np.random.choice(products, size=num_orders),
    'order_date': pd.date_range(start='2023-01-01', periods=num_orders, freq='D'),
    'quantity': np.random.randint(1, 10, size=num_orders),
    'unit_price': np.round(np.random.uniform(5, 100, size=num_orders), 2)
})

# Calcular total_price
sales['total_price'] = sales['quantity'] * sales['unit_price']

# Introduzir alguns valores ausentes (opcional)
sales.loc[np.random.choice(sales.index, size=20), 'quantity'] = np.nan

# --- Salvar como CSV ---
customers.to_csv('customers.csv', index=False)
sales.to_csv('sales_data.csv', index=False)

print("Arquivos gerados: 'customers.csv' e 'sales_data.csv'")
