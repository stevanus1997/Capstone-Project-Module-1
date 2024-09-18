import os

products = [
    {
        "barcode_id": "8801234567890",
        "name": "Rice",
        "category": "Groceries",
        "quantity": 20,
        "price": 12000,  # per kilogram
        "location": "Shelf 1, Row 2"
    },
    {
        "barcode_id": "8800987654321",
        "name": "Cooking Oil",
        "category": "Oil",
        "quantity": 50,
        "price": 28000,  # per liter
        "location": "Shelf 2, Row 1"
    },
    {
        "barcode_id": "8801357924680",
        "name": "Sugar",
        "category": "Groceries",
        "quantity": 75,
        "price": 14000,  # per kilogram
        "location": "Shelf 1, Row 3"
    },
    {
        "barcode_id": "8802468135790",
        "name": "Chicken Eggs",
        "category": "Eggs",
        "quantity": 200,
        "price": 2200,  # per egg
        "location": "Shelf 3, Row 1"
    },
    {
        "barcode_id": "8803579246801",
        "name": "Wheat Flour",
        "category": "Groceries",
        "quantity": 60,
        "price": 9000,  # per kilogram
        "location": "Shelf 1, Row 4"
    }
]


def validate_int_input(input_text, allow_empty=False):
    while True:
        try:
            user_input = input(input_text).strip()
            if not user_input and allow_empty:
                return None  # Allow empty input to keep the old value
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def validate_string_input(input_text):
    while True:
        user_input = input(input_text).strip()
        if user_input:
            return user_input
        print("Invalid input. can not be empty.")


def read(products_list=products):
    if not products_list:
        print("No products available.")
        return

    # Print table header
    print(f"{'No':<3} {'Barcode ID':<15} {'Name':<15} {'Category':<12} {'Quantity':<10} {'Price':<8} {'Location':<15}")
    print("-" * 80)

    # Print table rows
    for index, product in enumerate(products_list):
        print(
            f"{index + 1:<3} {product['barcode_id']:<15} {product['name']:<15} {product['category']:<12} {product['quantity']:<10} {product['price']:<8} {product['location']:<15}")


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def sleep():
    input("Press Enter to continue...")


def add_product():
    while True:
        barcode_id = validate_string_input("Enter barcode ID: ")
        # Check if the barcode ID already exists
        if barcode_id in [product['barcode_id'] for product in products]:
            print(
                "Product with the same barcode ID already exists. Please enter a different barcode ID.")
        else:
            break

    name = validate_string_input("Enter product name: ")
    category = validate_string_input("Enter product category: ")

    quantity = validate_int_input("Enter quantity: ")
    price = validate_int_input("Enter price per unit: ")
    shelf = validate_int_input("Enter shelf number: ")
    row = validate_int_input("Enter row number: ")

    # Combine shelf and row into a single location string
    location = f"Shelf {shelf}, Row {row}"

    print("\nNew Product Details:")
    print(f"Barcode ID: {barcode_id}")
    print(f"Name: {name}")
    print(f"Category: {category}")
    print(f"Quantity: {quantity}")
    print(f"Price: {price}")
    print(f"Location: {location}")
    confirmation = input(
        "Do you want to add this product? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        products.append({
            "barcode_id": barcode_id,
            "name": name,
            "category": category,
            "quantity": quantity,
            "price": price,
            "location": location
        })
        print("Product added successfully.")
    else:
        print("Product addition cancelled.")


