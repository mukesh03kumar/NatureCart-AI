from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from Seller_app.models import Product
from .models import UserProfile, CartItem, Order, OrderItem, PlasticAlternative

def home(request):
    products = Product.objects.filter(stock__gt=0)
    category = request.GET.get('category')
    search_query = request.GET.get('search')

    if category:
        products = products.filter(category=category)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # AI Personalized Recommendations
    ai_recommendations = []
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            if profile.preference:
                # Map preference to database categories
                pref_map = {
                    'Zero-Waste': ['Bags', 'Dental', 'Hydration'],
                    'Organic': ['Cleaning', 'Home'],
                    'Plastic-Free': ['Bags', 'Dental', 'Hydration', 'Composting'],
                    'Carbon-Footprint': ['Composting', 'Stationery', 'Home']
                }
                preferred_categories = pref_map.get(profile.preference, [])
                ai_recommendations = Product.objects.filter(
                    category__in=preferred_categories,
                    stock__gt=0
                ).exclude(seller=request.user).order_by('-co2_saving_weight')[:3]
        except UserProfile.DoesNotExist:
            pass

    # If no recommendations, grab top saving products
    if not ai_recommendations:
        ai_recommendations = Product.objects.filter(stock__gt=0).order_by('-plastic_saving_weight')[:3]

    categories = Product.CATEGORY_CHOICES

    return render(request, "customer/home.html", {
        "products": products,
        "categories": categories,
        "ai_recommendations": ai_recommendations,
        "selected_category": category,
        "search_query": search_query
    })

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        role = request.POST.get("role")
        preference = request.POST.get("preference")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "registration/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "registration/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "registration/register.html")

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            phone=phone,
            address=address,
            role=role,
            preference=preference
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "registration/register.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == "Seller":
                    return redirect("seller_dashboard")
                else:
                    return redirect("home")
            except UserProfile.DoesNotExist:
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "registration/login.html")

    return render(request, "registration/login.html")

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")

def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    # Find if there are plastic alternatives linked to this product
    alternatives = PlasticAlternative.objects.filter(alternative_product=product)
    
    # Simple recommendation: other products in same category
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]

    return render(request, "customer/product_details.html", {
        "product": product,
        "alternatives": alternatives,
        "related_products": related_products
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if profile.role != "Customer":
        messages.error(request, "Only customers can add items to cart.")
        return redirect("home")

    cart_item, created = CartItem.objects.get_or_create(
        customer=request.user,
        product=product
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"Added {product.name} to cart.")
    return redirect("cart")

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    
    # Calculate potential environmental savings
    total_plastic_savings = sum(item.product.plastic_saving_weight * item.quantity for item in cart_items)
    total_co2_savings = sum(item.product.co2_saving_weight * item.quantity for item in cart_items)
    
    return render(request, "customer/cart.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "total_plastic_savings": total_plastic_savings,
        "total_co2_savings": total_co2_savings
    })

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, customer=request.user)
    action = request.POST.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    elif action == 'remove':
        cart_item.delete()
        
    return redirect("cart")

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("home")
        
    # Calculate totals
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    order_plastic_saved = sum(item.product.plastic_saving_weight * item.quantity for item in cart_items)
    order_co2_saved = sum(item.product.co2_saving_weight * item.quantity for item in cart_items)
    
    # Check stock
    for item in cart_items:
        if item.product.stock < item.quantity:
            messages.error(request, f"Sorry, only {item.product.stock} units of {item.product.name} are available.")
            return redirect("cart")

    if request.method == "POST":
        payment_method = request.POST.get('payment_method', 'Card')
        
        # Create Order
        order = Order.objects.create(
            customer=request.user,
            total_price=subtotal,
            plastic_saved=order_plastic_saved,
            co2_saved=order_co2_saved,
            status='Pending'
        )
        
        # Create OrderItems and decrease stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()
            
        # Update User Profile dynamic green totals
        profile = request.user.userprofile
        profile.total_plastic_saved += order_plastic_saved
        profile.total_co2_saved += order_co2_saved
        profile.save()
        
        # Empty Cart
        cart_items.delete()
        
        messages.success(
            request, 
            f"Payment of ₹ {subtotal} processed successfully via {payment_method}! Your order #{order.id} has been placed."
        )
        return redirect("my_orders")
        
    return render(request, "customer/checkout_payment.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "total_plastic_savings": order_plastic_saved,
        "total_co2_savings": order_co2_saved
    })

@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, "customer/my_orders.html", {"orders": orders})

