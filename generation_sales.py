import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Убираем фиксированное семя для большей случайности
# np.random.seed(42)
# random.seed(42)

# Параметры данных
regions = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 
           'Казань', 'Нижний Новгород', 'Ростов-на-Дону', 'Краснодар']
payment_methods = ['Наличные', 'Карта', 'Онлайн', 'Рассрочка']

# Реальные данные по категориям и поставщикам (без изменений)
categories_data = {
    'Процессоры': {
        'suppliers': ['Intel', 'AMD'],
        'products': [
            ('Intel Core i9-13900K', 'Intel', 65000, 80000),
            ('Intel Core i7-13700K', 'Intel', 45000, 60000),
            ('Intel Core i5-13600K', 'Intel', 30000, 40000),
            ('Intel Core i3-13100F', 'Intel', 15000, 22000),
            ('Intel Core i9-12900K', 'Intel', 50000, 65000),
            ('Intel Core i7-12700K', 'Intel', 35000, 48000),
            ('AMD Ryzen 9 7950X', 'AMD', 60000, 75000),
            ('AMD Ryzen 7 7700X', 'AMD', 35000, 50000),
            ('AMD Ryzen 5 7600X', 'AMD', 25000, 35000),
            ('AMD Ryzen 9 5900X', 'AMD', 30000, 45000),
            ('AMD Ryzen 7 5800X', 'AMD', 22000, 35000),
            ('AMD Ryzen 5 5600X', 'AMD', 15000, 25000)
        ]
    },
    'Видеокарты': {
        'suppliers': ['NVIDIA', 'AMD', 'ASUS', 'MSI', 'Gigabyte', 'Palit', 'Zotac'],
        'products': [
            ('ASUS ROG Strix RTX 4090', 'ASUS', 120000, 180000),
            ('MSI RTX 4090 Suprim X', 'MSI', 110000, 170000),
            ('Gigabyte RTX 4080 Gaming OC', 'Gigabyte', 90000, 120000),
            ('Zotac RTX 4080 AMP Extreme', 'Zotac', 85000, 115000),
            ('ASUS TUF RTX 4070 Ti', 'ASUS', 70000, 95000),
            ('Palit RTX 4070 Ti GameRock', 'Palit', 65000, 90000),
            ('MSI RTX 4060 Ti Gaming X', 'MSI', 40000, 55000),
            ('Gigabyte RTX 4060 Eagle', 'Gigabyte', 30000, 45000),
            ('ASUS RTX 3090 Ti ROG Strix', 'ASUS', 100000, 140000),
            ('MSI RTX 3080 Ti Suprim X', 'MSI', 80000, 110000),
            ('Zotac RTX 3070 Ti AMP Holo', 'Zotac', 50000, 70000),
            ('Palit RTX 3060 Ti Dual', 'Palit', 35000, 50000),
            ('ASUS Radeon RX 7900 XTX', 'ASUS', 80000, 110000),
            ('Gigabyte Radeon RX 7800 XT', 'Gigabyte', 60000, 85000),
            ('MSI Radeon RX 7700 XT', 'MSI', 45000, 65000),
            ('ASRock Radeon RX 7600', 'ASRock', 30000, 45000),
            ('ASUS Radeon RX 6950 XT', 'ASUS', 60000, 90000),
            ('Gigabyte Radeon RX 6800 XT', 'Gigabyte', 50000, 75000),
            ('MSI Radeon RX 6700 XT', 'MSI', 35000, 55000)
        ]
    },
    'Материнские платы': {
        'suppliers': ['ASUS', 'MSI', 'Gigabyte', 'ASRock'],
        'products': [
            ('ASUS ROG Maximus Z790 Hero', 'ASUS', 40000, 55000),
            ('MSI MPG Z790 Edge WiFi', 'MSI', 30000, 42000),
            ('Gigabyte Z790 Aorus Elite', 'Gigabyte', 25000, 38000),
            ('ASRock Z790 Pro RS', 'ASRock', 20000, 32000),
            ('ASUS ROG Crosshair X670E Hero', 'ASUS', 45000, 60000),
            ('MSI MAG B650 Tomahawk WiFi', 'MSI', 22000, 35000),
            ('Gigabyte B650 Aorus Elite AX', 'Gigabyte', 20000, 32000),
            ('ASRock B650E Steel Legend', 'ASRock', 18000, 30000),
            ('ASUS TUF Gaming B550-Plus', 'ASUS', 12000, 20000),
            ('MSI B450 Tomahawk Max', 'MSI', 8000, 15000)
        ]
    },
    'Оперативная память': {
        'suppliers': ['Kingston', 'Corsair', 'G.Skill', 'Crucial', 'Team Group'],
        'products': [
            ('Kingston Fury Beast 32GB DDR5-6000', 'Kingston', 10000, 15000),
            ('Corsair Vengeance 32GB DDR5-5600', 'Corsair', 12000, 17000),
            ('G.Skill Trident Z5 32GB DDR5-6400', 'G.Skill', 15000, 20000),
            ('Kingston Fury Renegade 32GB DDR4-3600', 'Kingston', 8000, 12000),
            ('Corsair Vengeance RGB Pro 32GB DDR4-3200', 'Corsair', 9000, 14000),
            ('G.Skill Ripjaws V 32GB DDR4-3600', 'G.Skill', 7000, 11000),
            ('Crucial Ballistix 32GB DDR4-3200', 'Crucial', 6000, 10000),
            ('Team Group T-Force Vulcan 16GB DDR4-3200', 'Team Group', 3000, 5000),
            ('Kingston ValueRAM 8GB DDR4-2666', 'Kingston', 2000, 3500)
        ]
    },
    'Накопители': {
        'suppliers': ['Samsung', 'Western Digital', 'Seagate', 'Kingston', 'Crucial'],
        'products': [
            ('Samsung 990 Pro 2TB NVMe', 'Samsung', 15000, 22000),
            ('WD Black SN850X 1TB NVMe', 'Western Digital', 8000, 12000),
            ('Seagate FireCuda 530 1TB NVMe', 'Seagate', 9000, 13000),
            ('Kingston KC3000 1TB NVMe', 'Kingston', 7000, 11000),
            ('Crucial P5 Plus 1TB NVMe', 'Crucial', 6000, 10000),
            ('Samsung 870 Evo 1TB SATA', 'Samsung', 5000, 8000),
            ('WD Blue 1TB SATA', 'Western Digital', 4000, 7000),
            ('Seagate IronWolf 4TB NAS', 'Seagate', 8000, 12000),
            ('WD Red Plus 4TB NAS', 'Western Digital', 9000, 13000)
        ]
    },
    'Блоки питания': {
        'suppliers': ['Corsair', 'Seasonic', 'be quiet!', 'Cooler Master', 'Chieftec'],
        'products': [
            ('Corsair RM1000x 1000W', 'Corsair', 15000, 22000),
            ('Seasonic Prime TX-1000 1000W', 'Seasonic', 18000, 25000),
            ('be quiet! Dark Power 13 1000W', 'be quiet!', 20000, 28000),
            ('Corsair RM850x 850W', 'Corsair', 12000, 18000),
            ('Seasonic Focus GX-850 850W', 'Seasonic', 13000, 19000),
            ('Cooler Master V850 Gold V2 850W', 'Cooler Master', 11000, 17000),
            ('Chieftec GPE-700S 700W', 'Chieftec', 5000, 9000),
            ('be quiet! System Power 9 600W', 'be quiet!', 4000, 8000)
        ]
    },
    'Корпуса': {
        'suppliers': ['NZXT', 'Fractal Design', 'Lian Li', 'Cooler Master', 'Deepcool'],
        'products': [
            ('NZXT H7 Elite Black', 'NZXT', 12000, 18000),
            ('Fractal Design Torrent RGB Black', 'Fractal Design', 15000, 22000),
            ('Lian Li PC-O11 Dynamic', 'Lian Li', 10000, 16000),
            ('Cooler Master MasterBox TD500 Mesh', 'Cooler Master', 8000, 13000),
            ('Deepcool CH510 Mesh', 'Deepcool', 5000, 9000),
            ('NZXT H510 Flow', 'NZXT', 7000, 11000),
            ('Fractal Design Focus G', 'Fractal Design', 4000, 8000)
        ]
    },
    'Охлаждение': {
        'suppliers': ['Noctua', 'Cooler Master', 'Corsair', 'be quiet!', 'Deepcool'],
        'products': [
            ('Noctua NH-D15', 'Noctua', 10000, 15000),
            ('be quiet! Dark Rock Pro 4', 'be quiet!', 8000, 13000),
            ('Deepcool AK620', 'Deepcool', 5000, 9000),
            ('Cooler Master Hyper 212 Black', 'Cooler Master', 3000, 6000),
            ('Corsair iCUE H150i Elite Capellix', 'Corsair', 15000, 22000),
            ('NZXT Kraken X73', 'NZXT', 14000, 20000),
            ('Lian Li Galahad AIO 360', 'Lian Li', 12000, 18000),
            ('Deepcool LS720', 'Deepcool', 9000, 15000)
        ]
    }
}

