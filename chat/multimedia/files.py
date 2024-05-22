from datetime import datetime
import os

FILENAME_SCHEMA = "{timestamp}_{filename}"

def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def join_path_with_filename(path, filename):
    return os.path.join(path, filename)

def get_filename_from_schema(file_path):
    return FILENAME_SCHEMA.format(timestamp=datetime.now().strftime('%d%m%Y_%H%M%S'), 
                                filename=os.path.basename(file_path))

async def download_attachment_from_message(message, path):
    create_dir_if_not_exists(path)
    attachment = message.effective_attachment
    file = await attachment.get_file()
    filename = attachment.file_name
    full_path = join_path_with_filename(path, filename)
    await file.download_to_drive(custom_path=full_path)
    return full_path, filename

async def download_file_from_id(bot, file_id, path):
    create_dir_if_not_exists(path)
    file = await bot.get_file(file_id)
    filename = get_filename_from_schema(file.file_path)
    full_path = join_path_with_filename(path, filename)
    await file.download_to_drive(custom_path=full_path)
    return full_path, filename