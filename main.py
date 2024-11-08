import json
import csv


# function to get data from json file
def load_data(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        return json.load(f)


# function to get minimum price and type of room
def find_min_price(prices):
    min_value = float('inf')
    min_key = None
    for price_info in prices:
        for room_type, price in price_info['shown_price'].items():
            price = float(price)
            if price < min_value:
                min_value = price
                min_key = room_type
    return min_value, min_key


# function to get taxes and number of guests
def get_taxes_and_guests(data):
    taxes = json.loads(data[0]["ext_data"]['taxes'])
    tax = float(taxes['TAX'])
    city_tax = float(taxes["City tax"])
    number_of_guests = data[0]['number_of_guests']
    return tax, city_tax, number_of_guests


# function to get full price (net price + taxes) for each room
def calculate_net_price(prices, tax, city_tax):
    result = []
    for price_info in prices:
        for room_type, net_price in price_info["net_price"].items():
            total_price = float(net_price) + tax + city_tax
            result.append({'Room Type': room_type, 'Total Price': '{:.2f}'.format(total_price)})
    return result


# function to write in csv file
def write_to_file(data, filename):
    with open(filename, 'w', encoding='UTF-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


# main function
def main():
    # load data
    data = load_data('Python-task.json')
    prices = data['assignment_results']

    # get minimum price and type of room
    min_value, min_key = find_min_price(prices)
    print(f"Minimum price: {min_value}")
    print(f"Room type with the minimum price: '{min_key}'")

    # getting taxes and number of guests
    tax, city_tax, number_of_guests = get_taxes_and_guests(prices)
    print(f"Number of guests: {number_of_guests}")

    # getting price with taxes for all rooms
    net_price_data = calculate_net_price(prices, tax, city_tax)

    # write to csv file
    output_filename = 'Result.csv'
    write_to_file(net_price_data, output_filename)


if __name__ == '__main__':
    main()