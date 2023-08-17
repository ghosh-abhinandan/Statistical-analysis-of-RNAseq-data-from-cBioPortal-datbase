import time
import requests as rq
from requests.exceptions import HTTPError
import pandas as pd

# record start time
start = time.time()

gene_symbols = ["AURKA", "PTCH1", "SUFU", "INPP5E", "IFT20", "IFT88", "IFT122"]
molecular_profile_name = "mRNA expression (RNA Seq V2 RSEM)"

##### Get All gene IDs #####
print("Fetching All Gene IDs")
try:
    response = rq.get(
        f"https://www.cbioportal.org/api/genes",
        params={
            "pageNumber": 0,
            "direction": "ASC",
            "pageSize": 10000000,
            "projection": "ID",
        },
    )
    response.raise_for_status()
except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")
else:
    gene_ids: list[dict] = response.json()
print(f"Total number of Gene IDs fetched: {len(gene_ids)}")

##### Get Study IDs from keyword #####
try:
    response = rq.get(
        "https://www.cbioportal.org/api/studies",
        params={
            "direction": "ASC",
            "keyword": "Ovarian Serous Cystadenocarcinoma (TCGA, Firehose Legacy)",
            "pageNumber": 0,
            "pageSize": 10000000,
            "projection": "SUMMARY",
        },
    )
    response.raise_for_status()
except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")
else:
    studies: list = response.json()

##### Get Neoplasm Histologic Grade for each study #####
print("Fetching Neoplasm Histologic Grade for each study:")
clinical_datas = []
for study in studies:
    if study["studyId"] == "ov_tcga":
        clinical_data_type = "PATIENT"
    else:
        clinical_data_type = "SAMPLE"
    try:
        response = rq.get(
            f"https://www.cbioportal.org/api/studies/{study['studyId']}/clinical-data",
            params={
                "attributeId": "GRADE",
                "clinicalDataType": clinical_data_type,
                "direction": "ASC",
                "pageSize": 10000000,
                "projection": "SUMMARY",
            },
        )
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        clinical_datas.append(response.json())
        print(f"{study['name']}: {len(response.json())}")

##### Get Molecular Profile for each study #####
molecular_profile_ids = []
for study in studies:
    try:
        response = rq.get(
            f"https://www.cbioportal.org/api/studies/{study['studyId']}/molecular-profiles",
            params={
                "keyword": "mRNA expression (RNA Seq V2 RSEM)",
                "direction": "ASC",
                "pageSize": 10000000,
                "projection": "SUMMARY",
            },
        )
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        for molecular_profile in response.json():
            if molecular_profile["name"] == molecular_profile_name:
                molecular_profile_ids.append(molecular_profile["molecularProfileId"])
                break

##### Get Molecular Data for each study #####
print("Fetching Molecular Data for each study:")
molecular_datas: dict[str, list] = {}
for gene in gene_symbols:
    molecular_datas[gene] = []
for gene in gene_ids:
    if gene["hugoGeneSymbol"] in gene_symbols:
        for study in studies:
            for molecular_id in molecular_profile_ids:
                try:
                    response = rq.get(
                        f"https://www.cbioportal.org/api/molecular-profiles/{molecular_id}/molecular-data",
                        params={
                            "entrezGeneId": gene["entrezGeneId"],
                            "projection": "SUMMARY",
                            "sampleListId": f"{study['studyId']}_all",
                        },
                    )
                    response.raise_for_status()
                except HTTPError as http_err:
                    print(f"HTTP error occurred: {http_err}")
                except Exception as err:
                    print(f"Other error occurred: {err}")
                else:
                    molecular_datas[gene["hugoGeneSymbol"]] = response.json()
                    print(f"{gene['hugoGeneSymbol']}:\t{len(response.json())}")
    else:
        continue


# clinicalDF = pd.read_json("./clinicalData.json")
clinical_df = pd.DataFrame.from_dict(clinical_datas[0])
# print(clinicalDF.info())

for gene in gene_symbols:
    molecular_df = pd.DataFrame.from_dict(molecular_datas["AURKA"])

    mergedDF = pd.merge(
        clinical_df, molecular_df, left_on="patientId", right_on="patientId"
    )

    mergedDF.to_csv(f"{gene}.csv")

# record end time
end = time.time()

print("The time of execution of above program is :", (end - start) * 10**3, "ms")
