"""
Shared code for OCR functions and storage manipulation.
"""

import requests

class AzureOcrService(object):
    """
    Class for OCR service.
    """
    def get_ocr_results(self, ocr_service_url, subscription_key, image_url):
        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        params = {'language': 'unk', 'detectOrientation': 'true'}
        data = {'url': image_url}
        response = requests.post(ocr_service_url, headers=headers, params=params, json=data)
        results = response.json()
        return results

    def process_ocr_text(self, ocr_json):
        line_infos = [region["lines"] for region in ocr_json["regions"]]
        word_infos = []
        for line in line_infos:
            for word_metadata in line:
                for word_info in word_metadata["words"]:
                    word_infos.append(word_info)

        output_text = ""
        for word in word_infos:
            text = word["text"]
            output_text = output_text + " " + text

        return output_text
