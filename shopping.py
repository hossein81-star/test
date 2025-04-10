import json
import time


# Class to manage user-related operations
class users_class:
    def __init__(self):
        # Dictionary to store the list of users
        self.user_list = {}
        # Variables to track login and registration status
        self.is_user = None
        self.isregestered = False
        self.user_name = None

    # Function to open and read users from a JSON file
    def open_user_json(self):
        with open("user.json", "r", encoding="utf_8") as p_file:
            self.user_list = json.load(p_file)
            return self.user_list

    # Function to save users to a JSON file
    def save_user_json(self):
        with open("user.json", "w", encoding="utf_8") as p_file:
            json.dump(self.user_list, p_file, indent=4)

    # Function to check a user's password
    def check_password(self, us_name):
        while True:
            print("\n" + "=" * 40)
            password = input("🔑 Enter your password (or type 'exit' to quit): ")

            if password.lower() == "exit":
                print("🚪Exiting  Please wait...")
                time.sleep(1)
                break

            elif password == self.user_list[us_name]["password"]:
                self.isregestered = True
                print("✅ Access granted! Welcome! 🎉")
                return True

            else:
                print("❌ Incorrect password! Please try again.")
                self.user_name = None

    # Function to handle user login or registration
    def regester(self):
        print("You need to register first!")
        self.open_user_json()
        self.user_name = input("enter usrer name: ")
        if self.user_name in self.user_list:
            # If user already exists, verify password
            is_user = self.check_password(self.user_name)
            return is_user
        else:
            # If user doesn't exist, prompt for registration
            print("\n" + "=" * 40)
            print("📝 Please Register:")
            print("=" * 40)
            self.isregestered = self.regester_new_user()
            self.user_name = None

    # Function to register a new user
    def regester_new_user(self):
        self.open_user_json()

        print("\n" + "=" * 40)
        print("📝 Welcome! Let's create your account.")
        print("=" * 40)

        new_us_name = input("👤 Enter your username: ").strip()
        if new_us_name in self.user_list:
            print("⚠️ This username already exists! Try another one.")
            return

        new_us_password = input("🔑 Enter your password: ").strip()
        self.user_name = new_us_name
        self.user_list[new_us_name] = {"password": new_us_password, "cart": {"product": []}, "total": 0}
        self.isregestered = True
        self.save_user_json()
        print("\n✅ Registration successful! 🎉")
        time.sleep(1)
        print(f"🚀 Welcome, {new_us_name}!")

        return True


# Class to manage products
class product:
    def __init__(self, cart, users):
        self.users = users
        self.cart = cart
        # Load product list from JSON
        self.product_list = self.open_json()

    # Load product data from file
    @staticmethod
    def open_json():
        with open("product_list.json", "r", encoding="utf_8") as p_file:
            product_list = json.load(p_file)
        return product_list

    # Save product data to file
    @staticmethod
    def save_in_json(products_li):
        with open("product_list.json", "w", encoding="utf_8") as p_file:
            json.dump(products_li, p_file, indent=4)

    # Show products in the selected category
    def choised_category(self, category):
        category_pro_list = {
            key: product for key, product in self.product_list.items() if product["category"] == category
        }

        print(category_pro_list)

        if not category_pro_list:
            print(f"❌ No products found in the '{category}' category.")
            return

        print(f"\n📌 Products in the '{category}' category:\n")

        while True:
            for i, product in enumerate(category_pro_list.values(), 1):
                print(f"{i}. Name: {product['name']}")
                print(f"   Price: {product['price']}")
                print(f"   Stock: {product['stock']}")
                print("-" * 30)

            q = input("Do you have a choice? (yes/no): ").strip().lower()

            if q == "yes":
                if self.users.isregestered:
                    choised_product = input("\n🛍️ Enter the product you want to buy: ")
                    product_num = int(input("📦 Enter the quantity: "))
                    self.cart.control_shop(choised_product, category_pro_list, product_num)
                elif self.users.regester():
                    choised_product = input("\n🛍️ Enter the product you want to buy: ")
                    product_num = int(input("📦 Enter the quantity: "))
                    self.cart.control_shop(choised_product, category_pro_list, product_num)
                else:
                    print("❌ Registration failed! Please try again.")
            elif q == "no":
                print("\n✨ Thank you! Have a great day! ✨\n")
                break
            else:
                print("\n⚠️ Invalid input! Please enter 'yes' or 'no'.\n")

    # Display available product categories
    def show_product_category(self):
        self.open_json()
        pro_category = list(set(map(lambda pro: pro["category"], self.product_list.values())))
        print(pro_category)

        while True:
            print("\n📌 Available Categories:")
            for index, category in enumerate(pro_category, start=1):
                print(f"🔹 {index}. {category}")

            user_input = input("\nEnter a category name to view products (or type 'exit' to quit): ").strip()

            if user_input.lower() == "exit":
                print("👋 Exiting category selection.")
                break

            if user_input in pro_category:
                self.choised_category(user_input)
            else:
                print("❌ Invalid category! Please enter an exact category name.")


