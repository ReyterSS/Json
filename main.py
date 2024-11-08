import csv
import json

# function to get data from json file
def load_data(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        return json.load(f)


# function to get minimum price and type of room
def find_min_price(prices):
    min_value = float('inf')
    min_key = None
    for i in prices:
        shown_price = i['shown_price']
        for key, value in shown_price.items():
            value_float = float(value)
            if value_float < min_value:
                min_value = value_float
                min_key = key
    return min_value, min_key

# function to get taxes and number of guests
def get_taxes_and_guests(number_of_quests):
    for i in number_of_quests:
        taxes = i["ext_data"]['taxes']
        taxes = json.loads(taxes)
        tax = taxes['TAX']
        city_tax = taxes["City tax"]
        number_of_guests = i['number_of_guests']
    return tax, city_tax, number_of_guests

# function to get price with taxes
def calculate_net_price(prices, tax, city_tax):
    result = []
    for i in prices:
        net_price = i["net_price"]
        for key, value in net_price.items():
            type_room = key
            net_price_taxes = '{:.2f}'.format(float(value) + float(tax) + float(city_tax))
            result.append({'Lowest price': type_room, 'Number of guests': net_price_taxes})
    return result

# function to write in csv file
def write_to_file(data, filename='Result.txt'):
    with open(filename, 'a', encoding='UTF-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writerows(data)

# main function
def main():
    # load data
    data = load_data('Python-task.json')
    prices = data['assignment_results']
    number_of_quests = data['assignment_results']
    # get minimum price and type of room
    min_value, min_key = find_min_price(prices)
    print(f"Minimum price: {min_value}")
    # getting taxes and number of guests
    tax, city_tax, number_of_guests = get_taxes_and_guests(number_of_quests)
    print(f"Type of room: '{min_key}', Number of guests: '{number_of_guests}'")
    # getting price with taxes
    net_price_data = calculate_net_price(prices, tax, city_tax)
    # write to csv file
    write_to_file(net_price_data)

if __name__ == '__main__':
    main()