@login_required
def dashboard(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if profile.role != "Customer":
        return redirect("seller_dashboard")
        
    # Calculate carbon and tree planting equivalent
    # Formula: 1 tree absorbs approx 22kg CO2 per year. So co2_saved / 22 = tree equivalent days/years
    # Let's say 1 tree equivalent for every 10kg of CO2 saved.
    trees_saved = float(profile.total_co2_saved) / 10.0
    
    # Handle preference updates
    if request.method == "POST":
        preference = request.POST.get('preference')
        is_premium = request.POST.get('is_premium') == 'true'
        
        profile.preference = preference
        profile.is_premium_member = is_premium
        profile.save()
        messages.success(request, "Preferences updated successfully.")
        return redirect("customer_dashboard")
        
    return render(request, "customer/dashboard.html", {
        "profile": profile,
        "trees_saved": round(trees_saved, 2)
    })

# AI Chatbot API
@login_required
def chatbot_api(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        user_message = data.get("message", "")
        
        # Simple local AI rules
        message = user_message.lower()
        if 'hello' in message or 'hi' in message or 'hey' in message:
            response = "Hello! I'm EcoBot, your NatureCart AI guide. Ask me anything about sustainable living, reducing waste, or how to shop green!"
        elif 'plastic' in message or 'waste' in message or 'pollution' in message:
            response = "Plastic waste is a major crisis. Swapping plastic products for Bamboo Toothbrushes and Reusable Shopping Bags makes a huge difference. Every eco-friendly swap keeps toxic microplastics out of our soil and oceans!"
        elif 'carbon' in message or 'co2' in message or 'greenhouse' in message or 'footprint' in message:
            response = "Each product you buy on NatureCart reduces greenhouse emissions. For example, using a Stainless Steel Bottle saves around 0.5kg of CO₂ per year compared to plastic water bottles. We track your cumulative savings on your dashboard!"
        elif 'compost' in message or 'organic' in message or 'soil' in message:
            response = "Composting returning organic waste to the soil. A home compost bin helps recycle vegetable scraps and leaves, which reduces landfill waste and builds fertile soil for gardening. It is a vital zero-waste step!"
        elif 'water' in message or 'bottle' in message or 'drink' in message:
            response = "Did you know that 1 million plastic bottles are bought every minute globally? Switching to a reusable Stainless Steel Water Bottle and Reusable Steel Straws is a simple, high-impact way to live greener."
        elif 'paper' in message or 'tree' in message or 'stationery' in message:
            response = "NatureCart's Seed Paper Stationery is crafted from recycled materials and embedded with wildflower seeds. After reading or writing, you can literally plant the paper to grow flowers!"
        elif 'cleaning' in message or 'soap' in message or 'detergent' in message:
            response = "Traditional cleaning products are packed with synthetic chemicals that pollute waterways. Our Natural Cleaning Kit uses organic, biodegradable ingredients that clean effectively without damaging the planet."
        elif 'candle' in message or 'wax' in message or 'soy' in message:
            response = "Soy Wax Candles burn cleaner and longer than petroleum-based paraffin candles. They are non-toxic, biodegradable, and release zero carbon soot!"
        elif 'membership' in message or 'premium' in message or 'discount' in message:
            response = "NatureCart Premium gives you access to custom AI shopping lists, exclusive discounts, and partner manufacturer promotions. You can upgrade directly from your Dashboard settings!"
        else:
            response = "That is a great question! Sustainable living is a journey of small, conscious choices. Try looking up sustainable alternatives using our Alternative Finder, or browse our categories to make your next green choice."
            
        return JsonResponse({"response": response})
        
    return JsonResponse({"error": "Invalid request method"}, status=400)

# AI Alternatives Finder API
def alternatives_api(request):
    query = request.GET.get('query', '').strip()
    results = []
    
    if query:
        # Search the plastic alternative database
        alternatives = PlasticAlternative.objects.filter(
            Q(plastic_product_name__icontains=query) |
            Q(alternative_product__name__icontains=query)
        )
        
        for alt in alternatives:
            # Check if there is an image
            image_url = ""
            if alt.alternative_product.images.first():
                image_url = alt.alternative_product.images.first().image.url
                
            results.append({
                "plastic_name": alt.plastic_product_name,
                "alt_name": alt.alternative_product.name,
                "alt_id": alt.alternative_product.id,
                "alt_price": str(alt.alternative_product.price),
                "alt_image": image_url,
                "co2_savings": str(alt.co2_savings),
                "plastic_savings": str(alt.plastic_savings),
                "reasoning": alt.reasoning
            })
            
        # If no strict database match, do a simple category match or default suggestion
        if not results:
            # Let's see if we can search products directly
            matched_products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )[:2]
            
            for prod in matched_products:
                image_url = ""
                if prod.images.first():
                    image_url = prod.images.first().image.url
                    
                results.append({
                    "plastic_name": f"Plastic {query}",
                    "alt_name": prod.name,
                    "alt_id": prod.id,
                    "alt_price": str(prod.price),
                    "alt_image": image_url,
                    "co2_savings": str(prod.co2_saving_weight),
                    "plastic_savings": str(prod.plastic_saving_weight),
                    "reasoning": f"Switching to {prod.name} reduces waste and carbon output. It is a durable, eco-friendly choice for your household."
                })
                
    return JsonResponse({"results": results})


def about(request):
    return render(request, "customer/about.html")