# Class to manage the shopping cart
class shopping_cart:
    def __init__(self, users):
        self.users = users
        self.pro_list = product.open_json()
        self.buyed_pro = {}
        self.users_list = {}

    # Check if the product is available in the required quantity
    def control_shop(self, pro_name, category, num):
        if pro_name not in category:
            print("❌ Product not found!")
        else:
            if category[pro_name]["stock"] < num:
                print("❌ Not enough stock available!")
            else:
                self.add_to_shop(pro_name, category, num)

    # Add selected product to cart
    def add_to_shop(self, pro_name, category, num):
        self.users_list = self.users.open_user_json()

        if category[pro_name]["category"] == "Books":
            self.set_buyed_pro_ditails(pro_name, category, num, "author")
        else:
            self.set_buyed_pro_ditails(pro_name, category, num, "brand")

        self.sum_of_total_cash(self.users.user_name)
        self.users.save_user_json()
        self.number_reducer(num, pro_name)

    # Set product details in the cart
    def set_buyed_pro_ditails(self, pro_name, category, num, type):
        self.buyed_pro["name"] = pro_name
        self.buyed_pro["num"] = num
        self.buyed_pro["price"] = category[pro_name]["price"]
        self.buyed_pro["total_cash"] = self.buyed_pro["price"] * num
        print(f"before: {self.users_list[self.users.user_name]['cart']['product']}")
        if type == "brand":
            self.buyed_pro["brand"] = category[pro_name]["brand"]
        else:
            self.buyed_pro["author"] = category[pro_name]["author"]

        self.users_list[self.users.user_name]["cart"]["product"].append(self.buyed_pro)
        print(f"after: {self.users_list[self.users.user_name]['cart']['product']}")

    # Calculate total amount of user's cart
    def sum_of_total_cash(self, user_name):
        total_price_of_cart = sum([item["total_cash"] for item in self.users_list[user_name]["cart"]["product"]])
        self.users_list[user_name]["total"] = total_price_of_cart

    # Decrease the stock quantity after purchase
    def number_reducer(self, num, pro_name):
        self.pro_list[pro_name]["stock"] -= num
        product.save_in_json(self.pro_list)

    # Display the user's cart
    def show_cart(self, user_name):
        self.users_list = self.users.open_user_json()
        products = self.users_list[user_name]["cart"]["product"]

        print(f"\n🛒 Cart for {user_name}:\n{'-' * 40}")

        if not products:
            print("Your cart is empty.\n")
            return

        for idx, item in enumerate(products, start=1):
            print(f"Product {idx}:")
            print(f"  Name : {item['name']}")
            print(f"  Brand: {item.get('brand', item.get('author'))}")  # Show either brand or author
            print(f"  Qty  : {item['num']}")
            print(f"  Price: {item['price']} USD")
            print("-" * 40)

        print(f"💵 Total: {self.users_list[user_name]['total']} USD")


# Create instances
users = users_class()
shop_cart = shopping_cart(users)
products = product(shop_cart, users)
