# E-commerce Food Delivery Application System

## Introduction

The project aims to develop an application system for an E-commerce food delivery app, targeted at the company's employees. This tool will facilitate access to extensive data related to past food deliveries, encompassing various entities within the platform.

### Entities and Entity Sets

- **Users**: With attributes like `user_id`, `name`, `phone_number`, `email`, `member_since`. `Email` and `phone_number` serve as candidate keys.
- **Customers**: Attributes include `number_of_orders_made`, `subscription_status`.
- **Drivers**: Attributes cover `number_of_deliveries_made`, `driver_license_id`, `vehicle_type`.
- **Orders**: Comprising `order_id`, `tip`, `total_price`, `status`, `delivered_time`, and timestamp attributes for `Take_order` and `Create_order` relationships.
- **Restaurants**: With `restaurant_id`, `phone_number`, `opening_hour`, `closing_hour`.
- **Menus**: Includes `menu_id`, `name`, `price`.
- **Addresses**: Constituted by `address_id`, `address_line1`, `address_line2`, `city`, `state`, `zip_code`.

### Relationship Sets

- `create_order`: Connects Customers to Orders.
- `receive_order`: Connects Drivers to Orders.
- `order_from`: Connects Orders to Restaurants.
- `lives_at`: Connects Customers to Addresses.
- `deliver_to`: Connects Drivers to Addresses.
- `located_at`: Connects Restaurants to Addresses.
- `ordered_menu`: Connects Menus to Orders.
- `cook`: Connects Menus to Restaurants.

### Constraints

- Every user and restaurant must have exactly one address.
- Every menu in the order must be valid at the directed restaurant.
- Every order requires a driver for delivery and a customer who ordered it.

## Dataplan

- Restaurant and menu data will be sourced from online platforms (e.g., Grubhub, Uber Eats datasets on Kaggle).
- Dummy data will be generated for personal data like User and Driver Information.

## User Interaction Plans

- Users can access different sections: User, Driver, Order, Restaurant, Address information, and Payment Methods.
- Features include searching, filtering, and sorting database records.
