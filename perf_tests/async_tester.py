# importing standard modules ==================================================
from typing import List, Tuple
import json, datetime, asyncio


# importing third-party modules ===============================================
import aiohttp
from scipy import spatial


# importing custom modules ====================================================
from utils import load_test_case_file


# module variables ============================================================
INFERENCE_API_HOST: str = "http://localhost:9090"
INFERENCE_MODEL_NAME: str = "mini"


# method definitions ==========================================================
async def run_test_case(str1: str, str2: str, client: aiohttp.ClientSession) -> Tuple[
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

    __ts2__ = datetime.datetime.now()
    print("{:<80}; timestamp: {:>30}; diff: {:>20}"\
        .format(
            "sent request to '{}'".format(url), 
            str(__ts2__), str(__ts2__ - __ts1__))
        )

    async with client.post(
        url, 
        data={
            "data": json.dumps({
                "queries": queries
            })
        }
        ) as response:

        try:
            
            response.raise_for_status()
            vectors: bytes = await response.read()

            __ts3__ =  datetime.datetime.now()
            print("{:<80}; timestamp: {:>30}; diff: {:>20}"\
                .format("received response", str(__ts3__), str(__ts3__ - __ts2__)))

        except Exception as error:
            print("ERROR: {} - {}".format(type(error), str(error)))
            raise
        
        finally:
            response.close()

    # if network code all cool
    vectors = json.loads(vectors.decode("iso-8859-1"))
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



async def run_main() -> None:

    start = datetime.datetime.now()
    data = load_test_case_file()

    async with aiohttp.ClientSession() as client:
        await asyncio.gather(*[run_test_case(s1, s2, client) for s1, s2, _ in data])

    finish = datetime.datetime.now()

    print("Full test of '{}' cases completed in {}".format(len(data), (finish - start)))

    return None


# main ========================================================================
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete( run_main() )
    