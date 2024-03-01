function doGet(e) { 
  Logger.log( JSON.stringify(e) );  // view parameters
  var result = 'Ok'; // assume success
  if (e.parameter == 'undefined') {
    result = 'No Parameters';
  }
  else {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Database");
    var newRow = sheet.getLastRow() + 1;						
    var rowData = [];
    d=new Date();
    rowData[0] = d; // Timestamp in column A
    rowData[1] = d.toLocaleTimeString(); // Timestamp in column A
    
    for (var param in e.parameter) {
      Logger.log('In for loop, param=' + param);
      var value = stripQuotes(e.parameter[param]);
      Logger.log(param + ':' + e.parameter[param]);
      switch (param) {
        case 'I02': 
          rowData[2] = value; 
          result = 'PV ';
          break;
        case 'I03': 
          rowData[3] = value; 
          result += 'Ns ';
          break;
        case 'I04': 
          rowData[4] = value; 
          result += 'Np ';
          break;
        case 'I05': 
          rowData[5] = value; 
          result += 'G ';
          break;
        case 'I06': 
          rowData[6] = value; 
          result += 'T ';
          break;
        case 'I07': 
          rowData[7] = value; 
          result += 'Ang ';
          break;
        case 'I08':
          rowData[8] = value;
          result += 'CV ';
          break;
        case 'Q01':
          rowData[9] = value;
          result += 'Vc ';
          break;
        case 'Q02': 
          rowData[10] = value;
          result += 'Vm ';
          break;
        case 'Q03': 
          rowData[11] = value; 
          result += 'Ic ';
          break;
        case 'Q04': 
          rowData[12] = value; 
          result += 'Im ';
          break;
        case 'Q07': 
          rowData[18] = value; 
          result += 'n ';
          break;
        case 'Q08': 
          rowData[19] = value; 
          result += 'Iph ';
          break;
        case 'Q09': 
          rowData[20] = value;
          result += 'Io ';
          break;
        case 'Q10':
          rowData[21] = value; 
          result += 'Rs ';
          break;
        case 'Q11':
          rowData[22] = value; 
          result += 'Rsh';
          break;
        default:
          result = "Unsupported parameter";
      }
    }
    // Calculate Power based on the logged values of Voltage and current
    rowData[13] = rowData[9] * rowData[11]; // Pc 
    rowData[14] = rowData[10] * rowData[12]; // Pm

    // Calculate and write relative percent errors for voltage, current and power
    if (rowData[9] > 0 || rowData[11] > 0 || rowData[13] > 0 || rowData[15] > 0) {
        rowData[15] = 100 * Math.abs(rowData[9] - rowData[10]) / rowData[9];   // Err_V
        rowData[16] = 100 * Math.abs(rowData[11] - rowData[12]) / rowData[11]; // Err_I
        rowData[17] = 100 * Math.abs(rowData[13] - rowData[14]) / rowData[13]; // Err_P
    }
    else {
        rowData[17] = 0
        rowData[18] = 0
        rowData[19] = 0
        rowData[20] = 0
    }

    Logger.log(JSON.stringify(rowData));
    // Write new row below
    var newRange = sheet.getRange(newRow, 1, 1, rowData.length);
    newRange.setValues([rowData]);
  }
  // Return result of operation
  return ContentService.createTextOutput(result);
}
function stripQuotes( value ) {
  return value.replace(/^["']|['"]$/g, "");
}