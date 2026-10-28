/* Shared CSV helpers for the "Export CSV" buttons. Node names, channels, firmware strings and
   message text come from the mesh, so every cell is quoted with inner quotes doubled, and text
   that a spreadsheet would run as a formula (a leading = + - @, tab or carriage return) gets a
   leading ' so it opens as plain text. Plain numbers, including negative ones, are unchanged. */
(function () {
    const NUMBER = /^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$/;
    const FORMULA = /^\s*[=+\-@]|^[\t\r]/;
    window.csvCell = function csvCell(value) {
        if (value === null || value === undefined) return '""';
        let text = String(value);
        if (FORMULA.test(text) && !NUMBER.test(text.trim())) text = "'" + text;
        return '"' + text.replace(/"/g, '""') + '"';
    };
    window.csvFromRows = function csvFromRows(rows) {
        return rows.map(row => row.map(csvCell).join(",")).join("\n");
    };
})();
