from datetime import datetime


def image_directory_path(instance, filename):
    now = datetime.now()
    full_name = f"{instance.first_name} {instance.last_name}"
    return f"{instance.id}-{full_name}-{now}-{filename}"
