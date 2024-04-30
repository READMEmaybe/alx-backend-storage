#!/usr/bin/env python3
""" Log stats """
from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    This function prints various statistics about the logs stored in the
    specified MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection):
                    The MongoDB collection containing the logs.
    """
    print(f"{mongo_collection.estimated_document_count()} logs")
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    status = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status} status check")
    print("IPs:")
    ips = mongo_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip in ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats(MongoClient()['logs']['nginx'])
