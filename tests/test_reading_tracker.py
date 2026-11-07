import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "app" / "reading_tracker.py"
spec = importlib.util.spec_from_file_location("reading_tracker_t07", SOURCE)
tracker = importlib.util.module_from_spec(spec)
with patch.dict(os.environ, {"READING_DATA_MODE": "local"}):
    spec.loader.exec_module(tracker)


class ReadingTrackerTests(unittest.TestCase):
    def test_local_add_read_and_health_without_sdk(self):
        with patch.dict(os.environ, {"READING_DATA_MODE": "local", "APP_INSTANCE": "test-local"}):
            client = tracker.create_app().test_client()
        with patch.dict("sys.modules", {"boto3": None}):
            health = client.get("/health")
            self.assertEqual(health.status_code, 200)
            self.assertEqual(health.json["stage"], "reading-tracker")
            self.assertEqual(health.headers["X-App-Instance"], "test-local")
            self.assertIn(b"No books yet", client.get("/").data)
            for _ in range(2):
                response = client.post("/", data={
                    "title": "Cloud Notes", "pages_read": 20, "total_pages": 40, "rating": 4,
                })
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.headers["Location"], "/")
            page = client.get("/")
            self.assertEqual(page.data.count(b"<h2>Cloud Notes</h2>"), 2)
            self.assertIn(b"50% complete", page.data)
            self.assertIn(b"4.0/5", page.data)
            self.assertIn(b'<div class="num">40</div>', page.data)
            for data in ({"title": " "}, {"title": "Bad", "rating": "6"},
                         {"title": "Bad", "pages_read": "3", "total_pages": "2"}):
                self.assertEqual(client.post("/", data=data).status_code, 400)

    def test_dynamodb_wire_contract(self):
        import boto3
        from botocore.stub import Stubber
        from boto3.dynamodb.types import TypeSerializer

        table = boto3.session.Session().resource(
            "dynamodb", region_name="us-east-1",
            aws_access_key_id="test", aws_secret_access_key="test",
        ).Table("test-books")
        book = tracker.parse_entry({"title": "Example", "pages_read": "2", "total_pages": "4"})
        item = {key: TypeSerializer().serialize(value) for key, value in book.items()}
        cursor = {"record_id": item["record_id"]}
        store = tracker.DynamoStore("us-east-1", "test-books")
        with Stubber(table.meta.client) as stub, patch.object(store, "table", return_value=table):
            stub.add_response("put_item", {}, {
                "TableName": "test-books", "Item": book,
                "ConditionExpression": "attribute_not_exists(record_id)",
            })
            stub.add_response("scan", {"Items": [], "LastEvaluatedKey": cursor}, {
                "TableName": "test-books", "ConsistentRead": True,
            })
            stub.add_response("scan", {"Items": [item]}, {
                "TableName": "test-books", "ConsistentRead": True,
                "ExclusiveStartKey": {"record_id": book["record_id"]},
            })
            self.assertEqual(store.save_book(book), book["record_id"])
            self.assertEqual(store.load_books(), [book])
            stub.assert_no_pending_responses()

    def test_cloud_storage_failure_and_process_health(self):
        from botocore.exceptions import ClientError

        with patch.dict(os.environ, {
            "READING_DATA_MODE": "dynamodb", "AWS_DEFAULT_REGION": "us-east-1",
            "READING_TABLE": "test-books",
        }):
            app = tracker.create_app()
        client = app.test_client()
        error = ClientError({"Error": {"Code": "AccessDeniedException", "Message": "internal"}}, "Scan")
        with patch.object(tracker.DynamoStore, "table", side_effect=error) as table:
            self.assertEqual(client.get("/health").status_code, 200)
            table.assert_not_called()
            with self.assertLogs(app.logger, level="ERROR"):
                read = client.get("/")
                write = client.post("/", data={"title": "Example"})
            self.assertEqual((read.status_code, write.status_code), (503, 503))
            self.assertNotIn(b"AccessDeniedException", read.data)

    def test_cloud_requires_explicit_configuration(self):
        with patch.dict(os.environ, {"READING_DATA_MODE": "dynamodb"}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "AWS_DEFAULT_REGION"):
                tracker.create_app()


if __name__ == "__main__":
    unittest.main()
