from datetime import datetime
import re
import os

from app.database.mongo_odm import Product
from app.configs.config import InternalConfig

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


class Extractor:
    def _extract_size_info_from_extras(self, info_list):
        try:
            for item in info_list:
                match = re.search(r"ürün(.*?)bedendir", item)

                if match:
                    extracted_text = match.group(1)
                    return extracted_text
        except:
            return None

    def _extract_from_description(self, description_data: str) -> dict:
        try:
            soup = BeautifulSoup(description_data, "html.parser")

            # Extract text from <li> tags
            items = [item.get_text(strip=True) for item in soup.find_all("li")]

            # Create a dictionary
            info_dict = {"additional_info": []}
            for item in items:
                parts = item.split(":", 1)  # Split at the first occurrence of ':'
                if len(parts) == 2:
                    key, value = parts
                    info_dict[key.strip()] = value.strip()
                else:
                    info_dict["additional_info"] = info_dict["additional_info"] + [item]

            return info_dict
        except Exception as exc:
            raise TypeError(
                f"Something went wrong during Description data extraction :: {exc}"
            )

    def _extract_data_from_xml_file(
        self,
        xml_path,
    ):
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Create a list to store the dictionaries for each product
        products_list = []

        # Iterate over each product
        for product in root.findall("Product"):
            images = product.find("Images")
            if images is not None:
                image_paths = [image.get("Path") for image in images.findall("Image")]

            details = product.find("ProductDetails")
            if details is not None:
                product_details = {
                    detail.get("Name"): detail.get("Value")
                    for detail in details.findall("ProductDetail")
                }

            description = product.find("Description")
            if description is not None:
                description_dict = self._extract_from_description(
                    description.text.strip()
                )

            # Make a dynamic solution for Ürün Ölçümleri case
            def return_valid_key(_key, _dict):
                for __key in _dict.keys():
                    if _key in __key:
                        return __key
                    else:
                        None

            # Converting float to handle the cases like "2,24"
            def convert_to_float(_variable):
                try:
                    if "," in _variable or "." in _variable:
                        return float(_variable.replace(",", "."))
                    elif isinstance(_variable, int):
                        return float(_variable)
                    elif isinstance(_variable, str):
                        return float(_variable)
                    else:
                        return _variable
                except Exception as exc:
                    raise TypeError(
                        f"Error while converting variable:{_variable} :: {exc}"
                    )

            now = datetime.now()
            formatted_now = now.strftime("%Y-%m-%dT%H:%M:%S.%f+00:0")
            product_dict = {
                "stock_code": product.get("ProductId", "N/A"),
                "color": [product_details.get("Color", "N/A")],
                "discounted_price": convert_to_float(
                    product_details.get("DiscountedPrice", "N/A")
                ),
                "images": image_paths,
                "is_discounted": (
                    True
                    if convert_to_float(product_details.get("DiscountedPrice", 0))
                    < convert_to_float(product_details.get("Price", 0))
                    else False
                ),
                "name": product.get("Name", "N/A"),
                "price": convert_to_float(product_details.get("Price", "N/A")),
                "price_unit": "USD",  # Couldn't find any logical way to get the unit.
                "product_type": product_details.get("ProductType", "N/A"),
                "quantity": int(product_details.get("Quantity", "N/A")),
                "sample_size": self._extract_size_info_from_extras(
                    description_dict.get("additional_info", "N/A")
                ),
                "series": product_details.get("Series", "N/A"),
                "status": (
                    "Active"
                    if int(product_details.get("Quantity", 0)) > 0
                    else "Deactive"
                ),
                "fabric": description_dict.get(
                    return_valid_key("Kumaş Bilgisi", description_dict), "N/A"
                ),
                "model_measurements": description_dict.get(
                    return_valid_key("Model Ölçüleri", description_dict), "N/A"
                ),
                "product_measurements": description_dict.get(
                    return_valid_key("Ürün Ölçüleri", description_dict), "N/A"
                ),
                "createdAt": formatted_now,
                "updatedAt": formatted_now,
                "file_path": xml_path,
            }
            products_list.append(product_dict)

        return products_list

    def _save_product_docs_to_mongo(self, products_list):
        try:
            for product_doc in products_list:
                matched_documents = Product.objects(
                    stock_code=product_doc["stock_code"]
                )
                if not matched_documents:
                    mongo_product_doc = Product(**product_doc)
                    mongo_product_doc.save()

        except Exception as exc:
            raise TypeError(f"Error while saving documents to db... :: {exc}")

    def extract(self, file_name):
        if file_name.endswith(".xml"):
            products_list = self._extract_data_from_xml_file(
                os.path.join(InternalConfig.ASSETS_DIR_PATH, file_name)
            )
            self._save_product_docs_to_mongo(products_list)
        else:
            raise TypeError(f"The requested file is not in XML format...")

    def extract_periodically(self):
        directory_list = os.listdir(InternalConfig.ASSETS_DIR_PATH)
        xml_paths = [
            os.path.join(InternalConfig.ASSETS_DIR_PATH, file)
            for file in directory_list
            if file.endswith(".xml")
        ]
        unique_names = Product.objects.distinct("file_path")
        unrecognized_files_list = list(set(xml_paths) - set(unique_names))
        for file_path in unrecognized_files_list:
            product_list = self._extract_data_from_xml_file(file_path)
            self._save_product_docs_to_mongo(product_list)
