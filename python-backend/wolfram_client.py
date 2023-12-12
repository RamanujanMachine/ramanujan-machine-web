import json

import requests

from secrets import Secrets


class WolframClient:

    @staticmethod
    def ask(query: str, include_pod: str = None) -> str:
        """
        Invoke the Wolfram Alpha Results API which will allow us to perform various mathematical calculations to
        cross-check our results. Refer to https://products.wolframalpha.com/api/documentation for usage.
        :return: result of wolfram query in JSON
        """
        params = {"appid": Secrets.WolframAppId,
                  "input": query,
                  "output": "json",
                  "format": 'plaintext,moutput'}
        if include_pod is not None:
            params["includepodid"] = include_pod
        try:
            # for now we only need the Limit pod, but when add further calculations we will need to specify those pods
            # we are also only asking for plaintext and moutput because by default there is also additional output such
            # as a plot image url, but we are plotting in the frontend
            result = requests.get("https://api.wolframalpha.com/v2/query",
                                  params)
        except Exception as e:
            print("Wolfram API returned error", e)
        else:
            try:
                return json.loads(result.content)
            except Exception as e:
                print("Failed to parse Wolfram API result", e)

    @staticmethod
    def limit(fraction: str) -> str:
        try:
            result = WolframClient.ask(query="limit of {}".format(fraction), include_pod="Limit")
            # only want to return: queryresult -> pods[0] -> subpods
            return result["queryresult"]["pods"][0]["subpods"]
        except Exception as e:
            print("Failed to parse Wolfram API result", e)

    @staticmethod
    def continued_fraction(fraction: str) -> str:
        try:
            result = WolframClient.ask(query="continued fraction representation of {}".format(fraction))
            # only want to return: queryresult -> pods[0] -> subpods
            return result["queryresult"]["pods"][0]["subpods"]
        except Exception as e:
            print("Failed to parse Wolfram API result", e)
