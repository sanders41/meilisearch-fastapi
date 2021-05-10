import pytest
from async_search_client.errors import MeiliSearchApiError


@pytest.mark.asyncio
async def test_get_documents_none(empty_index, test_client):
    uid, _ = empty_index
    response = await test_client.get(f"/documents/{uid}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_add_documents(empty_index, small_movies, test_client):
    uid, index = empty_index
    document = {"uid": uid, "documents": small_movies}
    response = await test_client.post("/documents", json=document)
    assert "updateId" in response.json()
    update = await index.wait_for_pending_update(response.json()["updateId"])
    assert await index.get_primary_key() == "id"
    assert update.status == "processed"


@pytest.mark.asyncio
async def test_add_documents_with_primary_key(empty_index, test_client, small_movies):
    uid, index = empty_index
    primary_key = "release_date"
    document = {"uid": uid, "documents": small_movies, "primary_key": primary_key}
    response = await test_client.post("/documents", json=document)
    assert "updateId" in response.json()
    update = await index.wait_for_pending_update(response.json()["updateId"])
    assert await index.get_primary_key() == primary_key
    assert update.status == "processed"


@pytest.mark.asyncio
async def test_delete_document(test_client, index_with_documents):
    uid, index = index_with_documents
    response = await test_client.delete(f"/documents/{uid}/500682")
    await index.wait_for_pending_update(response.json()["updateId"])
    with pytest.raises(MeiliSearchApiError):
        await test_client.get(f"/documents/{uid}/500682")


@pytest.mark.asyncio
async def test_delete_documents(test_client, index_with_documents):
    to_delete = ["522681", "450465", "329996"]
    uid, index = index_with_documents
    delete_info = {
        "uid": uid,
        "document_ids": to_delete,
    }
    response = await test_client.post("/documents/delete", json=delete_info)
    await index.wait_for_pending_update(response.json()["updateId"])
    documents = await test_client.get(f"/documents/{uid}")
    ids = [x["id"] for x in documents.json()]
    assert to_delete not in ids


@pytest.mark.asyncio
async def test_delete_all_documents(test_client, index_with_documents):
    uid, index = index_with_documents
    response = await test_client.delete(f"/documents/{uid}")
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/documents/{uid}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_document(test_client, index_with_documents):
    uid, _ = index_with_documents
    response = await test_client.get(f"documents/{uid}/500682")
    assert response.json()["title"] == "The Highwaymen"


@pytest.mark.asyncio
async def test_get_document_nonexistent(test_client, empty_index):
    with pytest.raises(MeiliSearchApiError):
        uid, _ = empty_index
        await test_client.get(f"documents/{uid}/123")


@pytest.mark.asyncio
async def test_get_documents_populated(test_client, index_with_documents):
    uid, _ = index_with_documents
    response = await test_client.get(f"documents/{uid}")
    assert len(response.json()) == 20


@pytest.mark.asyncio
async def test_update_documents(test_client, index_with_documents, small_movies):
    uid, index = index_with_documents
    response = await test_client.get(f"documents/{uid}")
    response_docs = response.json()
    response_docs[0]["title"] = "Some title"
    update_body = {"uid": uid, "documents": response_docs}
    update = await test_client.put("documents", json=update_body)
    await index.wait_for_pending_update(update.json()["updateId"])
    response = await test_client.get(f"documents/{uid}")
    assert response.json()[0]["title"] == "Some title"
    update_body = {"uid": uid, "documents": small_movies}
    update = await test_client.put("documents", json=update_body)
    await index.wait_for_pending_update(update.json()["updateId"])
    response = await test_client.get(f"documents/{uid}")
    assert response.json()[0]["title"] != "Some title"


@pytest.mark.asyncio
async def test_update_documents_with_primary_key(test_client, empty_index, small_movies):
    primary_key = "release_date"
    uid, index = empty_index
    document_info = {"uid": uid, "documents": small_movies, "primaryKey": primary_key}
    update = await test_client.put("/documents", json=document_info)
    await index.wait_for_pending_update(update.json()["updateId"])
    assert await index.get_primary_key() == primary_key
