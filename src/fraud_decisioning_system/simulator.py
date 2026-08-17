import numpy as np
import pandas as pd

def generate_customers(n_customers: int, seed: int = 42) -> pd.DataFrame:
    """
    Generate a DataFrame of customers with random attributes.

    Args:
        n_customers (int): Number of customers to generate.
        seed (int): Random seed for reproducibility.

    Columns:
        - customer_id (str): Unique identifier for the customer.
        - avg_amount (float): Average transaction amount for the customer. use right skewed distribution to generate this value.
        - active_hour (int): the most active hour of the customer, use normal distribution to generate this value, center around 2pm (14) with a range of 0-23.
        - home_merchant_category (str): The most frequently bought merchant category for the customer. Select from [
            'grocery', 'restaurant', 'online retail', 'gas', 'travel', 'electronics'].
    Returns:
        pd.DataFrame: DataFrame containing customer attributes.
    """
    rng = np.random.default_rng(seed)
    customer_ids = [f"C{i:05d}" for i in range(n_customers)]
    avg_amounts = rng.lognormal(mean=4, sigma=1, size=n_customers)  # Right-skewed distribution
    active_hours = np.clip(rng.normal(14, 5, size=n_customers).round(), 0, 23).astype(int)
    merchant_categories = rng.choice(
        ['grocery', 'restaurant', 'online retail', 'gas', 'travel', 'electronics'],
        size=n_customers
    )
    return pd.DataFrame({
        'customer_id': customer_ids,
        'avg_amount': avg_amounts,
        'active_hour': active_hours,
        'home_merchant_category': merchant_categories
    })

def generate_merchants(n_merchants: int, seed: int = 43) -> pd.DataFrame:
    """
    Generate a DataFrame of merchants with random attributes.

    Args:
        n_merchants (int): Number of merchants to generate.
        seed (int): Random seed for reproducibility.

    Columns:
        - merchant_id (str): Unique identifier for the merchant. e.g.: M00001, M00002, ...
        - fraud_prone: 5% of merchants are fraud-prone, 95% are not. Use a Bernoulli distribution to generate this value.
        - merchant_category (str): The category of the merchant. Select from [
            'grocery', 'restaurant', 'online retail', 'gas', 'travel', 'electronics'].
        - avg_transaction_amount (float): Average transaction amount for the merchant. use right skewed distribution to generate this value.
    Returns:
        pd.DataFrame: DataFrame containing merchant attributes.
    """
    rng = np.random.default_rng(seed)
    merchant_ids = [f"M{i:05d}" for i in range(n_merchants)]
    merchant_categories = rng.choice(
        ['grocery', 'restaurant', 'online retail', 'gas', 'travel', 'electronics'],
        size=n_merchants
    )
    fraud_prone = rng.binomial(n=1, p=0.05, size = n_merchants).astype(bool)
    avg_transaction_amounts = rng.lognormal(mean=4, sigma=1, size=n_merchants)  # Right-skewed distribution
    return pd.DataFrame({
        'merchant_id': merchant_ids,
        'fraud_prone': fraud_prone,
        'merchant_category': merchant_categories,
        'avg_transaction_amount': avg_transaction_amounts
    })

def generate_cards(customers: pd.DataFrame, seed:int=44) -> pd.DataFrame:
    """
    Generate a DataFrame of cards for each customer.

    Args:
        customers (pd.DataFrame): DataFrame containing customer attributes.
        seed (int): Random seed for reproducibility.

    Columns:
        - card_id (str): Unique identifier for the card. every customers have 1-3 cards.
        - card_id "CARD00001" is for customer_id "C00001", "CARD00002" is for customer_id "C00001", "CARD00003" is for customer_id "C00001", "CARD00004" is for customer_id "C00002", ...
        - customer_id (str): The ID of the customer who owns the card.

    """
    rng = np.random.default_rng(seed)
    card_ids = []
    customer_ids = []
    count = rng.integers(1, 4, size=len(customers))  # Each customer has 1-3 cards
    customer_ids = np.repeat(customers['customer_id'], count) # what does it mean? it means that for each customer_id, we will repeat it count[i] times, where count[i] is the number of cards for that customer. For example, if customer_id "C00001" has 2 cards, then "C00001" will appear twice in the customer_ids list.
    card_ids = [f"CARD{i+1:05d}" for i in range(len(customer_ids))] # generate card_ids based on the length of customer_ids
    # for customer_id in customers['customer_id']:
    #     n_cards = rng.integers(1, 4) # Each customer has 1-3 cards
    #     for _ in range(n_cards):
    #         card_ids.append(f"CARD{len(card_ids)+1:05d}")
    #         customer_ids.append(customer_id)
    return pd.DataFrame({
        'card_id': card_ids,
        'customer_id': customer_ids
    })

def generate_devices(customers: pd.DataFrame, seed: int = 45) -> pd.DataFrame:
    """
    Generate a DataFrame of devices for each customer.

    Args:
        customers (pd.DataFrame): DataFrame containing customer attributes.
        seed (int): Random seed for reproducibility.

    Columns:
        - device_id (str): Unique identifier for the device. every customers have 1-2 devices.
        - device_id "DEVICE00001" is for customer_id "C00001", "DEVICE00002" is for customer_id "C00001"
        - customer_id (str): The ID of the customer who owns the device.

    """
    rng = np.random.default_rng(seed)
    device_ids = []
    customer_ids = []
    count = rng.integers(1, 3, size=len(customers))  # Each customer has 1-2 devices
    customer_ids = np.repeat(customers['customer_id'], count)
    device_ids = [f"DEVICE{i+1:05d}" for i in range(len(customer_ids))]
    return pd.DataFrame({
        'device_id': device_ids,
        'customer_id': customer_ids
    })

if __name__ == "__main__":
    df = generate_customers(1000)
    print(df.head(10))
    print(df["avg_amount"].describe())
    df_merchants = generate_merchants(100)
    df_cards = generate_cards(df)
    df_devices = generate_devices(df)
    print(f"customers: {len(df)}, merchants: {len(df_merchants)}, "
      f"cards: {len(df_cards)}, devices: {len(df_devices)}")
    print(df_cards["customer_id"].value_counts().describe())  