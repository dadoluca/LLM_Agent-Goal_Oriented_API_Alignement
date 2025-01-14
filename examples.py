# actors
example1_actors = """

        **Example:**\n\n
        The following is a description of a software project: \n
        "\"The application is designed to streamline food delivery operations. Customers can browse menus and place orders. Delivery personnel use the app to view delivery assignments and update order statuses. Restaurant managers can manage their menus and track incoming orders.\"\n",
        "\n",
        "Extracted Roles:\n",
        "name:  Customers, description: Individuals who order food\n",
        "name: Delivery Personnel, description: People who deliver orders\n",
        "name: Restaurant Managers, description: Individuals managing restaurant operations.\n",
        """

example2_actors = """

        **Example:**\n\n
        The following is a description of a software project: \n
        "\n"The application facilitates home maintenance services. Homeowners can browse available service providers, request quotes, and book appointments. Service providers can manage their profiles, respond to quote requests, and update job statuses. Administrators oversee platform operations, ensuring smooth communication and resolving disputes.\"\n",
        "\n",
        "Extracted Roles:\n"
        "name: Homeowners, description: People seeking home maintenance services.\n"
        "name: Service Providers, description: Professionals offering maintenance services.\n"
        "name: Administrators, description: Individuals overseeing platform operations.\n"
        """

# high level

example1_hl = """
    **Example:**\n\n

    Description: \n\n
    "The application is designed to streamline food delivery operations. Customers can browse menus and place orders. Delivery personnel use the app to view delivery assignments and update order statuses. Restaurant managers can manage their menus and track incoming orders.\n"\n",
    Actors:\n
    name: Customers, description: Individuals who order food.\n
    name: Delivery Personnel, description: People who deliver orders.\n
    name: Restaurant Managers, description: Individuals managing restaurant operations.\n
    Output:\n
    '{ "highLevelGoals": ["Allow customers to browse available menus and place orders", "Enable delivery personnel to manage delivery assignments and update order statuses", "Provide restaurant managers with tools to manage menus and track orders efficiently", "Facilitate seamless communication between customers, delivery personnel, and restaurant managers"]}'
    """

example2_hl = """
    **Example:**:\n\n

    Description: \n\n
    "Create an online store platform where users can browse products, add them to their cart, and checkout with multiple payment options.\n"\n,
    Actors:\n
    name: Visitor, description: Individuals browsing the platform without creating an account.\n
    name: Developer, description: Professionals maintaining and improving the platform's functionality.\n
    Output:\n
    '{ "highLevelGoals": ["Enable user to browse products", "Allow users to add products to cart", "Implement multiple payment options for checkout"]}'
    """

# low level

example1_ll = """
    **Example:**:\n\n
    Given the high level goal:\n
    "Allow customers to browse available menus and place orders"\n
    Output:\n
    {"lowLevelGoals":
        ["Design a user-friendly interface for menu browsing",
        "Implement a search functionality for specific dishes or categories",
        "Enable customers to customize orders (e.g., add toppings or remove ingredients)",
        "Integrate a secure checkout system for placing orders",
        "Allow users to save favorite orders for quick reordering"
      ]
    }\n\n
    """

example2_ll = """
    **Example:**:\n\n
    Given the high level goal:\n
    "Build an online shopping platform"\n
    Output:\n
    {"lowLevelGoals": ["Implement user authentication", "Integrate payment gateway", "Create shopping cart functionality"]}\n\n'
    """