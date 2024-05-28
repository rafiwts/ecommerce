from django.db import transaction
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .handlers import generate_unique_slug
from .models import Category, ChildSubcategory, Subcategory


@receiver(post_migrate)
def create_categories_and_subcategories(sender, **kwargs):
    if not Category.objects.exists():
        # define categories and their subcategories
        category_structure = {
            "Electronics": {
                "Mobile Phones": ["Smartphones", "Basic phones", "Feature phones"],
                "Laptops": [
                    "Notebooks",
                    "Tablets",
                    "Chromebook",
                    "Macbook",
                    "Ultrabook",
                ],
                "Cameras": ["Compact cameras", "Film cameras", "Bridge cameras"],
                "TV Sets": ["LED", "OLED", "QLED", "Smart TV", "8K TV"],
            },
            "Clothing": {
                "Men": [
                    "Shirts",
                    "Pants",
                    "Jackets",
                    "Suits",
                    "Underwear",
                    "Sportswear",
                ],
                "Women": [
                    "Dresses",
                    "Tops",
                    "Skirts",
                    "Jackets",
                    "Lingerie",
                    "Sportswear",
                ],
                "Kids": [
                    "T-shirts",
                    "Pants",
                    "Dresses",
                    "Jackets",
                    "School Uniforms",
                    "Sportswear",
                ],
            },
            "Books": {
                "Fiction": ["Fantasy", "Science Fiction", "Mystery", "Romance"],
                "Non-Fiction": ["Biographies", "Self-help", "History", "Science"],
                "Comics": ["Manga", "Graphic Novels", "Superhero Comics"],
                "Biographies": ["Historical", "Celebrity", "Political"],
                "Textbooks": ["School", "College", "Professional"],
                "Self-help": ["Motivational", "Psychology", "Health"],
                "Children's Books": ["Picture Books", "Young Adult", "Educational"],
            },
            "Toys": {
                "Action Figures": ["Superheroes", "Anime", "Movies"],
                "Puzzles": ["Jigsaw Puzzles", "3D Puzzles", "Brain Teasers"],
                "Dolls": ["Fashion Dolls", "Baby Dolls", "Collectible Dolls"],
                "Educational Toys": ["STEM Toys", "Learning Games", "Building Sets"],
                "Board Games": ["Strategy Games", "Family Games", "Party Games"],
                "Outdoor Toys": ["Swings", "Slides", "Trampolines"],
            },
            "Health": {
                "Vitamins": ["Multivitamins", "Vitamin D", "Vitamin C"],
                "Supplements": ["Protein Powder", "Herbal Supplements", "Omega-3"],
                "Medical Equipment": [
                    "Blood Pressure Monitors",
                    "Thermometers",
                    "Wheelchairs",
                ],
                "First Aid": ["Bandages", "Antiseptics", "First Aid Kits"],
                "Personal Care": ["Skincare", "Haircare", "Oral Care"],
                "Fitness Equipment": ["Treadmills", "Dumbbells", "Yoga Mats"],
            },
            "Food": {
                "Snacks": ["Chips", "Nuts", "Chocolate"],
                "Beverages": ["Soda", "Juice", "Coffee", "Tea"],
                "Groceries": ["Fruits", "Vegetables", "Dairy", "Meat"],
                "Organic": ["Organic Fruits", "Organic Vegetables", "Organic Meat"],
                "Gourmet": ["Cheese", "Caviar", "Truffles"],
                "Frozen Food": ["Frozen Vegetables", "Ice Cream", "Frozen Meals"],
            },
            "Sport Equipment": {
                "Fitness": ["Treadmills", "Exercise Bikes", "Weights"],
                "Outdoor": ["Camping Gear", "Hiking Gear", "Cycling"],
                "Indoor": ["Table Tennis", "Darts", "Indoor Basketball"],
                "Team Sports": ["Soccer", "Basketball", "Baseball"],
                "Water Sports": ["Swimming", "Surfing", "Diving"],
                "Winter Sports": ["Skiing", "Snowboarding", "Ice Skating"],
            },
            "Video Games": {
                "Consoles": ["PlayStation", "Xbox", "Nintendo"],
                "PC": ["Gaming Laptops", "Gaming Desktops", "PC Games"],
                "Accessories": ["Controllers", "Headsets", "VR Headsets"],
                "Games": ["Action", "Adventure", "RPG", "Simulation"],
                "Virtual Reality": ["VR Headsets", "VR Games", "VR Accessories"],
                "Handhelds": ["Nintendo Switch", "PlayStation Vita", "Retro Handhelds"],
            },
            "Home": {
                "Furniture": ["Living Room", "Bedroom", "Office", "Outdoor"],
                "Appliances": ["Refrigerators", "Washing Machines", "Microwaves"],
                "Decor": ["Wall Art", "Vases", "Clocks"],
                "Bedding": ["Sheets", "Comforters", "Pillows"],
                "Kitchenware": ["Cookware", "Cutlery", "Dinner Sets"],
                "Garden": ["Furniture", "Plants", "Tools"],
            },
            "Business": {
                "Office Supplies": ["Paper", "Pens", "Folders"],
                "Software": ["Antivirus", "Office Suites", "Graphic Design"],
                "Services": ["Consulting", "Legal", "Marketing"],
                "Furniture": ["Desks", "Chairs", "Storage"],
                "Networking": ["Routers", "Switches", "Cables"],
                "Stationery": ["Notebooks", "Envelopes", "Staplers"],
            },
            "Others": {
                "Miscellaneous": ["Batteries", "Adapters", "Cleaning Supplies"],
                "Gifts": ["Gift Cards", "Gift Baskets", "Personalized Gifts"],
                "Novelties": ["Gag Gifts", "Collectibles", "T-Shirts"],
                "Party Supplies": ["Balloons", "Decorations", "Tableware"],
                "Travel Accessories": ["Luggage", "Travel Pillows", "Adapters"],
            },
        }

        with transaction.atomic():
            # create empty category list
            categories = []

            for category_name in category_structure.keys():
                category_slug = generate_unique_slug(Category, category_name)
                categories.append(Category(name=category_name, slug=category_slug))

            Category.objects.bulk_create(categories)

            # fetch all categories
            category_dict = {
                category.name: category for category in Category.objects.all()
            }

            # create empty subcategories and child subcategories list
            subcategory_instances = []
            child_subcategory_instances = []

            for category_name, subcategories in category_structure.items():
                # get instance from the query
                category = category_dict[category_name]
                # create subcategory and attach it to a category
                for subcategory_name, child_subcategories in subcategories.items():
                    subcategory_slug = generate_unique_slug(
                        Subcategory, subcategory_name
                    )
                    subcategory = Subcategory(
                        name=subcategory_name, slug=subcategory_slug, category=category
                    )
                    subcategory_instances.append(subcategory)
                    # create child subcategory and attach it to subcategory
                    for child_subcategory_name in child_subcategories:
                        child_subcategory_slug = generate_unique_slug(
                            ChildSubcategory, child_subcategory_name
                        )
                        child_subcategory_instances.append(
                            ChildSubcategory(
                                name=child_subcategory_name,
                                slug=child_subcategory_slug,
                                subcategory=subcategory,
                            )
                        )

            Subcategory.objects.bulk_create(subcategory_instances)

            ChildSubcategory.objects.bulk_create(child_subcategory_instances)
