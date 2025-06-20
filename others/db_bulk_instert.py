from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine, text

load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
driver = "ODBC Driver 17 for SQL Server"

connection_string = (
    f"mssql+pyodbc://{username}:{password}@{server}/{database}"
    f"?driver={driver}"
)
engine = create_engine(connection_string)

data = {
    "closing_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "closing_tag": [2504, 2503, 2502, 2501, 2412, 2411, 2410, 2409, 2408, 2407, 2406, 2405, 2404, 2403, 2402],
    "md_bonus": [8651180, 5305505, 5947330, 8596171, 34079155, 8419338, 6057767, 5480741, 7772995, 8570917, 8836516, 6541392, 5092733, 8984268, 5412519],
    "dc_bonus": [7100237, 6298313, 5140614, 5214618, 5508183, 5787535, 7930374, 7521863, 6323841, 5580907, 6019349, 8449748, 6233862, 7282307, 7703841],
    "total_bonus": [15751417, 11603818, 11087944, 13810789, 39587338, 14206873, 13988141, 13002604, 14096836, 14151824, 14855865, 14991140, 11326595, 16266575, 13116360],
    "trc_so_target": [26611, 22932, 21967, 22418, 27717, 21504, 23616, 21603, 26347, 26928, 20372, 24452, 27942, 22437, 24734],
    "trc_so_ach": [21551, 18231, 21425, 16772, 35432, 16985, 16956, 18563, 22122, 19283, 18475, 23257, 26134, 18617, 15608],
    "vdf_so_target": [33141, 28540, 25569, 31914, 34843, 30416, 27672, 31982, 27855, 26710, 30495, 32030, 31709, 30884, 30196],
    "vdf_so_ach": [20222, 20336, 22868, 23740, 32718, 23836, 21867, 20162, 24338, 23664, 22979, 24263, 27109, 24693, 25439],
    "tt_so_target": [15727, 12405, 14926, 18415, 14257, 14945, 13824, 15631, 17606, 10189, 15247, 10415, 13807, 19751, 18803],
    "tt_so_ach": [12398, 11060, 13083, 13170, 8988, 12352, 12535, 10654, 14317, 8645, 8668, 8741, 9009, 18604, 16798],
    "extra_model_agreement": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0],
    "closing_month": pd.to_datetime([
        "2025-04-01", "2025-03-01", "2025-02-01", "2025-01-01",
        "2024-12-01", "2024-11-01", "2024-10-01", "2024-09-01",
        "2024-08-01", "2024-07-01", "2024-06-01", "2024-05-01",
        "2024-04-01", "2024-03-01", "2024-02-01"
    ])
}

df = pd.DataFrame(data)

try:
    df.to_sql("xiaomi_closing_data", engine, if_exists="append", index=False)
    print("Data inserted successfully!")
except Exception as e:
    print(f"Data insertion failed: {e}")