# Генерация артикулов
def generate_sku(category, supplier):
    prefix_map = {
        'Intel': 'INT',
        'AMD': 'AMD',
        'NVIDIA': 'NVD',
        'ASUS': 'ASUS',
        'MSI': 'MSI',
        'Gigabyte': 'GIG',
        'Kingston': 'KIN',
        'Corsair': 'COR',
        'G.Skill': 'GSK',
        'Crucial': 'CRU',
        'Samsung': 'SAM',
        'Western Digital': 'WD',
        'Seagate': 'SEA',
        'ASRock': 'ASR',
        'Noctua': 'NOC',
        'be quiet!': 'BQT',
        'Cooler Master': 'CM',
        'Seasonic': 'SEA',
        'NZXT': 'NZX',
        'Fractal Design': 'FRC',
        'Lian Li': 'LNL',
        'Palit': 'PAL',
        'Zotac': 'ZOT',
        'Team Group': 'TGR',
        'Chieftec': 'CHF',
        'Deepcool': 'DCL'
    }
    prefix = prefix_map.get(supplier, supplier[:3].upper())
    return f"{prefix}-{random.randint(1000, 9999)}"

# Генерация данных о товарах
products = []
for category, data in categories_data.items():
    for product_name, supplier, min_cost, max_cost in data['products']:
        cost = random.randint(min_cost, max_cost)
        price = round(cost * random.uniform(1.1, 1.5), 2)
        products.append({
            'SKU': generate_sku(category, supplier),
            'Category': category,
            'ProductName': product_name,
            'Supplier': supplier,
            'Cost': cost,
            'Price': price,
            'Warranty': random.choice([12, 24, 36])
        })

