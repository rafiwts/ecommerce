from datetime import datetime


def image_directory_path(instance):
    now = datetime.now()
    return f"{instance.first_name}-{instance.last_name}-{now}"
