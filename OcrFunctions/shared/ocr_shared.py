"""
Shared code for OCR functions and storage manipulation.
"""

import requests

class AzureOcrService():
    """
    Class for OCR service.
    """
    def __init__(self, ocr_service_url, subscription_key):
        self.ocr_service_url = ocr_service_url
        self.subscription_key = subscription_key

    def get_ocr_results(self, image_url):
        """
        Retrieve results of processing by OCR service.
        """

        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}
        params = {'language': 'unk', 'detectOrientation': 'true'}
        data = {'url': image_url}
        response = requests.post(self.ocr_service_url, headers=headers, params=params, json=data)
        results = response.json()
        return results

    @staticmethod
    def format_ocr_text(ocr_json):
        """
        Formats the OCR text in a neatly readable string.
        """

        line_infos = [region["lines"] for region in ocr_json["regions"]]
        word_infos = []
        for line in line_infos:
            for word_metadata in line:
                for word_info in word_metadata["words"]:
                    word_infos.append(word_info)

        output_array = []
        for word in word_infos:
            text = word["text"]
            output_array.append(text)
        output_text = " ".join(output_array)

        return output_text
