function myFunction()
{
    alert("You have called myFunction()")
}

function getCurrentDocumentId()
{
    var url_string = window.location.href;
    var url = new URL(url_string);
    return url.searchParams.get("id");
}

    function doSomethingWithSelectedText() {
        var selectedText = rangy.getSelection();
        if (selectedText != "" && typeof(selectedText) != 'undefined') {
            $('#serializedRangySelection').attr("value", rangy.serializeSelection(selectedText, true))
//            alert("Got selected text " + selectedText);
            $('#makeTagModal').modal('show')
            $('#newTagContent').text("New Tag Content: " + selectedText)
            $('#currentDocumentId').text("Document to Tag: " + getCurrentDocumentId())
            $('#newTagContentForm').attr("value", selectedText)
            $('#currentDocumentIdForm').attr("value", getCurrentDocumentId())
        }
    }

function getTags()
{
    return JSON.parse($('#serializedTags').text())
}

function getTagByPk(tags, pk)
{
    for (let tag of tags)
    {
        if (tag.pk === pk)
            return tag;
    }

    return null;
}

function highlightTags(tags)
{
    highlighter = rangy.createHighlighter();
    for (let tag of tags)
    {
        try{
            serializedSelection = tag.fields.rangySelection;
            console.log("Serialized Selection: " + serializedSelection)
        deserializedSelection = rangy.deserializeSelection(serializedSelection);
        console.log('deserialized selection: ' + deserializedSelection);
        highlighter.addClassApplier(rangy.createClassApplier('highlight', {
        ignoreWhiteSpace: true,
                elementTagName: "a",
                elementProperties: {
                    href: "#",
                    id: tag.pk,
                    onclick: function() {
                        var localTag = getTagByPk(this.id);
                        var creator_id = tag.fields.creator_id;
                        var label = tag.fields.label;
                        var create_datetime = tag.fields.create_datetime;
                        var highlight = highlighter.getHighlightForElement(this);
                        var alert_str = "Creation Date: " + create_datetime + '\n' +
                                        "Author: " + creator_id + '\n' +
                                        "Label: " + label;
                        alert(alert_str);
                        return false;
                    }
                }
         }));
        console.log("adding highlight");
        highlighter.highlightSelection('highlight');
        rangy.getSelection().removeAllRanges();
        }
        catch(err) {
            alert("Error parsing tag: " + tag);
            continue;
        }

    }
}

// need to highlight the selected text
$( document ).ready(function() {
    console.log( "ready!" );
    rangy.init();
    tags = getTags();
    highlightTags(tags);
    document.onmouseup = doSomethingWithSelectedText;
    document.onkeyup = doSomethingWithSelectedText;
});