# test_did_document.py

import pytest
from eidas_bridge.did_document import DIDDocument, EIDASDIDDocNoSubjectIdException, \
    EIDASServiceEndpointException
from tests.data.common_data import did_documents, bad_did_documents
import json

def test_did_document_bad_types():
    with pytest.raises(TypeError):
        DIDDocument(did_documents[0])

@pytest.mark.parametrize("did_doc", did_documents)
def test_did_document(did_doc):
    str_diddoc = json.dumps(did_doc, indent=4)
    assert DIDDocument(str_diddoc).to_json() == str_diddoc

@pytest.mark.parametrize("did_doc", did_documents)
def test_get_did(did_doc):
    assert DIDDocument(json.dumps(did_doc)).get_did() == did_doc['id']

@pytest.mark.parametrize("did_doc", bad_did_documents)
def test_did_document_no_id(did_doc):
    with pytest.raises(EIDASDIDDocNoSubjectIdException):
        DIDDocument(json.dumps(did_doc))
