#libraries-imports
from layer2.interfaces import IProductValidator

class DefaultProductValidator(IProductValidator):
    @staticmethod
    def is_valid_name(name, existing_names, current_product=None):
        if not name:
            return False, "Der Produktname darf nicht leer sein."
        if name in existing_names and (current_product is None or current_product.name != name):
            return False, "Der Produktname ist bereits vorhanden."
        return True, ""

    @staticmethod
    def is_valid_image_path(image_path):
        if not image_path:
            return False, "Ein Bild muss ausgewählt werden."
        return True, ""
