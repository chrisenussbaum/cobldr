// Receives waitlist signups from cobldr.com and adds them to this Google Sheet.
// Setup steps are in README.md next to this file.

var SHEET_NAME = "Waitlist";

function doPost(e) {
  var params = (e && e.parameter) || {};
  var email = String(params.email || "").trim().toLowerCase();

  // Reject anything that isn't an email, and anything a spreadsheet could treat as a formula.
  if (email.length > 254 || /^[=+\-@]/.test(email) || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return respond({ result: "error", message: "invalid email" });
  }

  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sheet = getSheet();
    var lastRow = sheet.getLastRow();
    if (lastRow > 1) {
      var existing = sheet.getRange(2, 2, lastRow - 1, 1).getValues().map(function (row) { return row[0]; });
      if (existing.indexOf(email) !== -1) {
        return respond({ result: "success", duplicate: true });
      }
    }
    sheet.appendRow([new Date(), email, String(params.source || "").slice(0, 500)]);
  } finally {
    lock.releaseLock();
  }

  return respond({ result: "success" });
}

function getSheet() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = spreadsheet.getSheetByName(SHEET_NAME) || spreadsheet.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(["Signed up", "Email", "Referrer"]);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function respond(body) {
  return ContentService.createTextOutput(JSON.stringify(body)).setMimeType(ContentService.MimeType.JSON);
}
