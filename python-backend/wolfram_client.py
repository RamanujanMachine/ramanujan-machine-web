import json

import requests

from secrets import Secrets


class WolframClient:

    @staticmethod
    def ask(query: str) -> str:
        """
        Invoke the Wolfram Alpha Results API which will allow us to perform various mathematical calculations to
        cross-check our results. Refer to https://products.wolframalpha.com/api/documentation for usage.
        :return: result of wolfram query in JSON
        """
        try:
            result = requests.get("https://api.wolframalpha.com/v2/query",
                                  params={"appid": Secrets.WolframAppId,
                                          "input": query,
                                          "output": "json"})
        except Exception as e:
            print("Wolfram API returned error", e)
        else:
            try:
                return json.loads(result.content)
            except Exception as e:
                print("Failed to parse Wolfram API result", e)

    @staticmethod
    def limit(fraction: str) -> str:
        return WolframClient.ask(query="limit of {}".format(fraction))
