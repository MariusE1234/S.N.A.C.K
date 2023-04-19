class ProductValidator:
    @staticmethod
    def is_valid_name(name, existing_names, current_product=None):
        if not name:
            return False, "Bitte geben Sie einen Produktnamen ein."
        
        if current_product:
            if name != current_product.name and name in existing_names:
                return False, "Ein Produkt mit diesem Namen existiert bereits."
        else:
            if name in existing_names:
                return False, "Ein Produkt mit diesem Namen existiert bereits."

        return True, ""

    @staticmethod
    def is_valid_image_path(image_path):
        if not image_path:
            return False, "Bitte wählen Sie ein Bild aus."
        return True, ""