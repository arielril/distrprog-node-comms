import string
import random
from os import path, getcwd


resource_folders = [
    "node1",
    "node2",
    "node3",
]
file_qty = 5


def get_random_string(size=6):
    return "".join(
        random.SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        )
        for _ in range(size)
    )


for folder in resource_folders:
    for _ in range(file_qty):
        file_suffix = get_random_string()
        file_path = path.join(
            getcwd(),
            "..",
            "code",
            "app",
            "resources",
            folder,
            f"resource_{file_suffix}",
        )
        f = open(file_path, "w")
        f.write(
            get_random_string(60),
        )
        f.close()
