# Online Retail Store Database Management System

## Description
The Online Retail Store Database Management System is a comprehensive backend system designed to manage customer information, product inventory, order tracking, and associated contact details. Built with Flask, SQLAlchemy ORM, and PostgreSQL, this project supports CRUD operations and allows seamless integration with REST APIs.

## API Reference

### Endpoints

| Endpoint                | Method | Description                       | Parameters                                                                                               |
|-------------------------|--------|-----------------------------------|---------------------------------------------------------------------------------------------------------|
| `/customers`            | GET    | Retrieve all customers            | None                                                                                                    |
| `/customers/<id>`       | GET    | Retrieve a specific customer      | `id` (integer)                                                                                          |
| `/customers`            | POST   | Create a new customer             | `username`, `password`, `email_id`, `first_name`, `last_name`, `contact_id` (optional, list of integers)|
| `/customers/<id>`       | DELETE | Delete a specific customer        | `id` (integer)                                                                                          |
| `/customers/<id>`       | PATCH  | Update a specific customer        | `id` (integer), fields to update (e.g., `username`, `email_id`, etc.)                                   |
| `/contacts/<id>`        | GET    | Retrieve a specific contact       | `id` (integer)                                                                                          |
| `/contacts`             | POST   | Create a new contact              | Address details (`address_line1`, `city`, etc.), `phone_number`                                         |
| `/contacts/<id>`        | DELETE | Delete a specific contact         | `id` (integer)                                                                                          |
| `/orders/<id>`          | GET    | Retrieve a specific order         | `id` (integer)                                                                                          |

## Retrospective

### How did the project's design evolve over time?
The project began with a conceptual ER diagram that defined the entities and their relationships. Over time, these relationships were translated into database tables, and an ORM-based backend was implemented to handle data interactions. Using SQLAlchemy provided a flexible way to modify the database schema while ensuring data integrity and simplifying relationships through declarative models.

### Did you choose to use an ORM or raw SQL? Why?
The project uses the ORM approach via SQLAlchemy. This decision was made because ORM abstracts the complexities of SQL queries, reduces boilerplate code, and provides an object-oriented way to interact with the database. It ensures maintainability and security while streamlining complex relationship management, especially in a relational schema like this one.

### What future improvements are in store, if any?
Future enhancements may include:
- **Payment System Integration**: Adding endpoints for handling payment processing and tracking.
- **Authentication**: Implementing  authentication for secure access.
- **Order Fulfillment**: Extending the API to include shipment tracking and delivery status updates.
- **Performance Optimization**: Indexing frequently queried columns and caching query results.

## Challenges and Learnings
Challenges faced during the implementation included:
- Managing many-to-many relationships between customers and contacts using an association table.
- Implementing Flask Blueprints to modularize endpoints.
- Debugging errors while starting the local Flask web server and testing APIs in Insomnia.

These challenges provided valuable insights into API design, Flask architecture, and ORM-based relationship management. 

## Initial Design

The initial ER diagram highlighted key entities and relationships:
- **Customer-Address**: Many-to-many relationship with a bridge table.
- **Customer-Order**: One-to-many relationship linking customers to their orders.
- **Order-OrderItem**: One-to-many relationship between orders and their items.
- **OrderItem-Product**: One-to-many relationship associating products with order items.

This design ensured normalization and scalability while adhering to database best practices.
