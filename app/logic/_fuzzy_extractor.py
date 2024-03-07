import os
import logging

from app.configs.config import InternalConfig, configure_logging
from app.utils.decyhper_utils import Cipher

import xml.etree.ElementTree as ET
from langchain_mistralai.chat_models import ChatMistralAI
from langchain import PromptTemplate
from langchain.chains import LLMChain

configure_logging()
logger = logging.getLogger(__name__)


class LLMMixin:
    def get_mistral_model(self, token: str):
        """
        This function decrypts the api key with the provided token, and returns the model

        Args:
            - token : str

        Returns:
            ChatMistralAI (model to perform LLM)
        """
        try:
            decrypted_api_key = Cipher(token).decrypt(InternalConfig.MISTRAL_API_KEY)
            return ChatMistralAI(
                mistral_api_key=decrypted_api_key, model="mistral-small"
            )
        except Exception as exc:
            logger.error(f"Getting model failed... :: {exc}")


class FuzzyLLMKeyFinder(LLMMixin):
    def __init__(self):
        self.template = """
        Given the word, please choose only one of the strings below. Chosen word should have closest meaning. Give me the answer between two asteriks which is * your answer *. If anything that doesn't match, respond *None*. If anything matches, respond *your answer*
        1. Price
        2. DiscountedPrice
        3. ProductType
        4. Quantity
        5. Color
        6. Series
        7. Season
        8. Ürün Bilgisi
        9. Kumaş Bilgisi
        10. Ürün Ölçüleri
        11. Model Ölçüleri
        Here are some examples:
        Given word : "ÜrünBilgisi3", your answer : * Ürün Bilgisi *
        Given word : "Renk", your answer : * Color *
        Given word : "PType", your answer : * ProductType *
        Given word : "Sezon", your answer : * Season *
        Given word : "Qty", your answer : * Quantity *
        Given word : "Ürün Miktarları", your answer : * Quantity *
        Given word : "Union", your answer : * None * . If you think the given word doesn't match to anything, respond "None" You must give me only the string without any explanation.
        Now it's your turn. You must give me only the string without any explanation. No explanation ever. Give me the answer only.
        please choose only one of the strings numerated above. Only give one word. Don't give me more than one answer. Chosen word should have closest meaning and string.
        Given word : "{keyword}", your answer :
        """

    def analyze_key(self, keyword: str, token: str) -> str:
        """
        This function resolves the keyword to get a more meaningful one using Mistral model with the prompt template defined at init function, its an experimental project

        Args:
            - keyword : str
            - token : str (the token to decrypt secret api key)

        Returns:
            - answer : str (the beautified output)
        """
        try:
            model = self.get_mistral_model(token)
            prompt_template = PromptTemplate(
                input_variables=["keyword"],
                template=self.template,
            )
            logger.info(
                "Waiting for an output from the model, this might take a while..."
            )
            chain = LLMChain(llm=model, prompt=prompt_template)
            answer = chain.run(keyword)
            if "None" in answer:
                return None
            else:
                return (
                    answer.replace("* ", "").replace(" *", "").replace("*", "")
                )  # workaround to get a more beautiful output
        except Exception as exc:
            logger.error(f"Error occured while gettin the result from model :: {exc}")


