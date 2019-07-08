from eidas_bridge.eidas_bridge import eidas_link_did, \
    eidas_get_service_endpoint_struct, eidas_sign_credential, eidas_verify_credential

did = "this is a test DID"
certificate = "this is a test certificate"
proof = "this is a proof"

print("--- INIT EIDAS DEMO ---\n\r")

print("1.- calling eidas link did ")
print (eidas_link_did("","",""))

print("\n2.- calling eidas get service endpoint struct ")
print (eidas_get_service_endpoint_struct(""))

print("\n3.- calling eidas sign credential ")
print (eidas_sign_credential(""))

print("\n4.- calling eidas verify credential ")
print (eidas_verify_credential(""))

print("\n--- END EIDAS DEMO ---")