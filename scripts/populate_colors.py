from catalog.models import Color

colors = [
    ("Black", "#000000"),
    ("White", "#FFFFFF"),
    ("Gray", "#808080"),
    ("Light Gray", "#D3D3D3"),
    ("Navy", "#000080"),
    ("Blue", "#0000FF"),
    ("Light Blue", "#ADD8E6"),
    ("Red", "#FF0000"),
    ("Burgundy", "#800020"),
    ("Pink", "#FFC0CB"),
    ("Orange", "#FFA500"),
    ("Yellow", "#FFFF00"),
    ("Green", "#008000"),
    ("Olive", "#808000"),
    ("Khaki", "#F0E68C"),
    ("Brown", "#8B4513"),
    ("Beige", "#F5F5DC"),
    ("Cream", "#FFFDD0"),
    ("Purple", "#800080"),
    ("Lavender", "#E6E6FA"),
]

for name, hex_code in colors:
    Color.objects.get_or_create(name=name, hex_code=hex_code)

print("Colors populated successfully.")
