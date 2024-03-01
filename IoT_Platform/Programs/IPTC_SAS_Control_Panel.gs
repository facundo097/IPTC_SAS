function doGet(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Control_Panel");
  var response = "";
  
  if (e.parameter.action && e.parameter.action === "readA1") {
    response = sheet.getRange("A1").getValue();
  }

  if (e.parameter.action && e.parameter.action === "readA2") {
    sheet.getRange("H2").setValue(new Date());
    response = sheet.getRange("A2").getValue();
  }

  if (e.parameter.D6) {
    sheet.getRange("D6").setValue(e.parameter.D6);
    response = "Update ";
  }

  if (e.parameter.D7) {
    sheet.getRange("D7").setValue(e.parameter.D7);
    response += "StartStop ";
  }

  if (e.parameter.D8) {
    sheet.getRange("D8").setValue(e.parameter.D8);
    response += "PV ";
  }

  if (e.parameter.D9) {
    sheet.getRange("D9").setValue(e.parameter.D9);
    response += "Ns ";
  }

  if (e.parameter.D10) {
    sheet.getRange("D10").setValue(e.parameter.D10);
    response += "Np ";
  }

  if (e.parameter.D11) {
    sheet.getRange("D11").setValue(e.parameter.D11);
    response += "G ";
  }

  if (e.parameter.D12) {
    sheet.getRange("D12").setValue(e.parameter.D12);
    response += "T ";
  }

  if (e.parameter.D13) {
    sheet.getRange("D13").setValue(e.parameter.D13);
    response += "Ang ";
  }

  if (e.parameter.D14) {
    sheet.getRange("D14").setValue(e.parameter.D14);
    response += "CV ";
  }

  if (e.parameter.D15) {
    sheet.getRange("D15").setValue(e.parameter.D15);
    response += "CVV";
  }

  return ContentService.createTextOutput(response).setMimeType(ContentService.MimeType.TEXT);
}
