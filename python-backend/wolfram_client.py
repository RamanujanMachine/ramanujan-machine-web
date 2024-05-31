"""
Specific queries to the Wolfram results API and a generic ask() function to invoke the API
"""
import json
import logging
from json import JSONDecodeError

import requests

from constants import WOLFRAM_CHAR_LIMIT
from custom_exceptions import APIError
from custom_secrets import CustomSecrets

logger = logging.getLogger('rm_web_app')


class WolframClient:
    """
    Operations against the Wolfram API
    """

    @staticmethod
    def ask(query: str, include_pod: str = None) -> dict:
        """
        Invoke the Wolfram Alpha Results API which will allow us to perform various mathematical calculations to
        cross-check our results. Refer to https://products.wolframalpha.com/api/documentation for usage.
        :return: result of wolfram query in JSON
        """
        params = {"appid": CustomSecrets.WolframAppId,
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
            logger.error("Wolfram API returned error", e)
        else:
            try:
                result = json.loads(result.content)
                logger.debug(result)
                try:
                    raise APIError(result["queryresult"]["error"]["msg"])
                except (AttributeError, TypeError):
                    # if the key does not exist or is false then the api call was successful
                    pass
                return result
            except JSONDecodeError as e:
                logger.error("Failed to parse Wolfram API result", e)

    @staticmethod
    def closed_form(expression: str) -> dict:
        """
        Query the Wolfram results API for limits of a string expression
        :param expression: Mathematical expression for which we would like to compute the limit(s)
        :return: Wolfram API response "subpods" with the computed limit(s)
        """
        try:
            # Wolfram has a 200 character input limit
            assert len(expression) <= WOLFRAM_CHAR_LIMIT
        except AssertionError:
            logger.warning("Truncating decimal value to 200 characters to keep within Wolfram API query limit")

        try:
            result = WolframClient.ask(query=expression[:WOLFRAM_CHAR_LIMIT], include_pod="PossibleClosedForm")
            # only want to return: queryresult -> pods[0] -> subpods
            # infos has metadata on the subpods e.g. the constant names and links to reference content
            # Note: the index of the infos does not line up with the index of the closed form results
            subpods = result["queryresult"]["pods"][0]["subpods"]
            meta = result["queryresult"]["pods"][0].get("infos", [])
            return {"closed_forms": subpods, "metadata": meta}
        except Exception as e:
            logger.error("Failed to obtain Wolfram API result", e)
