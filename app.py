from dotenv import load_dotenv
import os
import json
import requests
import base64

requests.packages.urllib3.disable_warnings()

load_dotenv()

baseEndpoint = os.getenv("BC_BASE_ENDPOINT")
params = "?$top=1"
additionals_params = os.getenv("ADDITIONALS_PARAMS")

if (additionals_params):
    params += "&" + additionals_params

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
encoded_auth_string = base64.b64encode(
    f"{client_id}:{client_secret}".encode()).decode()
authorization_header = f"Basic {encoded_auth_string}"

excluded_keys = [
    "@odata.etag",
    "systemId",
    "systemModifiedAt",
    "systemModifiedBy",
    "systemCreatedAt",
    "systemCreatedBy"
]

excluded_extensions = [
    "png",
    "svg",
    "scss",
    "css",
    "jpg",
    "ico"
]


def query_entity_api_endoint(entity):
    r = requests.get(
        f"{baseEndpoint}/{entity}{params}",
        headers={"Authorization": authorization_header}, verify=False
    )

    data = r.json()['value'][0]
    keys = list(data.keys())
    for key in excluded_keys:
        if key in keys:
            keys.remove(key)

    return keys


def file_is_not_excluded(file):
    return file.split('.')[-1] not in excluded_extensions


def key_found_in_file(root, file, key):
    with open(os.path.join(root, file), encoding="utf-8") as f:
        return key.lower() in f.read().lower()


def clear_logs():
    for root, dirs, files in os.walk("entities"):
        for file in files:
            if file != ".gitignore":
                os.remove(os.path.join(root, file))


with open("targets.json") as f:
    entities = json.load(f)["entities"]

    keys_by_entity = []

    clear_logs()

    for entity in entities:
        keys = query_entity_api_endoint(entity.lower())

        keys_by_entity.append([entity.lower(), [
            [key, False, []] for key in keys
        ]])

        for root, dirs, files in os.walk(os.getenv("ROOT")):
            if "vendor" in root:
                continue

            for file in files:
                if file_is_not_excluded(file):
                    with open(os.path.join(root, file), encoding="utf-8") as f:
                        for key in keys:
                            if key_found_in_file(root, file, key):
                                keys_by_entity[-1][1][keys.index(key)
                                                      ][1] = True
                                keys_by_entity[-1][1][keys.index(
                                    key)][2].append([root, file])

    for entity in keys_by_entity:
        with open(f"entities/{entity[0]}.txt", "w", encoding="utf-8") as f:
            f.write(f"Entity: {entity[0]}\n\n")

            count_of_unused_keys = len(
                [key for key in entity[1] if not key[1]])

            f.write("❌ Unused keys (count: {}):\n".format(count_of_unused_keys))
            for key in entity[1]:
                if not key[1]:
                    f.write(f"- {key[0]}\n")

            f.write("\n\n✅ Used keys:\n")
            for key in entity[1]:
                if key[1]:
                    f.write(f"- {key[0]}\n")
                    for path in key[2]:
                        f.write(f"  - {path[0]}/{path[1]}\n")
