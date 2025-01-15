# actors
example1_actors = """

        **Example:**\n\n
        The following is a description of a software project: \n
        "\"The application is designed to streamline food delivery operations. Customers can browse menus and place orders. Delivery personnel use the app to view delivery assignments and update order statuses. Restaurant managers can manage their menus and track incoming orders.\"\n",
        "\n",
        "Extracted Roles:\n",
        "name: Customers, description: Individuals who order food\n",
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

# map


example1_map = """
    **Example:**:\n\n
    Given the following goal:
    "Implement a feature that calculates delivery fees dynamically based on the customer’s location, distance from the restaurant, and current demand."
    And the list of APIs below:
    [API(api_name='getRestaurantListGET', api_path='/restaurants', description='Fetches a list of restaurants available in the user’s area', request_type='get'),
    API(api_name='getMenuItemsGET', api_path='/restaurants/\{restaurant_id\}/menu', description='Retrieves the menu items of a specific restaurant', request_type='get'),
    API(api_name='postPlaceOrderPOST', api_path='/orders', description='Places a new order with the selected items and delivery details', request_type='post'),
    API(api_name='getOrderStatusGET', api_path='/orders/\{order_id\}/status', description='Fetches the current status of an order', request_type='get'),
    API(api_name='calculateDeliveryFeePOST', api_path='/delivery/fee', description='Calculates the delivery fee based on location and distance', request_type='post'),
    API(api_name='getUserProfileGET', api_path='/users/\{user_id\}', description='Retrieves the user profile information', request_type='get'),
    API(api_name='postUpdateOrderStatusPOST', api_path='/orders/\{order_id\}/status', description='Updates the status of an order (e.g., picked up, on the way)', request_type='post'),
    API(api_name='getRestaurantAnalyticsGET', api_path='/restaurants/\{restaurant_id\}/analytics', description='Fetches analytics data for a restaurant, such as sales trends and popular items', request_type='get'),
    API(api_name='postCustomerFeedbackPOST', api_path='/feedback', description='Submits feedback or reviews for a completed order', request_type='post')]

    Output:\n
    calculateDeliveryFeePOST
"""

example2_map = """
    **Example:**\n\n
    Given the following goal:
    "Implement a feature that sends automated reminders to users about upcoming appointments via email and push notifications."
    And the list of APIs below:
    [API(api_name='getUserPreferencesGET', api_path='/users/\{user_id\}/preferences', description='Fetches the notification and communication preferences of a user', request_type='get'),
    API(api_name='postUpdateUserProfilePOST', api_path='/users/\{user_id\}', description='Allows users to update their profile information', request_type='post'),
    API(api_name='getProviderSpecializationsGET', api_path='/providers/specializations', description='Fetches the list of available provider specializations', request_type='get'),
    API(api_name='postUploadInsuranceDetailsPOST', api_path='/users/\{user_id\}/insurance', description='Allows users to upload and update insurance details', request_type='post'),
    API(api_name='getAppointmentDetailsGET', api_path='/appointments/\{appointment_id\}', description='Retrieves the details of a specific appointment', request_type='get'),
    API(api_name='getUserActivityLogGET', api_path='/users/\{user_id\}/activity', description='Fetches the activity log for a user account', request_type='get'),
    API(api_name='postAddProviderReviewPOST', api_path='/reviews', description='Allows users to submit reviews for healthcare providers', request_type='post'),
    API(api_name='getAvailableTimeslotsGET', api_path='/providers/\{provider_id\}/timeslots', description='Fetches the available appointment times for a healthcare provider', request_type='get'),
    API(api_name='getHealthcareArticlesGET', api_path='/articles', description='Retrieves a list of healthcare-related articles for user education', request_type='get'),
    API(api_name='postGenerateInvoicePOST', api_path='/billing/invoice', description='Generates an invoice for a user’s recent transactions', request_type='post')]

    Output:\n
    No API Found
"""