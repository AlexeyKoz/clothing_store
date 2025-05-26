from catalog.models import Brand

brands = [
    "Abidas",
    "Puima",
    "Nyke",
    "Reebak",
    "Livi’s",
    "H&N",
    "Zarra",
    "Guccy",
    "Kelvin Clain",
    "Tammy Hilviger",
    "Under Armore",
    "Laqoste",
    "Convurse",
    "New Balenzo",
    "Kolumbia",
]

for name in brands:
    Brand.objects.get_or_create(name=name)

print("Brands populated successfully.")
