# importing standard modules ==================================================
from typing import Tuple, List
import os, pprint as pp
import pandas


# method definitions ==========================================================
def load_test_case_file() -> List[Tuple[str, str, float]]:
    r""" Load Test Case File 
    - arguments:
    - returns:
        - a list of tuples containing str, str, float
    - raises:
    - notes:
    """

    file_dirname: str = os.path.dirname(__file__)
    path_to_file: str = os.path.join(
        file_dirname, "test_case_files", "Sample Sheet.csv"
    )

    dataframe: pandas.DataFrame = pandas.read_csv(
        path_to_file, index_col=False, names=["t1", "t2", "score"]
    )

    data: List[Tuple[str, str, float]] = [
        (
            str(item.t1).strip(), 
            str(item.t2).strip(), 
            float(str(item.score).strip())
        ) for item in dataframe.itertuples()
    ]
    
    return data



# test main ===================================================================
if __name__ == "__main__":
    x = load_test_case_file()
    print(x)

