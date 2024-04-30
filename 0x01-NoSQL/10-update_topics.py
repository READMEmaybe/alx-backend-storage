#!/usr/bin/env python3
""" update topics in a document """


def update_topics(mongo_collection, name, topics):
    """
    Update the topics field for documents in the given mongo_collection
    that match the specified name.
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
