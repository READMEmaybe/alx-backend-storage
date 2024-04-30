#!/usr/bin/env python3
""" list all documents in a collection """


def schools_by_topic(mongo_collection, topic):
    """ Retrieves a list of schools from a MongoDB collection
    based on a given topic. """

    return mongo_collection.find({"topics": topic})
