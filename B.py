from A import DataAgent
import json


def main():
    agent = DataAgent()

    # Insert users into the database
    agent.insert_user("Alice", "alice@example.com")
    agent.insert_user("Bob", "bob@example.com")

    # Fetch and display users
    users = agent.fetch_users()
    print("Users in database:")
    for user in users:
        print(user)

    # Call external API
    api_url = "https://jsonplaceholder.typicode.com/todos/1"
    api_response = agent.call_external_api(api_url)

    print("API Response:")
    print(json.dumps(api_response, indent=2))

    # Generate summary and upload to S3
    summary = f"User count: {len(users)}"
    upload_response = agent.upload_to_s3("my-demo-bucket", "user_summary.txt", summary)

    print("S3 Upload Response:")
    print(upload_response)


if __name__ == "__main__":
    main()
