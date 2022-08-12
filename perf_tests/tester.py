# importing standard modules ==================================================
from typing import List, Tuple
import json, datetime


# importing third-party modules ===============================================
import requests
from scipy import spatial


# importing custom modules ====================================================
from utils import load_test_case_file


# module variables ============================================================
INFERENCE_API_HOST: str = "http://localhost:9090"
INFERENCE_MODEL_NAME: str = "mini"


# method definitions ==========================================================
def run_test_case(str1: str, str2: str) -> Tuple[
    float, 
    Tuple[
        datetime.datetime, 
        datetime.datetime, 
        datetime.datetime, 
        datetime.datetime, 
        datetime.datetime
    ]
    ]:
    r""" Gets the score for a single test case """

    __ts1__ =  datetime.datetime.now()
    print(
        "{:<80}; timestamp: {:>30}".format("started 'run_main'", str(__ts1__))
    )

    template_url: str = "{}/predictions/{}"
    url: str = template_url.format(
        INFERENCE_API_HOST, INFERENCE_MODEL_NAME
    )

    queries: List[str] = [str1, str2]

    try:
        __ts2__ = datetime.datetime.now()
        print("{:<80}; timestamp: {:>30}; diff: {:>20}"\
            .format(
                "sent request to '{}'".format(url), 
                str(__ts2__), str(__ts2__ - __ts1__))
            )


        response: requests.Response = requests.post(
            url, 
            data={
                "data": json.dumps({
                    "queries": queries
                })
            }
        )


        __ts3__ =  datetime.datetime.now()
        print("{:<80}; timestamp: {:>30}; diff: {:>20}"\
            .format("received response", str(__ts3__), str(__ts3__ - __ts2__)))


        response.raise_for_status()
        vectors: List = response.json()

    except Exception as error:
        print("ERROR: {} - {}".format(type(error), str(error)))
        raise

    # if network code all cool
    similarity_score: float = 1 - spatial.distance.cosine(vectors[0], vectors[1])

    __ts4__ = datetime.datetime.now()
    print("{:<80}; timestamp: {:>30}; diff: {:>20}"\
        .format("calculated similarity", str(__ts4__), str(__ts4__ - __ts3__)))

    __ts5__ = datetime.datetime.now()
    print("{:<80}; timestamp: {:>30}; diff: {:>20}"\
        .format("finished test case", str(__ts5__), str(__ts5__ - __ts1__)))
    
    print("===================================================================="
    "\nSimilarity score for\n{} = {}".format(queries, similarity_score))

    return similarity_score, (__ts1__, __ts2__, __ts3__, __ts4__, __ts5__)



def run_main() -> None:
    
    data = load_test_case_file()

    start = datetime.datetime.now()
    for s1, s2, _ in data:
        score, _stamps_ = run_test_case(s1, s2)
        t1, t2, t3, t4, t5 = _stamps_
    finish = datetime.datetime.now()

    print("Full test of '{}' cases completed in {}".format(len(data), (finish - start)))

    return None


# main ========================================================================
if __name__ == "__main__":
    run_main()