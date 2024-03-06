import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

class Extractor:
    def _extract_from_description(self, description_data):
        soup = BeautifulSoup(description_data, 'html.parser')

        # Extract text from <li> tags
        items = [item.get_text(strip=True) for item in soup.find_all('li')]

        # Create a dictionary
        info_dict = {}
        for item in items:
            parts = item.split(':', 1)  # Split at the first occurrence of ':'
            if len(parts) == 2:
                key, value = parts
                info_dict[key.strip()] = value.strip()

        return info_dict

    def extract(self):
        # Parse the XML file
        tree = ET.parse('assets/lonca-sample.xml')
        root = tree.getroot()

        # Create a list to store the dictionaries for each product
        products_list = []

        # Iterate over each product
        for product in root.findall('Product'):
            product_dict = {}

            # Extract ProductId and Name
            product_dict['ProductId'] = product.get('ProductId')
            product_dict['Name'] = product.get('Name')

            # Extract Images
            images = product.find('Images')
            if images is not None:
                image_paths = [image.get('Path') for image in images.findall('Image')]
                product_dict['Images'] = image_paths

            # Extract ProductDetails
            details = product.find('ProductDetails')
            if details is not None:
                product_details = {detail.get('Name'): detail.get('Value') for detail in details.findall('ProductDetail')}
                product_dict.update(product_details)

            # Extract Description
            description = product.find('Description')
            if description is not None:
                description_dict = self._extract_from_description(description.text.strip())
                product_dict.update(description_dict)


            # Add the product dictionary to the products list
            products_list.append(product_dict)
        breakpoint()
        x = 2