def menu_add_product():
    while True:
        clear()
        print("\n\nAdd Product")
        print("1. Add Product")
        print("2. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            clear()
            add_product()
            sleep()
            break
        elif choice == "2":
            clear()
            sleep()
            break
        else:
            print("Invalid choice please choose between 1-2")


def search_products():
    while True:
        search_by = input(
            "Search by (barcode_id/name/category/location): ").strip().lower()

        if search_by in ['barcode_id', 'name', 'category', 'location']:
            break  # Exit the loop if the input is valid
        else:
            print(
                "Invalid search type. Please choose between 'barcode_id', 'name', 'category', or 'location'.")

    if search_by == 'location':
        shelf = input("Enter shelf (e.g., 'Shelf 1'): ").strip().lower()
        row = input("Enter row (e.g., 'Row 2'): ").strip().lower()

        filtered_products = []
        for product in products:
            location = product['location'].strip().lower()
            # Extract shelf and row from location
            product_shelf, product_row = location.split(', ')
            # Check if the shelf and row match
            if (shelf in product_shelf) and (row in product_row):
                filtered_products.append(product)
    else:
        search_value = input(f"Enter the {search_by}: ").strip().lower()
        filtered_products = [
            product for product in products
            if search_value in product[search_by].strip().lower()
        ]

    return filtered_products


def sort_products(product_list):
    sort_input = input(
        "Sort by (field,order) or press Enter to skip sorting (e.g., 'quantity,asc' or 'price,desc'): ").strip().lower()

    if sort_input:
        try:
            sort_field, sort_order = sort_input.split(',')
            if sort_field in ['barcode_id', 'name', 'category', 'quantity', 'price', 'location']:
                reverse = sort_order == 'desc'
                if sort_field == 'location':
                    sorted_list = sorted(product_list, key=lambda x: (
                        # Sort by shelf number
                        int(x['location'].split(',')[0].split()[1]),
                        # Then sort by row number
                        int(x['location'].split(',')[1].split()[1])
                    ), reverse=reverse)
                else:
                    sorted_list = sorted(
                        product_list, key=lambda x: x[sort_field], reverse=reverse)
            else:
                print("Invalid sort field. Displaying results without sorting.")
                sorted_list = product_list
        except ValueError:
            print(
                "Invalid format. Use 'field,asc' or 'field,desc'. Displaying results without sorting.")
            sorted_list = product_list
    else:
        print("No sorting applied.")
        sorted_list = product_list

    return sorted_list


def manage_product_search():
    print("Search Product")

    # Filter the products based on user input
    found_products = search_products()

    # If products are found, sort them
    if found_products:
        # Display the search results
        print("\nSearch Results:")
        if len(found_products) > 1:
            sorted_products = sort_products(found_products)
            read(sorted_products)
        else:
            read(found_products)

    else:
        print("No products found.")


def select_product(products_list, input_text):
    while True:
        try:
            product_index = int(input(f"\n{input_text}")) - 1
            if 0 <= product_index < len(products_list):
                return products_list[product_index]
            else:
                print("Invalid selection. Please choose a valid product number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def update_product():
    clear()
    print("Update Product")

    # Search for products
    found_products = search_products()

    if found_products:
        if len(found_products) > 1:
            # Display search results
            print("\nSelect the product to update:")
            read(found_products)

            # Ask user to select a product to update
            product_to_update = select_product(
                found_products, "Enter the number of the product you want to update: ")
        else:
            product_to_update = found_products[0]

        # Update product details
        print(f"\nUpdating product: {product_to_update['name']}")
        product_to_update['name'] = input(
            f"Enter new name (current: {product_to_update['name']}) or press Enter to keep: ").strip() or product_to_update['name']
        product_to_update['category'] = input(
            f"Enter new category (current: {product_to_update['category']}) or press Enter to keep: ").strip() or product_to_update['category']

        # Validate and update quantity
        quantity = validate_int_input(
            f"Enter new quantity (current: {product_to_update['quantity']}) or press Enter to keep: ", allow_empty=True)
        if quantity is not None:
            product_to_update['quantity'] = quantity

        # Validate and update price
        price = validate_int_input(
            f"Enter new price (current: {product_to_update['price']}) or press Enter to keep: ", allow_empty=True)
        if price is not None:
            product_to_update['price'] = price

        # Update location by prompting for shelf and row
        while True:
            try:
                # Extract current shelf and row from location
                current_location = product_to_update['location']
                current_shelf = current_location.split(
                    ', ')[0].replace('Shelf ', '')
                current_row = current_location.split(
                    ', ')[1].replace('Row ', '')

                # Prompt user for new shelf and row
                shelf = validate_int_input(
                    f"Enter new shelf (current: {current_shelf}) or press Enter to keep: ", allow_empty=True)
                row = validate_int_input(
                    f"Enter new row (current: {current_row}) or press Enter to keep: ", allow_empty=True)

                # Use current values if no new values are entered
                if shelf is None:
                    shelf = int(current_shelf)
                if row is None:
                    row = int(current_row)

                # Update location with new shelf and row
                product_to_update['location'] = f"Shelf {shelf}, Row {row}"
                break
            except ValueError:
                print("Invalid input. Please enter valid numbers for shelf and row.")

        print("Product updated successfully.")
    else:
        print("No products found to update.")


def delete_product():
    clear()
    print("Delete Product")

    found_products = search_products()
    if found_products:

        if len(found_products) > 1:
            # Display search results
            print("\nSelect the product to delete:")
            read(found_products)
            # Ask user to select a product to delete, if multiple products are found
            product_to_delete = select_product(
                found_products, "Enter the number of the product you want to delete: ")
        else:
            product_to_delete = found_products[0]

        confirmation = input(
            f"Are you sure you want to delete the product '{product_to_delete['name']}'? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            products.remove(product_to_delete)
            print("Product deleted successfully.")
        else:
            print("Product deletion cancelled.")
    else:
        print("No products found to delete.")


def view_product():
    while True:
        clear()
        print("\n\nView Product")
        print("1. View all products")
        print("2. Search product")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            clear()
            read()
            sleep()
        elif choice == "2":
            clear()
            manage_product_search()
            sleep()
        elif choice == "3":
            break
        else:
            print("Invalid choice please choose between 1-3")


def menu_update_product():
    while True:
        clear()
        print("\n\nUpdate Product")
        print("1. Update Product")
        print("2. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            clear()
            update_product()
            sleep()
            break
        elif choice == "2":
            clear()
            sleep()
            break
        else:
            input("Invalid choice please choose between 1-2")


def menu_delete_product():
    while True:
        clear()
        print("\n\nDelete Product")
        print("1. Delete Product")
        print("2. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            clear()
            delete_product()
            sleep()
            break
        elif choice == "2":
            clear()
            sleep()
            break
        else:
            input("Invalid choice please choose between 1-2")


def main_menu():
    while True:
        clear()
        print("\n\nWelcome to Sembako Sejahtera\n")
        read()
        print("\n\nMenu")
        print("1. Add Product")
        print("2. View Product")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            menu_add_product()
        elif choice == "2":
            view_product()
        elif choice == "3":
            menu_update_product()
        elif choice == "4":
            menu_delete_product()
        elif choice == "5":
            input('Thank you for using our program')
            break
        else:
            print("Invalid choice please choose between 1-5")
            sleep()


if __name__ == "__main__":
    main_menu()
