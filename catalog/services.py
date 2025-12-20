from catalog.models import Category, Product


class ProductService:

    @staticmethod
    def get_products_in_category(category_id):
        categories = Category.objects.filter(id=category_id)
        if not categories:
            return Product.objects.none()
        return Product.objects.filter(category=categories[0])
