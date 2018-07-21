import Qt.labs.platform 1.0

FileDialog {
    id: root

    property string output

    onAccepted: {
        // 1 (File) : File (remove file://) : format
        var fileString = file.toString()
        if (fileString.startsWith("file:///")) {
            // Check if is a windows string (8) or linux (7)
            var sliceValue = fileString.charAt(9) === ':' ? 8 : 7
            fileString = fileString.substring(sliceValue)
        }

        output = fileString
    }
}