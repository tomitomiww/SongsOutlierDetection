from enum import Enum

DATA_PATH = r"Data" # the data folder's name.
EXISTING_DATA_PATH =DATA_PATH+r"\\EXISTING_DATA.txt" # the existing data's file path.
STOPWORDS_PATH = DATA_PATH+r"\\STOPWORDS.txt" # the stopwords' list path.
DATA_SEPERATION_CHAR = "@" # separates between data in the same line.

PLT_COLORMAPS = ["viridis", "plasma", "magma", "spring", "twilight"] # plt colormaps' names.
SKIP_LIST = ["EP: ", "remix ", "demo: ", "audiobook: "] # the program's DO-NOT-READ list.


"""
ENUM: DATA_STATUS
Represents an artist's data status:
    1. FULL: the data of the artist is up to date.
    2. SEMI_FULL: the artist's data needs to be updated.
    3. EMPTY: the artist was never inspected.
"""
class DATA_STATUS(Enum):
    FULL = 1
    SEMI_FULL = 2
    EMPTY = 3

"""
ENUM: AD_METHOD
Represents the Anomaly Detection method which is being used:
    1. LOF: Local Outlier Factory.
    2. ISO_FORSET: Isolation Forest.
    3. KMEANS: K-Means algorithm.
    4. WCLOUD: create a word-cloud.
"""
class AD_METHOD(Enum):
    LOF = 1
    ISO_FOREST = 2
    KMEANS = 3
    WCLOUD = 4

# A dictionary to link between AD-METHODS' names and enums.
AD_METHODS_DICT = {'1. Local Outlier Factory': AD_METHOD.LOF,
                   '2. Isolation Forest': AD_METHOD.ISO_FOREST,
                   '3. K-Means algorithm': AD_METHOD.KMEANS,
                   '4. Create a word-cloud': AD_METHOD.WCLOUD}