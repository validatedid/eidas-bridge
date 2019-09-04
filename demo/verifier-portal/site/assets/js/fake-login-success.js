$(function() {
    $("#validate-elicence .glyphicon").hide();
});

function validateElicence (requester, attribute, token) {
    $("#validate-elicence .glyphicon").show();

    var data = {
        requester: requester,
        token: token,
        attribute: attribute
    };

    $.ajax({
        type: "POST",
        url: "http://localhost/~albertsolana/Projects/08.eIDAS_Bridge/eidas-bridge/demo/verifier-portal/validate_attribute.php",
        processData: false,
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: onValidationSuccess
    });
}

function onValidationSuccess(data) {
    if (data.result) {
        // Change Modal content on load
        $("#validateModal").modal("show");
        $("#validate-elicence .glyphicon").hide();
    } else {
        console.error('Error');
    }
}