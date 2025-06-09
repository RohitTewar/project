import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
try:
    df = pd.read_csv('sample_sales_data.csv', parse_dates=['Date'])
except FileNotFoundError:
    print("❌ File not found. Make sure 'sales_data.csv' is in the same folder.")
    exit()

# Add additional useful columns
df['Month'] = df['Date'].dt.to_period('M')
df['Week'] = df['Date'].dt.isocalendar().week
df['Day'] = df['Date'].dt.day_name()

# 📊 1. Total Revenue Over Time

daily_revenue = df.groupby('Date')['Total Revenue'].sum()
daily_revenue.plot(kind='line', title='Daily Revenue Trend', figsize=(10, 5))
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.grid(True) # Add grid for better readability
plt.tight_layout()
plt.show()

# 🥇 2. Top-Selling Products

top_products = df.groupby('Product')['Units Sold'].sum().sort_values(ascending=False).head(5)
top_products.plot(kind='bar', title='Top 5 Products Sold', figsize=(8, 4))
plt.ylabel('Units Sold')
plt.tight_layout()
plt.show()

# 🧾 3. Payment Method Share

payment_share = df['Payment Method'].value_counts()
payment_share.plot(kind='pie', autopct='%1.1f%%', title='Payment Method Distribution', figsize=(6, 6))
plt.ylabel('')
plt.tight_layout()
plt.show()

# 🔥 4. Heatmap of Day-of-Week Sales

heatmap_data = df.groupby(['Day', 'Category'])['Total Revenue'].sum().unstack()
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title('Revenue Heatmap: Day vs Category')
plt.tight_layout()
plt.show()
