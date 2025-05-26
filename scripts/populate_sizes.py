from catalog.models import Size

sizes = [
    "XS",
    "S",
    "M",
    "L",
    "XL",
    "XXL",
    "3XL",
    "4XL",
    "28",
    "30",
    "32",
    "34",
    "36",
    "38",
    "40",
    "One Size",
]

for name in sizes:
    Size.objects.get_or_create(name=name)

print("Sizes populated successfully.")
