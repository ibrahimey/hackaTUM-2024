import json
import requests

from typing import Any, Dict, Optional


class AzureOpenAIClient:
    def __init__(self, endpoint: str, api_key: str) -> None:
        """
        Initializes the AzureOpenAIClient with the specified API endpoint and key.

        :param endpoint: The API URL endpoint to which the client will make requests.
        :param api_key: The API key used for authentication in requests.
        """
        self.endpoint = endpoint
        self.headers = {"Content-Type": "application/json", "api-key": api_key}

    def _parse_response(self, response: requests.Response) -> Any:
        """
        Parses the HTTP response from Azure and extracts the necessary data based on the endpoint.

        :param response: The response object to parse.
        :return: The extracted data from the response JSON, tailored to the specific service interaction.
        """
        if "gpt" in self.endpoint:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return json.loads(response.content.decode("utf-8"))["data"][0]["url"]

    def send_request(self, payload: Dict[str, Any]) -> Optional[Any]:
        """
        Sends a POST request to the configured Azure endpoint with the provided payload.

        :param payload: The JSON-serializable dictionary to send as the request payload.
        :return: The parsed response data if the request is successful, or None if an error occurs.
        """
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return self._parse_response(response)
        except requests.RequestException as e:
            print(f"Failed to make the request. Error: {e}")
            return None

    def send_text_generation_request(
        self, prompt: str, temperature: float = 0.4, top_p: float = 0.95
    ):
        """
        Sends a text generation request to the Azure API with specified parameters to control the style and limits of the generated text.

        :param prompt: The input text prompt for generating the response.
        :param temperature: Controls randomness in text generation. Lower values make the text more predictable, default is 0.4.
        :param top_p: Controls the nucleus sampling, filtering out the least likely options under the cumulative probability top_p, default is 0.95.
        :return: The generated text if the request is successful, or None if an error occurs.
        """
        return self.send_request(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                        ],
                    },
                ],
                "temperature": temperature,
                "top_p": top_p,
            }
        )

    def generate_image(self, prompt: str, size: str = "1024x1024") -> Optional[Any]:
        """
        Sends a request to generate an image based on the provided text prompt and specified size.

        :param prompt: The text prompt describing the desired image.
        :param size: The resolution of the image, default is "1024x1024".
        :return: The image data or URL returned from the API if successful, or None if an error occurs.
        """
        return self.send_request(
            payload={
                "prompt": prompt,
                "size": size,
            }
        )