products_df = pd.DataFrame(products)

# Определяем веса для товаров на основе цены и категории
def get_product_weights(products_df):
    weights = []
    for _, row in products_df.iterrows():
        weight = 1.0
        if row['Price'] < 20000:
            weight *= 3.0
        elif row['Price'] < 50000:
            weight *= 1.5
        else:
            weight *= 0.5
        if row['Category'] in ['Видеокарты', 'Оперативная память']:
            weight *= 2.0
        weights.append(weight)
    return weights

# Генерация данных о продажах
sales_data = []
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

for _ in range(30000):
    product = products_df.sample(1, weights=get_product_weights(products_df)).iloc[0]
    date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    
    if product['Category'] in ['Видеокарты', 'Процессоры']:
        if product['Price'] > 100000:
            quantity = random.randint(1, 2)
        elif product['Price'] > 50000:
            quantity = random.randint(1, 4)
        else:
            quantity = random.randint(1, 6)
    else:
        quantity = random.randint(1, 8)
    
    if date.month in [11, 12]:
        quantity = min(quantity + random.randint(0, 3), 10)
    
    region_weights = [2.0 if region == 'Москва' and product['Price'] > 50000 else 1.0 for region in regions]
    region = random.choices(regions, weights=region_weights, k=1)[0]
    
    discount = np.clip(np.random.normal(0.05, 0.03), 0.0, 0.2)
    
    sales_data.append({
        'Date': date.date(),
        'SKU': product['SKU'],
        'Region': region,
        'Quantity': quantity,
        'PaymentMethod': random.choice(payment_methods),
        'TotalCost': product['Cost'] * quantity,
        'TotalPrice': product['Price'] * quantity,
        'Discount': discount
    })

sales_df = pd.DataFrame(sales_data)
sales_df['DiscountAmount'] = sales_df['TotalPrice'] * sales_df['Discount']
sales_df['FinalPrice'] = sales_df['TotalPrice'] - sales_df['DiscountAmount']
sales_df['Profit'] = sales_df['FinalPrice'] - sales_df['TotalCost']

# Добавляем столбцы месяца и квартала
sales_df['Month'] = pd.to_datetime(sales_df['Date']).dt.month_name()
sales_df['Quarter'] = 'Q' + pd.to_datetime(sales_df['Date']).dt.quarter.astype(str)

# Сохраняем данные с запятой как десятичным разделителем и точкой с запятой как разделителем столбцов
products_df.to_csv('products.csv', index=False, sep=';', decimal=',')
sales_df.to_csv('sales.csv', index=False, sep=';', decimal=',')
