from elasticsearch import Elasticsearch
from datetime import date, datetime, time

# Your Elasticsearch credentials
ELASTICSEARCH_USER = 'elastic'
ELASTICSEARCH_PASS = 'WgLVWv0vE*Z+Xv8L50Mr'

# Elasticsearch configuration with authentication
es = Elasticsearch(
    hosts=[{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],
    basic_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASS)  # Use basic_auth for authentication
)
index_name = "news"

# Test the connection by checking the cluster health
try:
    cluster_health = es.cluster.health()
    print("Connected to Elasticsearch cluster:", cluster_health['cluster_name'])
except Exception as e:
    print("Error connecting to Elasticsearch:", e)


def query_news_count_by_category_today(current_date):

    # Get the date range for today
    start_time = datetime.combine(current_date, time.min)
    end_time = datetime.combine(current_date, time.max)

    # Format date range for the query
    start_time_str = start_time.strftime("%d-%m-%Y - %I:%M %p")
    end_time_str = end_time.strftime("%d-%m-%Y - %I:%M %p")

    body = {
        "from" : 0, "size" : 1000,
        "query": {
            "bool": {
                "filter": {
                    "range": {
                        "Created": {
                            "gte": start_time_str,
                            "lte": end_time_str
                        }
                    }
                }
            }
        },
        "aggs": {
            "news_by_category": {
                "terms": {
                    "field": "Category",
                    "size": 20
                }
            }
        }
    }

    try:
        # Execute the query
        result = es.search(
            index=index_name,
            body=body
        )

        # Process the result
        news_by_category = {}
        for bucket in result["aggregations"]["news_by_category"]["buckets"]:
            category = bucket["key"]
            count = bucket["doc_count"]
            news_by_category[category] = count

        return news_by_category

    except Exception as e:
        print(f"Error occurred: {e}")
        return None


# Current date
current_date = date.today()
print(current_date)

# Example usage:
news_count_by_category_today = query_news_count_by_category_today(current_date)
if news_count_by_category_today:
    print(news_count_by_category_today)
else:
    print("No news found for today.")
