import os
import requests
import logging
import page_loader.resourse

logging.basicConfig(level=logging.INFO)


def download(url, output=os.getcwd()):
    html_name = page_loader.resourse.make_name(url)
    html_path = os.path.join(output, html_name)
    file_folder_name = page_loader.resourse.make_name(url, is_dir=True)
    file_folder_path = os.path.join(output, file_folder_name)

    logging.info(f"GET {url}")
    response = requests.get(url)
    response.raise_for_status()
    logging.info("Done.")

    logging.info(f"MAKE RESOURCES DIR AT: '{file_folder_path}'")
    if not os.path.exists(file_folder_path):
        os.mkdir(file_folder_path)
    logging.info("Done.")

    logging.info("Preparing resources...")
    resources, html = page_loader.resourse.prepare(
        response.text, url, file_folder_name)
    logging.info("Done.")

    logging.info("Downloading resources:")
    for resource in resources:
        page_loader.resourse.download(resource, output)
    logging.info("Done.")

    logging.info(f"Saving html to {html_path}")
    page_loader.resourse.save(html, html_path)
    page_loader.resourse.save(html, html_path)
    logging.info("Done.")
    return html_path