class LLMXMLParser(LLMMixin):
    def __init__(self):
        self.template = """
        Please convert given xml to python. Please only give me the summary, no other comments. Dont ever answer any comment.
        Example : 1) XML File : start of xml * <?xml version="1.0"?>
        <Products>
        <Product ProductId="27356-01" Name="NAKIŞLI ELBİSE">
        <Images>
                <Image Path="www.aday-butik-resim-sitesi/27356-turuncu-1.jpeg"></Image>
                <Image Path="www.aday-butik-resim-sitesi/27356-turuncu-2.jpeg"></Image>
                <Image Path="www.aday-butik-resim-sitesi/27356-turuncu-3.jpeg"></Image>
            </Images>
            <ProductDetails>
            <ProductDetail Name="Price" Value="5,24"/>
            <ProductDetail Name="DiscountedPrice" Value="2,24"/>
            <ProductDetail Name="ProductType" Value="Elbise"/>
            <ProductDetail Name="Quantity" Value="9"/>
            <ProductDetail Name="Color" Value="Turuncu"/>
            <ProductDetail Name="Series" Value="1S-1M-2L-1XL"/>
            <ProductDetail Name="Season" Value="2023 Kış"/>
            </ProductDetails>
            <Description>
        <![CDATA[<ul><li><strong>Ürün Bilgisi:</strong>Kruvaze yaka, uzun kollu, düşük omuzlu, astarlı, crop boy, tam kalıp, düz kesim, blazer ceket</li><li><strong>Kumaş Bilgisi:</strong>%90 Polyester %10 Likra</li><li><strong>Ürün Ölçüleri1:</strong>&nbsp;Boy: 42 cm Kol: 62 cm</li><li><strong>Model Ölçüleri:</strong>&nbsp;Boy: 1.72, Göğüs: 86,&nbsp;Bel: 64, Kalça: 90</li><li>Modelin üzerindeki ürün <strong>S/36</strong>&nbsp;bedendir.</li><li>Bedenler arası +/- sapma olabilir.</li></ul>]]>
        </Description>
        </Product>
        <Product ProductId="27356-02" Name="NAKIŞLI ELBİSE">
        <Images>
                <Image Path="www.aday-butik-resim-sitesi/27356-sarı-1.jpeg"></Image>
                <Image Path="www.aday-butik-resim-sitesi/27356-sarı-2.jpeg"></Image>
                <Image Path="www.aday-butik-resim-sitesi/27356-sarı-3.jpeg"></Image>
            </Images>
            <ProductDetails>
            <ProductDetail Name="Price" Value="5,24"/>
            <ProductDetail Name="DiscountedPrice" Value="5,24"/>
            <ProductDetail Name="ProductType" Value="Elbise"/>
            <ProductDetail Name="Quantity" Value="0"/>
            <ProductDetail Name="Color" Value="Sarı"/>
            <ProductDetail Name="Series" Value="1S-1M-1L-1XL"/>
            <ProductDetail Name="Season" Value="2023 Kış"/>
            </ProductDetails>
            <Description>
        <![CDATA[<ul><li><strong>Ürün Bilgisi: </strong>v yaka, kısa kollu, pamuklu, terletmez, iç göstermez, parlak kumaş, standart boy, düz kesim, tan kalıp, gri tişört</li><li><strong>Kumaş Bilgisi:</strong> %100 Pamuklu</li><li><strong>Ürün Ölçüleri:</strong> Boy: 62 cm</li><li><strong>Model Ölçüleri:</strong> Boy: 1.74, Göğüs: 85, Bel: 64, Kalça: 91</li><li>Modelin üzerindeki ürün <strong>S/36</strong> bedendir.</li><li>Bedenler arası +/- 2cm fark olmaktadır.</li></ul>]]>
        </Description>
        </Product>
        <Product ProductId="62156-01" Name="Büzgü Kollu T-shirt">
        <Images>
                <Image Path="www.aday-butik-resim-sitesi/62156-ekru-1.jpeg"></Image>
                <Image Path="www.aday-butik-resim-sitesi/62156-ekru-2.jpeg"></Image>
                <Image Path="www.aday-butik-resim-sitesi/62156-ekru-3.jpeg"></Image>
            </Images>
            <ProductDetails>
            <ProductDetail Name="Price" Value="3,24"/>
            <ProductDetail Name="DiscountedPrice" Value="0"/>
            <ProductDetail Name="ProductType" Value="T-shirt"/>
            <ProductDetail Name="Quantity" Value="0"/>
            <ProductDetail Name="Color" Value="Ekru"/>
            <ProductDetail Name="Series" Value="1M-1L-1XL"/>
            <ProductDetail Name="Season" Value="2023 Yaz"/>
            </ProductDetails>
            <Description>
        <![CDATA[<ul><li><strong>Ürün Bilgisi: </strong>Yuvarlak yaka, ince askılı, yanı büzgülü, bağcık detaylı, terletmez, likralı kumaş, dar kalıp, dar kesim, crop</li><li><strong>Kumaş Bilgisi:</strong></li><li><strong>Model Ölçüleri:</strong> Boy: 1.73, Kilo: 50, Göğüs: 87, Bel: 63, Kalça: 88</li></ul>]]>
        </Description>
        </Product>
        <Product ProductId="62156-02" Name="Büzgü Kollu T-shirt">
        <Images>
                <Image Path="www.aday-butik-resim-sitesi/62156-vizon-1.jpeg"></Image>
                <Image Path="www.aday-butik-resim-sitesi/62156-vizon-2.jpeg"></Image>
                <Image Path="www.aday-butik-resim-sitesi/62156-vizon-3.jpeg"></Image>
            </Images>
            <Description>
        <![CDATA[<ul><li><strong>Ürün Bilgisi: </strong>Polo yaka, düğmeli, göğüs ve sırt dekolteli, likralı, triko kumaş, likralı, crop boy, dar kalıp, dar kesim, bluz</li><li><strong>Kumaş Bilgisi:</strong> Triko</li><li><strong>Model Ölçüleri:</strong> Boy: 1.73, Kilo: 50, Göğüs: 87, Bel: 63, Kalça: 88</li><li>Modelin üzerindeki ürün <strong>STD</strong> bedendir.</li></ul>]]>
        </Description>
            <ProductDetails>
            <ProductDetail Name="Price" Value="3,24"/>
            <ProductDetail Name="DiscountedPrice" Value="1,24"/>
            <ProductDetail Name="ProductType" Value="T-shirt"/>
            <ProductDetail Name="Quantity" Value="0"/>
            <ProductDetail Name="Color" Value="Vizon"/>
            <ProductDetail Name="Series" Value="1M-1L-1XL"/>
            <ProductDetail Name="Season" Value="2023 Yaz"/>
            </ProductDetails>
        </Product>
        </Products>
        * end of xml
        Needs to be converted to : [{{'ProductId': '27356-01', 'Name': 'NAKIŞLI ELBİSE', 'Images': ['www.aday-butik-resim-sitesi/27356-turuncu-1.jpeg', 'www.aday-butik-resim-sitesi/27356-turuncu-2.jpeg', 'www.aday-butik-resim-sitesi/27356-turuncu-3.jpeg'], 'Price': '5,24', 'DiscountedPrice': '2,24', 'ProductType': 'Elbise', 'Quantity': '9', 'Color': 'Turuncu', 'Series': '1S-1M-2L-1XL', 'Season': '2023 Kış', 'Ürün Bilgisi': 'Kruvaze yaka, uzun kollu, düşük omuzlu, astarlı, crop boy, tam kalıp, düz kesim, blazer ceket', 'Kumaş Bilgisi': '%90 Polyester %10 Likra', 'Ürün Ölçüleri1': 'Boy: 42 cm Kol: 62 cm', 'Model Ölçüleri': 'Boy: 1.72, Göğüs: 86,\xa0Bel: 64, Kalça: 90'}}, {{'ProductId': '27356-02', 'Name': 'NAKIŞLI ELBİSE', 'Images': ['www.aday-butik-resim-sitesi/27356-sarı-1.jpeg', 'www.aday-butik-resim-sitesi/27356-sarı-2.jpeg', 'www.aday-butik-resim-sitesi/27356-sarı-3.jpeg'], 'Price': '5,24', 'DiscountedPrice': '5,24', 'ProductType': 'Elbise', 'Quantity': '0', 'Color': 'Sarı', 'Series': '1S-1M-1L-1XL', 'Season': '2023 Kış', 'Ürün Bilgisi': 'v yaka, kısa kollu, pamuklu, terletmez, iç göstermez, parlak kumaş, standart boy, düz kesim, tan kalıp, gri tişört', 'Kumaş Bilgisi': '%100 Pamuklu', 'Ürün Ölçüleri': 'Boy: 62 cm', 'Model Ölçüleri': 'Boy: 1.74, Göğüs: 85, Bel: 64, Kalça: 91'}}, {{'ProductId': '62156-01', 'Name': 'Büzgü Kollu T-shirt', 'Images': ['www.aday-butik-resim-sitesi/62156-ekru-1.jpeg', 'www.aday-butik-resim-sitesi/62156-ekru-2.jpeg', 'www.aday-butik-resim-sitesi/62156-ekru-3.jpeg'], 'Price': '3,24', 'DiscountedPrice': '0', 'ProductType': 'T-shirt', 'Quantity': '0', 'Color': 'Ekru', 'Series': '1M-1L-1XL', 'Season': '2023 Yaz', 'Ürün Bilgisi': 'Yuvarlak yaka, ince askılı, yanı büzgülü, bağcık detaylı, terletmez, likralı kumaş, dar kalıp, dar kesim, crop', 'Kumaş Bilgisi': '', 'Model Ölçüleri': 'Boy: 1.73, Kilo: 50, Göğüs: 87, Bel: 63, Kalça: 88'}}, {{'ProductId': '62156-02', 'Name': 'Büzgü Kollu T-shirt', 'Images': ['www.aday-butik-resim-sitesi/62156-vizon-1.jpeg', 'www.aday-butik-resim-sitesi/62156-vizon-2.jpeg', 'www.aday-butik-resim-sitesi/62156-vizon-3.jpeg'], 'Price': '3,24', 'DiscountedPrice': '1,24', 'ProductType': 'T-shirt', 'Quantity': '0', 'Color': 'Vizon', 'Series': '1M-1L-1XL', 'Season': '2023 Yaz', 'Ürün Bilgisi': 'Polo yaka, düğmeli, göğüs ve sırt dekolteli, likralı, triko kumaş, likralı, crop boy, dar kalıp, dar kesim, bluz', 'Kumaş Bilgisi': 'Triko', 'Model Ölçüleri': 'Boy: 1.73, Kilo: 50, Göğüs: 87, Bel: 63, Kalça: 88'}}]
        Here's the xml file : start of xml * {xml_file_string} * end of xml
        Your answer as a Python list :
        """

    def parse_xml(self, token: str) -> list:
        """
        This function gets the mistral model via decrypting the secret api key and returns a more meaningful dict regarding the template

        Args:
            - token : str

        Returns:
            - a list of dict containing the data
        """
        try:
            model = self.get_mistral_model(token)
            # Read the XML from assets folder
            tree = ET.parse(
                os.path.join(InternalConfig.ASSETS_DIR_PATH, "lonca-sample.xml")
            )
            root = tree.getroot()
            # Convert XML file to string
            xml_string = ET.tostring(root, encoding="utf8", method="xml").decode()
            prompt_template = PromptTemplate(
                input_variables=["xml_string"],
                template=self.template,
            )
            logger.info(
                "Waiting for an output from the model, this might take a while..."
            )
            chain = LLMChain(llm=model, prompt=prompt_template)
            answer = chain.run(xml_string)
            return answer
        except Exception as exc:
            logger.error(
                f"Error occured while getting the answer for LLM parser... :: {exc}"
            )
