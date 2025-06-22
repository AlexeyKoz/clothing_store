# Clothing Store - Django E-commerce Platform

A full-featured e-commerce platform built with Django, featuring a modern web interface, REST API, and comprehensive shopping functionality.

## 🛍️ Features

### Core E-commerce Features
- **Product Catalog**: Browse products by category, brand, and search functionality
- **Shopping Cart**: Add/remove items, update quantities, view cart total
- **User Authentication**: Registration, login, logout with email verification
- **Order Management**: Complete checkout process with address and payment details
- **Product Reviews**: Users can leave reviews and ratings for products
- **Product Likes**: Users can like/favorite products
- **Admin Panel**: Full Django admin interface for managing products, orders, and users

### Advanced Features
- **REST API**: Complete API with JWT authentication for mobile apps or third-party integrations
- **Social Authentication**: Google and Facebook login support
- **PDF Invoice Generation**: Automatic invoice generation for orders
- **Support Tickets**: Customer support system for order-related issues
- **Caching**: Redis-based caching for improved performance
- **Responsive Design**: Mobile-friendly interface with modern UI

### Technical Features
- **PostgreSQL Database**: Robust database backend
- **Redis Caching**: Performance optimization
- **JWT Authentication**: Secure API authentication
- **File Upload**: Product image management
- **Email Integration**: Order confirmations and notifications
- **Search Functionality**: Product search with filters

## 🏗️ Project Structure

```
clothing_store/
├── api/                    # REST API endpoints
├── cart/                   # Shopping cart functionality
├── catalog/                # Product catalog and management
├── config/                 # Django settings and configuration
├── core/                   # Core functionality and home page
├── orders/                 # Order management and checkout
├── reviews/                # Product reviews system
├── scripts/                # Data population scripts
├── static/                 # CSS, JS, and static assets
├── support/                # Customer support tickets
├── templates/              # HTML templates
├── users/                  # User management and profiles
└── manage.py              # Django management script
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Redis (optional, for caching)
- Git

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd clothing_store
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=clothing_store
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### Step 5: Database Setup
```bash
# Create PostgreSQL database
createdb clothing_store

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Step 6: Populate Sample Data (Optional)
```bash
# Run all population scripts
python scripts/populate_all_stuff_100.py

# Or run individual scripts
python scripts/populate_brands.py
python scripts/populate_categories.py
python scripts/populate_products.py
python scripts/populate_users.py
```

### Step 7: Start Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## 📱 API Endpoints

### Authentication
- `POST /api/token/` - Get JWT tokens
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details
- `POST /api/products/` - Create product (admin only)
- `PUT /api/products/{id}/` - Update product (admin only)
- `DELETE /api/products/{id}/` - Delete product (admin only)

### Cart
- `GET /api/cart-items/` - Get user's cart items
- `POST /api/cart-items/` - Add item to cart
- `PUT /api/cart-items/{id}/` - Update cart item
- `DELETE /api/cart-items/{id}/` - Remove item from cart

### Orders
- `GET /api/orders/` - Get user's orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get order details

### Users
- `GET /api/users/` - List users (admin only)
- `GET /api/users/{id}/` - Get user details (admin only)

## 🛒 User Features

### Shopping Experience
1. **Browse Products**: Navigate through categories and brands
2. **Search**: Find products using the search bar
3. **Product Details**: View detailed product information, images, and reviews
4. **Add to Cart**: Add products to shopping cart
5. **Manage Cart**: Update quantities, remove items
6. **Checkout**: Complete purchase with shipping and payment details
7. **Order Tracking**: View order status and history

### User Account
- **Registration**: Create account with email verification
- **Profile Management**: Update personal information
- **Address Management**: Save shipping addresses
- **Order History**: View past orders and invoices
- **Reviews**: Leave reviews for purchased products

## 🔧 Admin Features

### Product Management
- Add/edit/delete products
- Manage categories, brands, colors, and sizes
- Upload product images
- Set pricing and stock status

### Order Management
- View all orders
- Update order status
- Generate invoices
- Process refunds

### User Management
- View user accounts
- Manage user profiles
- Handle support tickets

## 🎨 Frontend Features

### Modern UI/UX
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Navigation**: Clean navbar with search functionality
- **Product Grid**: Attractive product display with images
- **Interactive Elements**: Hover effects, buttons, and forms
- **User Feedback**: Success/error messages and notifications

### Key Pages
- **Home Page**: Featured products and categories
- **Product Catalog**: Browse by category and brand
- **Product Detail**: Full product information with reviews
- **Shopping Cart**: Cart management interface
- **Checkout**: Multi-step checkout process
- **User Dashboard**: Account management
- **Order History**: Past orders and invoices

## 🔒 Security Features

- **JWT Authentication**: Secure API access
- **CSRF Protection**: Cross-site request forgery protection
- **Password Validation**: Strong password requirements
- **Email Verification**: Account verification via email
- **Admin Permissions**: Role-based access control
- **Input Validation**: Form validation and sanitization

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in settings
2. Configure production database
3. Set up static file serving
4. Configure email backend
5. Set up Redis for caching
6. Configure web server (Nginx + Gunicorn)

### Environment Variables
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DB_NAME=production_db_name
DB_USER=production_db_user
DB_PASSWORD=production_db_password
DB_HOST=production_db_host
DB_PORT=5432
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

The project includes comprehensive tests for:
- User authentication
- Shopping cart functionality
- Order processing
- Product management
- API endpoints

## 📊 Performance

- **Caching**: Redis-based caching for popular products
- **Database Optimization**: Efficient queries and indexing
- **Static Files**: Optimized CSS and JavaScript
- **Image Optimization**: Compressed product images

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Updates

Stay updated with the latest features and bug fixes by regularly pulling from the main branch:
```bash
git pull origin main
python manage.py migrate
```

---

**Happy Shopping! 🛍️**
