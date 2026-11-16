// Receives waitlist signups from cobldr.com and adds them to this Google Sheet.
// Setup steps are in README.md next to this file.

var SHEET_NAME = "Waitlist";
var HEADERS = ["Signed up", "Email", "Referrer", "What they're building / what's stopping them"];

function doPost(e) {
  var params = (e && e.parameter) || {};
  var email = String(params.email || "").trim().toLowerCase();

  // Reject anything that isn't an email, and anything a spreadsheet could treat as a formula.
  if (email.length > 254 || /^[=+\-@]/.test(email) || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return respond({ result: "error", message: "invalid email" });
  }
  var answer = cellText(params.answer, 1000);

  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sheet = getSheet();
    var lastRow = sheet.getLastRow();
    if (lastRow > 1) {
      var existing = sheet.getRange(2, 2, lastRow - 1, 1).getValues().map(function (row) { return row[0]; });
      var index = existing.indexOf(email);
      if (index !== -1) {
        // Already signed up: keep the original row, but save a new answer if they gave one.
        if (answer) sheet.getRange(index + 2, 4).setValue(answer);
        return respond({ result: "success", duplicate: true });
      }
    }
    sheet.appendRow([new Date(), email, cellText(params.source, 500), answer]);
  } finally {
    lock.releaseLock();
  }

  return respond({ result: "success" });
}

function getSheet() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = spreadsheet.getSheetByName(SHEET_NAME) || spreadsheet.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.setFrozenRows(1);
  } else if (!sheet.getRange(1, 4).getValue()) {
    sheet.getRange(1, 4).setValue(HEADERS[3]); // Sheets created before the question was added
  }
  return sheet;
}

// Free text from the form, trimmed and length-capped. A leading apostrophe stops Sheets from treating it as a formula.
function cellText(value, maxLength) {
  var text = String(value || "").trim().slice(0, maxLength);
  return /^[=+\-@]/.test(text) ? "'" + text : text;
}

function respond(body) {
  return ContentService.createTextOutput(JSON.stringify(body)).setMimeType(ContentService.MimeType.JSON);
}
